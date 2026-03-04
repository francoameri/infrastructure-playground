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

---

## ⚙️ Config Highlights

### OSPF (Internal)
```plaintext
router ospf 10
 network 100.100.0.0 0.0.0.3 area 0
 network 100.200.0.0 0.0.0.3 area 0
 default-information originate
```

### Static Routing (Edge to ISPs/Google)
```plaintext
ip route 0.0.0.0 0.0.0.0 172.0.0.1   ! toward ISP1
ip route 10.0.0.0 255.255.255.252 172.0.0.6   ! toward Google via ISP2
ip route 172.0.0.12 255.255.255.252 172.0.0.14 ! toward SP2
```

### ACLs (Border Router)
```plaintext
access-list 100 deny ip 192.168.100.0 0.0.0.255 any
access-list 100 deny ip 100.100.0.0 0.0.0.3 any
access-list 100 permit ip any any
interface g0/0
 ip access-group 100 out

access-list 200 deny ip 192.168.200.0 0.0.0.255 any
access-list 200 deny ip 100.200.0.0 0.0.0.3 any
access-list 200 permit ip any any
interface g0/1
 ip access-group 200 out
```

### NAT (Static)
```plaintext
ip nat inside source static 192.168.100.10 172.0.0.2
ip nat inside source static 192.168.200.20 172.0.0.10

interface g0/0
 ip nat inside
interface s0/0/0
 ip nat outside

interface g0/1
 ip nat inside
interface s0/0/1
 ip nat outside
```

### VLANs & Trunking
```plaintext
vlan 100
 name Office
vlan 200
 name Administration

interface range g0/1 - 2
 switchport mode trunk
 switchport trunk allowed vlan 100,200
```

### EtherChannel (LACP)
```plaintext
interface range g0/3 - 4
 channel-group 1 mode active
!
interface port-channel 1
 switchport mode trunk
 switchport trunk allowed vlan 100,200
```

🧪 Verification Commands
```
- ping 10.0.0.2 → reach Google server from Office or Administration VLAN
- show ip ospf neighbor → confirm adjacency between BORDER, L3SW1, L3SW2
- show ip route → check static + OSPF routes
- show access-lists → confirm ACL hits
- show etherchannel summary → verify LACP bundle
```
