# HW2 Practical: DNS Tunneling Proxy

This practical assignment implements a simple DNS tunneling system in Python.
It uses DNS TXT responses to carry HTTP response data back to a local proxy.

**Author:** Parmis Hemasian

## What It Does

- Runs a DNS server on port `5454`.
- For normal DNS queries, forwards traffic to an upstream resolver.
- For `.tunnel` queries, decodes an encoded URL and fetches the target content.
- Splits large responses into chunks.
- Provides a local HTTP proxy on port `3128`.
- Provides a local SOCKS5 proxy on port `8080`.
- Handles concurrent requests with threads.

## Files

- `HW2-questions.pdf`: original practical assignment questions.
- `practical-dns-tunnel/server.py`: DNS server and tunnel endpoint.
- `practical-dns-tunnel/client.py`: local HTTP/SOCKS proxy client.

## Run

Start the DNS tunnel server:

```sh
cd practical-dns-tunnel
python3 server.py
```

In another terminal, start the client proxy:

```sh
python3 client.py
```

Example HTTP proxy test:

```sh
curl -x http://localhost:3128 http://ifconfig.io
```

Example SOCKS5 proxy test:

```sh
curl -v -x socks5h://localhost:8080 http://ifconfig.io
```
