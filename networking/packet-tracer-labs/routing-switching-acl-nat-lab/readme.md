## 🧩 Network Playground  

A small, reproducible **Packet Tracer lab** showcasing:  
- 🖧 **VLAN design** and switch trunking essentials  
- 📡 **Basic WLAN setup** with WLC/AP configuration and verification steps  
- 🛣️ **Static & OSPF routing** for connectivity across subnets  
- 🔒 **ACL & NAT examples** to control and translate traffic  
- ⚙️ **Simple automation snippets** for repeatable tasks  
- 🗂️ **Sanitized configs & outputs** so you can reproduce the exercises locally without customer data  

---

### 🚀 Quickstart  
1. ⬇️ Download and open `pkt/topology.pkt` with Cisco Packet Tracer (recommended: v8.x).  
2. 📖 Follow the steps in `docs/lab-instructions.md` to run verification commands and tests.  

---

### 📂 Files & Folders  
- `pkt/topology.pkt` — main Packet Tracer lab file (sanitized)  
- `README.md` — this file  

---

### ✅ How to Verify the Lab  
- 🖥️ From a PC host, run `ping` to another host in the same VLAN → expected: successful replies.  
- 🔍 On the switch CLI, run `show vlan brief` and `show interface trunk` → confirm VLAN assignments and trunking.  
- 📡 On the WLC/AP console, verify SSID assignment and client association.  

---

### 📬 Contact  
Franco Ameri Sbraccia  
- 🌐 [GitHub](https://github.com/francoameri)  
- 💼 [LinkedIn](https://linkedin.com/in/fameri)  
- ✉️ famerisbraccia@gmail.com  
