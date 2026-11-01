# Computer Networks — Practical Homework

A collection of the programming exercises from the Computer Networks course at Sharif University of Technology (Fall 2025). Each homework directory includes the code, question sheet, and setup notes.

| Homework | Implementation | Tools |
| --- | --- | --- |
| [HW1](HW1/README.md) | HTTP load balancing based on Host headers | Python sockets, threads |
| [HW2](HW2/README.md) | HTTP-over-DNS tunneling | Python sockets, DNS TXT records |
| [HW3](HW3/README.md) | IP fragmentation simulation | OMNeT++, INET |
| [HW4](HW4/README.md) | SNMP queries and ICMP packet inspection | SNMP tools, Scapy |

## Getting started

Start with the README inside the homework you want to run. HW1 and HW2 use Python 3; HW1's test script also needs `requests`. HW3 requires OMNeT++ and INET. HW4 uses `snmpget`, `snmpwalk`, and Scapy, with raw-socket permissions for ICMP experiments.

The folders are independent exercises, not parts of a single deployable network service. Original assignment PDFs are included for context; personal reports and generated artifacts are excluded.
