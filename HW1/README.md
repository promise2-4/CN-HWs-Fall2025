# HW1 Practical: HTTP Load Balancer

This practical assignment implements an application-layer HTTP load balancer in
Python.

## What It Does

- Routes HTTP requests based on the `Host` header.
- Supports `round_robin.cn.edu` and `least_time.cn.edu` upstream groups.
- Implements weighted round-robin scheduling.
- Tracks response time history for least-time routing.
- Performs active health checks through `/healthz`.
- Marks timed-out upstreams unhealthy through passive health checks.
- Handles multiple client connections using threads.

## Files

- `HW1-questions.pdf`: original assignment questions.
- `practical/http_load_balancer.py`: load balancer implementation.
- `practical/http_server.py`: simple upstream HTTP server.
- `practical/start_servers.py`: helper to start the upstream servers.
- `practical/test_load_balancer.py`: automated tests.

## Run

Start the upstream servers:

```sh
cd practical
python3 start_servers.py
```

In another terminal, start the load balancer:

```sh
python3 http_load_balancer.py
```

Then run the tests:

```sh
python3 test_load_balancer.py
```
