# HW4 Practicals: SNMP and ICMP

HW4 focuses on two classic network diagnostic and management tools: SNMP for
reading management information from a host, and ICMP for sending and inspecting
Echo Request/Echo Reply traffic.

**Author:** Parmis Hemasian

Course: Computer Networks, Sharif University of Technology, Fall 2025

## Practical Q1: SNMP

The first practical configures a local SNMP agent and queries information from
the system MIB. The goal is to see how a manager can read operational data from
an SNMP-enabled machine.

The included command file covers:

- Installing `snmp` and `snmpd`.
- Adding a read-only local community string for lab use.
- Restarting and checking the SNMP daemon.
- Querying system name and uptime.
- Walking interface descriptions, speeds, and received octet counters.
- Using numeric OIDs when symbolic MIB names are unavailable.

Files:

- `HW4-questions.pdf`: original assignment questions.
- `practical-snmp/snmp_commands.md`: setup and query commands.

Run the SNMP commands on a Linux machine with `snmpd` installed. The commands
use `localhost` and the lab community string `public`; this is only appropriate
for a local controlled setup.

## Practical Q2: ICMP

The second practical builds ICMP Echo Request packets manually with Scapy. It
sends one packet to a reachable destination and another to an unreachable local
address, then prints the observed response behavior.

The script demonstrates:

- Creating an IPv4 packet with an ICMP payload.
- Setting a custom ICMP identifier and sequence number.
- Measuring round-trip time.
- Inspecting returned packet fields with Scapy.
- Comparing a successful Echo Reply with a timeout/unreachable case.

Files:

- `practical-icmp/custom_ping.py`: Scapy-based ICMP test script.

## Running The ICMP Script

Install Scapy:

```sh
pip install scapy
```

Run the script with privileges if your OS requires raw-socket access:

```sh
sudo python3 practical-icmp/custom_ping.py
```

Expected behavior:

- `8.8.8.8` should normally return an Echo Reply if ICMP is allowed by the
  network.
- `192.168.1.222` is used as an example unreachable/private address and may
  time out depending on the local network.

## Notes

- ICMP experiments depend heavily on local firewall rules and network policy.
- SNMP output depends on the Linux distribution, available MIB files, and the
  network interfaces visible inside the VM or host.
- The report files and screenshots were intentionally excluded from this public
  repository; only the practical commands and implementation code are kept.
