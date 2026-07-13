import socket
import threading
import base64
import struct
import requests

DNS_PORT = 5454
UPSTREAM_DNS = ("8.8.8.8", 53)
CHUNK_SIZE = 300 
response_cache = {}

def parse_qname(data):
    labels = []
    i = 12
    while data[i] != 0:
        l = data[i]
        labels.append(data[i+1:i+1+l].decode())
        i += l + 1
    return labels, i + 1

def build_dns_response(txid, qname_bytes, payload_bytes):
    header = struct.pack("!HHHHHH", txid, 0x8180, 1, 1, 0, 0)
    question = qname_bytes + struct.pack("!HH", 16, 1)
    answer_header = b"\xc0\x0c" + struct.pack("!HHI", 16, 1, 60)
    txt_data = b""
    for i in range(0, len(payload_bytes), 254):
        chunk = payload_bytes[i:i+254]
        txt_data += bytes([len(chunk)]) + chunk
    answer = answer_header + struct.pack("!H", len(txt_data)) + txt_data
    return header + question + answer

def handle_tunnel(data, addr, sock, labels, q_end):
    txid = struct.unpack("!H", data[:2])[0]
    qname_bytes = data[12:q_end]
    try:
        idx = 0
        target_labels = labels[:-1]
        if target_labels[0].startswith("idx"):
            idx = int(target_labels[0][3:])
            target_labels = target_labels[1:]
        
        url = base64.b64decode("".join(target_labels)).decode()
        if url not in response_cache:
            resp = requests.get(url, timeout=5)
            response_cache[url] = base64.b64encode(resp.content)

        full_data = response_cache[url]
        start = idx * CHUNK_SIZE
        chunk_to_send = full_data[start : start + CHUNK_SIZE]
        sock.sendto(build_dns_response(txid, qname_bytes, chunk_to_send), addr)
    except Exception as e: print(f"Err: {e}")

def handle_packet(data, addr, sock):
    try:
        labels, q_end = parse_qname(data)
        if labels and "tunnel" in labels: handle_tunnel(data, addr, sock, labels, q_end)
        else:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.settimeout(3); s.sendto(data, UPSTREAM_DNS)
                sock.sendto(s.recvfrom(1024)[0], addr)
    except: pass

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", DNS_PORT))
print("[+] Server Running")
while True:
    d, a = sock.recvfrom(2048)
    threading.Thread(target=handle_packet, args=(d, a, sock)).start()