# Computer Networks Homework Practicals

Practical implementation archive for **Computer Networks, Fall 2025**.

This repository contains only the practical parts of the homework set: question
PDFs where available, source code, simulation/configuration files, and concise
README files explaining each practical task. Reports, answer PDFs, submission
archives, generated files, and screenshots are intentionally excluded.

> Repository description: Computer Networks practical homework implementations
> covering HTTP load balancing, DNS tunneling, IP fragmentation simulation,
> SNMP monitoring, and ICMP packet analysis.

## Contents

```text
.
├── HW1/
│   ├── HW1-questions.pdf
│   ├── README.md
│   └── practical/
│       ├── http_load_balancer.py
│       ├── http_server.py
│       ├── start_servers.py
│       └── test_load_balancer.py
├── HW2/
│   ├── README.md
│   └── practical-dns-tunnel/
│       ├── client.py
│       └── server.py
├── HW3/
│   ├── HW3-questions.pdf
│   ├── README.md
│   └── practical-fragmentation/
│       ├── Fragmentation.ned
│       └── omnetpp.ini
└── HW4/
    ├── HW4-questions.pdf
    ├── README.md
    ├── practical-icmp/
    │   └── custom_ping.py
    └── practical-snmp/
        └── snmp_commands.md
```

## Homework Summary

| Homework | Practical Topic | Main Technologies |
| --- | --- | --- |
| HW1 | HTTP load balancer | Python sockets, threading, HTTP |
| HW2 | DNS tunneling proxy | Python sockets, DNS TXT records, HTTP/SOCKS |
| HW3 | IP fragmentation | OMNeT++, INET, NED, simulation config |
| HW4 | SNMP and ICMP | `snmpget`, `snmpwalk`, Scapy |

## Public Repository Cleanup

Before publishing, the repository was cleaned to remove:

- Report PDFs and answer documents
- Submission zip files
- `.DS_Store` files
- Word temporary files
- Generated outputs and screenshots

## Course Context

Implemented for the Computer Networks course, Fall 2025.
