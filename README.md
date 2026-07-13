# Computer Networks Homework Practicals

Practical implementation archive for the **Computer Networks** course at
**Sharif University of Technology**, Fall 2025.

**Author:** Parmis Hemasian

This repository keeps the practical side of the homework set in a clean,
reviewable form. It includes the assignment questions, source code,
configuration files, and short explanations for each practical task. Personal
reports, answer PDFs, submission archives, screenshots, and generated files are
left out on purpose.

> Repository description: Computer Networks practical homework implementations
> covering HTTP load balancing, DNS tunneling, IP fragmentation simulation,
> SNMP monitoring, and ICMP packet analysis.

## Overview

The homeworks cover several layers of the networking stack:

- Application-layer request routing with an HTTP load balancer.
- Tunneling HTTP traffic through DNS TXT responses.
- Packet fragmentation behavior in an OMNeT++/INET simulation.
- Basic network management with SNMP.
- ICMP Echo Request/Reply packet construction and inspection.

Each homework folder has its own README with the practical goal, included
files, and basic run instructions.

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
│   ├── HW2-questions.pdf
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

| Homework | Practical topic | Main technologies |
| --- | --- | --- |
| HW1 | HTTP load balancing by `Host` header | Python sockets, threads, HTTP |
| HW2 | DNS tunnel with HTTP and SOCKS clients | Python sockets, DNS TXT records |
| HW3 | IP fragmentation simulation | OMNeT++, INET, NED, `omnetpp.ini` |
| HW4 | SNMP monitoring and ICMP probing | `snmpget`, `snmpwalk`, Scapy |

## How To Use

Start from the README inside the homework you want to run. Some parts are normal
Python programs; others need a specific lab environment:

- HW1 and HW2 can be run with Python 3. HW1 also needs the `requests` package
  for its test script.
- HW3 needs OMNeT++ with the INET framework.
- HW4 Q1 needs Linux SNMP tools and `snmpd`.
- HW4 Q2 needs Scapy and raw-socket permission, so it may require `sudo`.

The question PDFs are included for context, but the repository is organized
around the practical implementations rather than written answers.

## Public Repository Cleanup

Before publishing, the repository was cleaned to remove:

- Report PDFs and answer documents
- Submission zip files
- `.DS_Store` files
- Word temporary files
- Generated outputs and screenshots

## Course Context

Implemented for the Computer Networks course at Sharif University of
Technology, Fall 2025.
