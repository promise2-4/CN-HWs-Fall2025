# HW4 Practical Q1: SNMP Monitoring Commands

This practical part configures a local SNMP agent and queries basic system and
interface information.

## Setup

Install the SNMP service and command-line tools:

```sh
sudo apt update
sudo apt install snmp snmpd
```

Edit the SNMP daemon configuration:

```sh
sudo nano /etc/snmp/snmpd.conf
```

For a local lab setup, configure a read-only community string such as:

```text
rocommunity public 127.0.0.1
```

Restart the service:

```sh
sudo systemctl restart snmpd
sudo systemctl status snmpd
```

## Queries

Query the system name:

```sh
snmpget -v2c -c public localhost .1.3.6.1.2.1.1.5.0
```

Query system uptime:

```sh
snmpget -v2c -c public localhost .1.3.6.1.2.1.1.3.0
```

List network interface descriptions:

```sh
snmpwalk -v2c -c public localhost .1.3.6.1.2.1.2.2.1.2
```

Query interface speed values:

```sh
snmpwalk -v2c -c public localhost .1.3.6.1.2.1.2.2.1.5
```

Query received octets per interface:

```sh
snmpwalk -v2c -c public localhost .1.3.6.1.2.1.2.2.1.10
```

## Notes

- Numeric OIDs are used so the commands work even when MIB names are not
  installed or loaded.
- The `public` community string is suitable only for local lab experiments.
  Production SNMP deployments should use stronger access control and SNMPv3.
