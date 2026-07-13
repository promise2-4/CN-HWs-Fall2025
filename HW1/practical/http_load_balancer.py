import socket
import threading
import time
import re
from collections import defaultdict
import select

ROUND_ROBIN = "round_robin"
LEAST_TIME = "least_time"
LOAD_BALANCING_ALGORITHMS = [ROUND_ROBIN, LEAST_TIME]


class HTTPLoadBalancer:
    def __init__(self, lb_host='localhost', lb_port=8000):
        self.lb_host = lb_host
        self.lb_port = lb_port
        self.lb_socket = None
        self.running = False
        
        # قفل برای دسترسی thread-safe به متغیرهای مشترک
        self.lock = threading.Lock()
        
        # آمار پاسخ‌گویی سرورها برای الگوریتم Least Time
        self.response_times = defaultdict(list)  # key: server_id, value: list of response times
        self.last_selected = {}  # برای Round Robin با وزن

        self.upstream_groups = {
            "round_robin.cn.edu": {
                "algorithm": ROUND_ROBIN,
                "servers": [
                    {"host": "127.0.0.1", "port": 8080, "weight": 1, "healthy": True, "timeout": 2},
                    {"host": "127.0.0.1", "port": 8081, "weight": 3, "healthy": True, "timeout": 2},
                    {"host": "domain.cn.edu", "port": 8082, "weight": 2, "healthy": True, "timeout": 3},
                ]
            },
            "least_time.cn.edu": {
                "algorithm": LEAST_TIME,
                "servers": [
                    {"host": "127.0.0.1", "port": 8083, "weight": 1, "healthy": True, "timeout": 2},
                    {"host": "127.0.0.1", "port": 8084, "weight": 1, "healthy": True, "timeout": 2},
                    {"host": "domain.cn.edu", "port": 8085, "weight": 1, "healthy": True, "timeout": 3},
                ]
            }
        }

    def start_load_balancer(self):
        try:
            self.lb_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.lb_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.lb_socket.bind((self.lb_host, self.lb_port))
            self.lb_socket.listen(10)
            self.running = True
            
            print(f" HTTP Load Balancer started on {self.lb_host}:{self.lb_port}")
            for domain, group in self.upstream_groups.items():
                print(f" Domain: {domain}")
                print(f"  Algorithm: {group['algorithm']}")
                print(f"  Servers: {len(group['servers'])}")
            print("=" * 50)
            
            # شروع تردهای مانیتورینگ سلامت و دستورات
            threading.Thread(target=self.monitor_health, daemon=True).start()
            threading.Thread(target=self.handle_commands, daemon=True).start()

            while self.running:
                try:
                    client_socket, client_address = self.lb_socket.accept()
                    client_thread = threading.Thread(
                        target=self.handle_http_request,
                        args=(client_socket, client_address)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                except Exception as e:
                    if self.running:
                        print(f"Load balancer error: {e}")
                        
        except Exception as e:
            print(f"Failed to start load balancer: {e}")
        finally:
            self.stop_load_balancer()
    
    def extract_host_header(self, request_str):
        # پیدا کردن هدر Host با regex قوی و مقاوم
        match = re.search(r'^Host:\s*([^\r\n:]+)', request_str, re.IGNORECASE | re.MULTILINE)
        if match:
            host = match.group(1).strip()
            # حذف پورت اگر وجود داشت (مثل example.com:8000)
            return host.split(':')[0]
        return ""

    def select_upstream_server(self, domain: str):
        if not domain or domain not in self.upstream_groups:
            return None

        group = self.upstream_groups[domain]
        algorithm = group["algorithm"]
        servers = [s for s in group["servers"] if s["healthy"]]

        if not servers:
            return None  # هیچ سرور سالمی نیست

        with self.lock:
            if algorithm == ROUND_ROBIN:
                # Weighted Round Robin ساده
                if domain not in self.last_selected:
                    self.last_selected[domain] = -1
                
                total_weight = sum(s["weight"] for s in servers)
                current = (self.last_selected[domain] + 1) % total_weight
                self.last_selected[domain] = current

                count = 0
                for server in group["servers"]:
                    if not server["healthy"]:
                        continue
                    count += server["weight"]
                    if current < count:
                        return server

            elif algorithm == LEAST_TIME:
                # انتخاب سروری که میانگین کمترین زمان پاسخ رو داره
                best_server = None
                best_avg = float('inf')

                for server in servers:
                    server_id = f"{server['host']}:{server['port']}"
                    times = self.response_times[server_id]
                    avg_time = sum(times) / len(times) if times else 0.1  # اولویت اولیه به همه
                    if avg_time < best_avg:
                        best_avg = avg_time
                        best_server = server
                return best_server

        return servers[0]  # fallback

    def handle_http_request(self, client_socket, client_address):
        try:
            request_data = client_socket.recv(4096)
            if not request_data:
                return
            
            request_str = request_data.decode('utf-8', errors='ignore')
            host_header = self.extract_host_header(request_str)
            upstream_server = self.select_upstream_server(host_header)
            
            if not host_header:
                self.send_error_response(client_socket, 400, "Bad Request: Missing Host header")
                return

            if not upstream_server:
                if host_header in self.upstream_groups:
                    self.send_error_response(client_socket, 503, "No Healthy Upstream")
                else:
                    self.send_error_response(client_socket, 404, "Domain Not Found")
                return

            result = self.forward_http_request(client_socket, upstream_server, request_data)
            
            # به‌روزرسانی آمار برای Least Time و Passive Health Check
            if result["success"]:
                server_id = result["server_id"]
                with self.lock:
                    self.response_times[server_id].append(result["response_time"])
                    # فقط 20 تا آخرین زمان رو نگه می‌داریم
                    if len(self.response_times[server_id]) > 20:
                        self.response_times[server_id] = self.response_times[server_id][-20:]
            else:
                # اگر خطا بود (مثل timeout)، سرور رو ناسالم علامت بزن
                if "timeout" in result.get("error", "").lower():
                    upstream_server["healthy"] = False

        except Exception as e:
            print(f"Error handling request from {client_address}: {e}")
            self.send_error_response(client_socket, 500, "Internal Server Error")
        finally:
            client_socket.close()
    
    def forward_http_request(self, client_socket, upstream_server, request_data):
        upstream_socket = None
        start_time = time.time()

        try:
            upstream_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            upstream_socket.settimeout(upstream_server["timeout"])
            upstream_socket.connect((upstream_server["host"], upstream_server["port"]))
            
            upstream_socket.send(request_data)
            
            response_data = upstream_socket.recv(4096)
            client_socket.send(response_data)
            
            response_time = time.time() - start_time
            
            return {
                "success": True,
                "response_time": response_time,
                "response_data": response_data,
                "server_id": f"{upstream_server['host']}:{upstream_server['port']}",
                "upstream_server": upstream_server
            }
            
        except socket.timeout:
            self.send_error_response(client_socket, 504, "Gateway Timeout")
            return {
                "success": False,
                "error": "timeout",
                "server_id": f"{upstream_server['host']}:{upstream_server['port']}",
                "upstream_server": upstream_server
            }
        except Exception as e:
            self.send_error_response(client_socket, 502, "Bad Gateway")
            return {
                "success": False,
                "error": str(e),
                "server_id": f"{upstream_server['host']}:{upstream_server['port']}",
                "upstream_server": upstream_server
            }
        finally:
            if upstream_socket:
                upstream_socket.close()
    
    def check_server_health(self, server):
        try:
            health_request = "GET /healthz HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n\r\n"
            
            health_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            health_socket.settimeout(server["timeout"])
            health_socket.connect((server["host"], server["port"]))
            health_socket.send(health_request.encode('utf-8'))
            
            response = health_socket.recv(1024).decode('utf-8')
            health_socket.close()
            
            # اگر کد 200 بود و بدنه شامل OK بود → سالم
            if "200 OK" in response and "OK" in response.split("\r\n\r\n")[-1]:
                return True
            return False
                
        except Exception:
            return False
    
    def monitor_health(self):
        while self.running:
            time.sleep(5)
            with self.lock:
                for domain, group in self.upstream_groups.items():
                    for server in group["servers"]:
                        was_healthy = server["healthy"]
                        is_healthy = self.check_server_health(server)
                        server["healthy"] = is_healthy
                        if was_healthy != is_healthy:
                            status = "Healthy" if is_healthy else "Unhealthy"
                            print(f"Health change → {server['host']}:{server['port']} is now {status}")

    def send_error_response(self, client_socket, status: int, message: str = ""):
        status_texts = {
            400: "Bad Request",
            404: "Not Found",
            500: "Internal Server Error",
            502: "Bad Gateway",
            503: "Service Unavailable",
            504: "Gateway Timeout"
        }
        text = status_texts.get(status, "Error")
        if message:
            body = message
        else:
            body = text
        
        http_response = (
            f"HTTP/1.1 {status} {text}\r\n"
            "Content-Type: text/plain\r\n"
            f"Content-Length: {len(body)}\r\n"
            "Connection: close\r\n"
            "\r\n"
            f"{body}"
        )
        try:
            client_socket.send(http_response.encode('utf-8'))
        except:
            pass

    def handle_commands(self):
        print("Command console started. Type 'help' for commands.")
        while self.running:
            try:
                cmd = input("> ").strip().lower()
                if cmd == "list":
                    self.list_upstream_servers()
                elif cmd == "quit" or cmd == "exit":
                    self.quit_load_balancer()
                    break
                elif cmd == "help":
                    print("Commands: list, quit")
                elif cmd == "":
                    continue
                else:
                    print("Unknown command. Type 'help'.")
            except:
                break

    def list_upstream_servers(self):
        print("\nUpstream Servers Status:")
        print("=" * 50)
        for domain, group in self.upstream_groups.items():
            print(f"Domain: {domain} ({group['algorithm']})")
            for i, server in enumerate(group["servers"], 1):
                status = "Healthy" if server["healthy"] else "Unhealthy"
                weight = server.get("weight", 1)
                print(f"  [{i}] {server['host']}:{server['port']} | Weight: {weight} | {status}")
        print()

    def quit_load_balancer(self):
        print("Shutting down load balancer...")
        self.running = False

    def stop_load_balancer(self):
        self.running = False
        if self.lb_socket:
            self.lb_socket.close()
        print("Load balancer stopped")


def main():
    print("HTTP LOAD BALANCER")
    print("=" * 60)
    lb = HTTPLoadBalancer()
    try:
        lb.start_load_balancer()
    except KeyboardInterrupt:
        print("\nLoad balancer stopped by user")
    finally:
        lb.stop_load_balancer()

if __name__ == "__main__":
    main()