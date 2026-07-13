import socket, threading, base64, struct, time

DNS_SERVER = ("127.0.0.1", 5454)

def dns_tunnel_fetch(url_bytes):
    full_b64 = b""; chunk_idx = 0
    url_b64 = base64.b64encode(url_bytes).decode()
    while True:
        query_str = f"idx{chunk_idx}." + ".".join([url_b64[i:i+50] for i in range(0, len(url_b64), 50)]) + ".tunnel"
        packet = struct.pack("!HHHHHH", 0xAAAA+chunk_idx, 0x0100, 1, 0, 0, 0)
        for label in query_str.split("."): packet += bytes([len(label)]) + label.encode()
        packet += b"\x00" + struct.pack("!HH", 16, 1)
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(5); s.sendto(packet, DNS_SERVER)
            try:
                data, _ = s.recvfrom(4096)
                txt_seg = data[len(packet)+12:]; chunk = b""; curr = 0
                while curr < len(txt_seg):
                    l = txt_seg[curr]; chunk += txt_seg[curr+1:curr+1+l]; curr += l+1
                if not chunk: break
                full_b64 += chunk; chunk_idx += 1
            except: break
    return base64.b64decode(full_b64)

def handle_http(c):
    try:
        data = c.recv(4096)
        if not data: return
        url = data.split(b' ')[1]
        if not url.startswith(b'http'): url = b"http://" + url
        content = dns_tunnel_fetch(url)
        c.sendall(b"HTTP/1.1 200 OK\r\nContent-Length: "+str(len(content)).encode()+b"\r\n\r\n"+content)
    finally: c.close()

def handle_socks(c):
    try:
        c.recv(262); c.sendall(b"\x05\x00")
        req = c.recv(4)
        if req and req[3] == 0x03:
            domain = c.recv(c.recv(1)[0]); c.recv(2)
            content = dns_tunnel_fetch(b"http://" + domain)
            c.sendall(b"\x05\x00\x00\x01\x00\x00\x00\x00\x00\x00")
            c.sendall(b"HTTP/1.1 200 OK\r\nContent-Length: "+str(len(content)).encode()+b"\r\n\r\n"+content)
    finally: c.close()

def start_proxy(port, handler):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", port)); s.listen(50)
    while True:
        conn, _ = s.accept()
        threading.Thread(target=handler, args=(conn,)).start()

print("[+] Client Ready: HTTP(3128), SOCKS(8080)")
threading.Thread(target=start_proxy, args=(3128, handle_http), daemon=True).start()
start_proxy(8080, handle_socks)