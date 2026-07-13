# HW3 Practical: IP Fragmentation Simulation

This practical assignment models packet fragmentation in OMNeT++/INET.

## What It Does

- Builds a small network with two hosts and one router.
- Sends UDP traffic from `hostA` to `hostB`.
- Sets a reduced MTU on the router output interface.
- Forces a 1500-byte UDP payload to fragment across the constrained link.

## Files

- `HW3-questions.pdf`: original assignment questions.
- `practical-fragmentation/Fragmentation.ned`: OMNeT++ network topology.
- `practical-fragmentation/omnetpp.ini`: simulation configuration.

## Run

Open the folder as an OMNeT++/INET simulation project, then run the
`FragmentationNetwork` scenario defined in `omnetpp.ini`.

The important setting is:

```ini
**.router.eth[1].mac.mtu = 500B
```

This MTU is smaller than the generated packet, so fragmentation is observable in
the simulation event log and packet inspector.
