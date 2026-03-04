# 🧩 Enterprise Network Playground

A reproducible **Cisco Packet Tracer lab** showcasing real-world enterprise edge design:

- 🖧 **VLAN segmentation** (Office & Administration) with trunking
- 🛣️ **OSPF dynamic routing** inside the LAN (L3SW1, L3SW2, BORDER)
- 📡 **Static routing** toward ISP1, ISP2, Google, SP2
- 🔒 **ACLs** applied at the BORDER to enforce policy
- 🌐 **NAT** translating internal servers to public IPs
- ⚙️ **EtherChannel (LACP)** between distribution switches
- 🗂️ **Sanitized configs & outputs** so you can reproduce the exercises locally

---

## 🚀 Quickstart
1. ⬇️ Download and open `pkt/topology.pkt` with Cisco Packet Tracer (recommended: v8.x).  
   👉 If you don’t have Packet Tracer installed, see [Getting Packet Tracer Guide](../docs/getting-packet-tracer.md).
2. 📖 Follow the steps in `docs/lab-instructions.md` to run verification commands and tests.

---

## 🗺️ Topology & Networks
- **Network A (Office):** 192.168.100.0/24 (VLAN 100)
- **Network B (Administration):** 192.168.200.0/24 (VLAN 200)
- **L3SW2 ↔ BORDER:** 100.100.0.0/30
- **L3SW1 ↔ BORDER:** 100.200.0.0/30
- **BORDER ↔ ISP1:** 172.0.0.0/30
- **ISP2 ↔ Google:** 172.0.0.4/30, 172.0.0.8/30
- **BORDER ↔ SP2:** 172.0.0.12/30
- **Google Server:** 10.0.0.0/30

```plaintext

[Admini VLAN 200]---L3SW1---\
                             BORDER---ISP1---Google---ServerPT
[Office VLAN 100]---L3SW2---/        \                 /
                                   ISP2---Google-------
```

---

## ⚙️ Config Highlights

### OSPF (Internal)
```plaintext
- OSPF runs between L3SW1, L3SW2, BORDER.
- VLAN networks (A & B) are redistributed into OSPF.
- BORDER originates default route toward ISPs.
```

### Static Routing (Edge to ISPs/Google)
```plaintext
- Purpose: Simulates redundant ISP2 paths toward Google.
- Design: Static routes point to next‑hop addresses for load‑sharing or failover testing.
```

### ACLs (Border Router)
```plaintext
• 	ACL 100 (G0/0): Blocks Office VLAN (192.168.100.0/24) and transit link (100.100.0.0/30) from leaking out.
• 	ACL 200 (G0/1): Blocks Administration VLAN (192.168.200.0/24) and transit link (100.200.0.0/30).
• 	Policy Goal: Prevent internal addressing from being routed externally, while still allowing NAT‑translated traffic
```

### NAT (Static)
```plaintext
- Inside Local: 192.168.100.10 (Office Webserver in VLAN 100)
- Inside Global: 172.0.0.2 (Public IP advertised to ISPs)
This static NAT entry ensures the internal webserver is reachable from the outside world using its public IP.
```

### VLANs & Trunking
```plaintext
- OSPF runs between L3SW1, L3SW2, BORDER.
- VLAN networks (A & B) are redistributed into OSPF.
- BORDER originates default route toward ISPs.
```

### EtherChannel (LACP)
```plaintext
- Combines multiple physical links (Fa0/1, Fa0/2) into a single logical Port‑Channel.
- Provides higher aggregate bandwidth between distribution switches.
- Ensures redundancy — if one link fails, traffic continues over the remaining link(s).
- Acts as the trunk backbone carrying VLAN 100 (Office) and VLAN 200 (Administration) between L3SW1 and L3SW2.
- Improves stability and throughput for inter‑VLAN routing and OSPF adjacency.
- Simplifies management: the two physical interfaces are treated as one logical interface (Po1).
```

🧪 Verification Commands
```
- ping 10.0.0.2 → reach Google server from Office or Administration VLAN
- show ip ospf neighbor → confirm adjacency between BORDER, L3SW1, L3SW2
- show ip route → check static + OSPF routes
- show access-lists → confirm ACL hits
- show etherchannel summary → verify LACP bundle
- show ip nat translations → confirm NAT mappings.
- traceroute 10.0.0.2 → verify static route path via ISP2.
- show spanning-tree → confirm VLAN trunk stability
```

## 🎯 Learning Outcomes
- Practice edge ACL design to block RFC1918 leakage
- Configure static NAT for internal webserver publishing
- Observe OSPF adjacencies across distribution and border
- Test static routing toward multiple ISPs with redundancy
