#!/usr/bin/env python3
"""
verify_lab.py

Automates the "Verification Commands" checklist already documented in this lab's
readme.md (show ip ospf neighbor, show ip nat translations, show etherchannel
summary, show access-lists, etc.) instead of running them by hand after every
change to the topology.

This is written to be IOS-generic: it works unmodified against real Cisco
hardware, GNS3, or EVE-NG -- not just Packet Tracer. See the companion
README.md in this folder for the one real caveat: Packet Tracer's simulated
devices are only reachable over real SSH if the topology is bridged out via a
Cloud-PT / real NIC, since PT doesn't expose its virtual devices to the host's
network stack by default.

Usage:
    python3 verify_lab.py --inventory devices.yaml
    python3 verify_lab.py --inventory devices.yaml --device BORDER
    python3 verify_lab.py --inventory devices.yaml --json

Exit codes:
    0  -- every check passed
    1  -- one or more checks failed
    2  -- connection or input error
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from typing import Callable, Optional

try:
    import yaml
except ImportError:
    yaml = None

from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException


@dataclass
class Check:
    name: str
    command: str
    validator: Callable[[str], tuple]  # returns (passed: bool, detail: str)


@dataclass
class DeviceResult:
    device: str
    reachable: bool = True
    error: Optional[str] = None
    checks: list = field(default_factory=list)  # list of (Check.name, passed, detail)


# ---------------------------------------------------------------------------
# Validators -- each parses a specific "show" command's output and returns
# (passed, human-readable detail). These map directly to what the lab readme
# already tells a human to look for manually.
# ---------------------------------------------------------------------------

def validate_ospf_neighbors(output: str, expected_min: int = 1):
    neighbors = re.findall(r'^\d+\.\d+\.\d+\.\d+\s+\d+', output, re.MULTILINE)
    count = len(neighbors)
    passed = count >= expected_min
    return passed, f"{count} OSPF neighbor(s) found (expected >= {expected_min})"


def validate_nat_translations(output: str):
    # "show ip nat translations" prints one line per active translation;
    # a completely empty table (just the header, or no output) means NAT isn't translating.
    lines = [l for l in output.splitlines() if l.strip() and not l.strip().startswith("Pro ")]
    count = len(lines)
    passed = count > 0
    return passed, f"{count} active NAT translation(s) found"


def validate_etherchannel(output: str):
    # Looks for a Port-channel group in an "up" / bundled state (SU flag in IOS output,
    # e.g. "Po1(SU)"). No whitespace between the port-channel name and its flag in
    # real IOS output, so the pattern must not allow anything to intervene.
    passed = bool(re.search(r'Po\d+\(SU\)', output))
    return passed, "Port-channel bundled and up (SU)" if passed else "No bundled/up Port-channel found"


def validate_access_lists_present(output: str):
    passed = "Standard IP access list" in output or "Extended IP access list" in output
    return passed, "ACLs present" if passed else "No ACLs found in output"


def validate_nonempty(output: str):
    passed = bool(output.strip())
    return passed, "Command returned output" if passed else "Command returned no output"


# ---------------------------------------------------------------------------
# Per-device check definitions -- mirrors the lab readme's own verification
# list, scoped to which device each check actually applies to.
# ---------------------------------------------------------------------------

DEVICE_CHECKS = {
    "BORDER": [
        Check("NAT translations active", "show ip nat translations", validate_nat_translations),
        Check("ACLs present", "show access-lists", validate_access_lists_present),
        Check("OSPF neighbors up", "show ip ospf neighbor", validate_ospf_neighbors),
    ],
    "L3SW1": [
        Check("OSPF neighbors up", "show ip ospf neighbor", validate_ospf_neighbors),
        Check("EtherChannel bundled", "show etherchannel summary", validate_etherchannel),
    ],
    "L3SW2": [
        Check("OSPF neighbors up", "show ip ospf neighbor", validate_ospf_neighbors),
        Check("EtherChannel bundled", "show etherchannel summary", validate_etherchannel),
    ],
    "SW1": [
        Check("Spanning-tree responds", "show spanning-tree", validate_nonempty),
    ],
    "SW2": [
        Check("Spanning-tree responds", "show spanning-tree", validate_nonempty),
    ],
    "ISP1": [
        Check("Interfaces respond", "show ip interface brief", validate_nonempty),
    ],
    "ISP2": [
        Check("Interfaces respond", "show ip interface brief", validate_nonempty),
    ],
    "GOOGLE": [
        Check("Interfaces respond", "show ip interface brief", validate_nonempty),
    ],
}


def load_inventory(path: str) -> dict:
    if yaml is None:
        print("PyYAML is required: pip install pyyaml", file=sys.stderr)
        sys.exit(2)
    with open(path) as f:
        return yaml.safe_load(f)


def run_device_checks(name: str, conn_params: dict) -> DeviceResult:
    result = DeviceResult(device=name)
    checks = DEVICE_CHECKS.get(name.upper(), [])
    if not checks:
        result.error = f"No check definitions for device '{name}' (add one to DEVICE_CHECKS)"
        return result

    try:
        conn = ConnectHandler(**conn_params)
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as e:
        result.reachable = False
        result.error = str(e)
        return result

    try:
        for check in checks:
            output = conn.send_command(check.command)
            passed, detail = check.validator(output)
            result.checks.append((check.name, passed, detail))
    finally:
        conn.disconnect()

    return result


def main():
    parser = argparse.ArgumentParser(description="Run the lab's documented verification checklist against real devices.")
    parser.add_argument("--inventory", required=True, help="YAML file listing devices and connection params (see devices.example.yaml)")
    parser.add_argument("--device", help="Only check this one device (matches names in DEVICE_CHECKS)")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON instead of a text report")
    args = parser.parse_args()

    inventory = load_inventory(args.inventory)
    devices = inventory.get("devices", {})

    if args.device:
        if args.device not in devices:
            print(f"'{args.device}' not found in inventory", file=sys.stderr)
            sys.exit(2)
        devices = {args.device: devices[args.device]}

    results = []
    for name, conn_params in devices.items():
        results.append(run_device_checks(name, conn_params))

    overall_pass = True

    if args.json:
        out = []
        for r in results:
            out.append({
                "device": r.device,
                "reachable": r.reachable,
                "error": r.error,
                "checks": [{"name": n, "passed": p, "detail": d} for n, p, d in r.checks],
            })
            if not r.reachable or any(not p for _, p, _ in r.checks):
                overall_pass = False
        print(json.dumps(out, indent=2))
    else:
        for r in results:
            print(f"\n=== {r.device} ===")
            if not r.reachable:
                print(f"  ❌ UNREACHABLE: {r.error}")
                overall_pass = False
                continue
            if r.error:
                print(f"  ⚠️  {r.error}")
                continue
            for name, passed, detail in r.checks:
                icon = "✅" if passed else "❌"
                print(f"  {icon} {name}: {detail}")
                if not passed:
                    overall_pass = False

        print("\n" + "=" * 50)
        print("✅ All checks passed" if overall_pass else "❌ One or more checks failed")

    sys.exit(0 if overall_pass else 1)


if __name__ == "__main__":
    main()
