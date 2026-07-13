# HW4 Practicals: SNMP and ICMP

HW4 contains two practical networking tasks.

## Practical Q1: SNMP

The SNMP part configures a local SNMP agent and queries system/interface
information with `snmpget` and `snmpwalk`.

Files:

- `HW4-questions.pdf`: original assignment questions.
- `practical-snmp/snmp_commands.md`: setup and query commands.

## Practical Q2: ICMP

The ICMP part uses Scapy to craft Echo Request packets, send them to reachable
and unreachable destinations, and inspect the replies.

Files:

- `practical-icmp/custom_ping.py`: Scapy-based ICMP test script.

## Run ICMP Script

Install Scapy:

```sh
pip install scapy
```

Run the script with privileges if your OS requires raw-socket access:

```sh
sudo python3 practical-icmp/custom_ping.py
```
