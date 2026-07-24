# Lab Verification Script

Automates the "Verification Commands" checklist already documented in the main lab
[`readme.md`](../readme.md) — instead of running `show ip ospf neighbor`,
`show ip nat translations`, `show etherchannel summary`, etc. by hand after every
change, `verify_lab.py` runs the full checklist and reports pass/fail per device.

## Setup

```bash
pip install netmiko pyyaml
cp devices.example.yaml devices.yaml
# edit devices.yaml with real credentials/addresses
```

## Usage

```bash
python3 verify_lab.py --inventory devices.yaml            # check every device
python3 verify_lab.py --inventory devices.yaml --device BORDER   # check one device
python3 verify_lab.py --inventory devices.yaml --json      # machine-readable output
```

Exit code is `0` if every check passed, `1` if anything failed, `2` on a setup/input error — so this drops straight into a CI job or a scheduled task if you want the lab re-verified automatically after changes.

## ⚠️ One real caveat: Packet Tracer reachability

This script is written IOS-generically and connects over real SSH via
[netmiko](https://github.com/ktbyers/netmiko) — it works unmodified against real
Cisco hardware, GNS3, or EVE-NG. The one thing to know if you're running it against
this lab specifically **inside Packet Tracer**: PT's simulated devices aren't
reachable from your host machine's network stack by default. To actually SSH into
them from outside Packet Tracer, the topology needs a **Cloud-PT** (or a bridged
NIC) connecting the simulated network to a real interface on your machine.

If that's not set up, the practical options are:
- Run the verification commands manually inside Packet Tracer (as the readme
  already describes) — this script doesn't replace that, it's for when you want
  it automated.
- Bridge the topology out via Cloud-PT and point `devices.yaml` at the bridged
  addresses.
- Reuse this exact script unchanged if you ever rebuild this same topology in
  GNS3, EVE-NG, or on physical hardware — that's the scenario it was written for
  first, with Packet Tracer as a secondary target.

## Extending

Each device's checks are defined in the `DEVICE_CHECKS` dict at the top of
`verify_lab.py` — add a new `Check(name, command, validator)` entry to check
something else, or write a new `validate_*` function for a command this doesn't
already parse.
