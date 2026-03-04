# network-playground
A small, reproducible Packet Tracer lab showcasing VLANs, basic WLAN (WLC/AP) configuration, static and OSPF routing, ACL, NAT and simple automation examples. All device configurations are sanitized to remove any customer-identifying data; lab logic is preserved so you can open the Packet Tracer file and reproduce the exercises locally.

What this repository demonstrates
- VLAN design and switch trunking essentials
- Basic WLC / AP configuration and WLAN verification steps
- Static and OSPF Routing
- ACL and NAT
- Exported device configs (sanitized) and example show outputs
- How to reproduce tests and verify connectivity in the lab

Quickstart (one line)
- Download and open pkt/topology.pkt with Cisco Packet Tracer (recommended version: Packet Tracer 8.x).
- Follow the steps in docs/lab-instructions.md to run verification commands and tests.

Files and folders
- pkt/topology.pkt — Packet Tracer lab file (sanitized)
- configs/ — sanitized running-config exports per device (switches, WLC, APs)
- docs/lab-instructions.md — step-by-step reproduction and verification commands
- docs/diagram.drawio.svg — editable topology diagram (also exported as PNG in screenshots/)
- screenshots/ — verification screenshots and expected outputs
- results/ — example outputs, short pcaps or logs (sanitized)
- README.md — this file

How to verify the lab (short checklist)
- Open pkt/topology.pkt in Packet Tracer.
- From a PC host, run ping to another host in the same VLAN. Expected: successful replies.
- From the switch CLI, run show vlan brief and show interface trunk to confirm VLAN assignments and trunking.
- From the WLC or AP (console in Packet Tracer), verify SSID assignment and client association.

Contact
Franco Ameri Sbraccia — github.com/francoameri — linkedin.com/in/fameri — famerisbraccia@gmail.com
