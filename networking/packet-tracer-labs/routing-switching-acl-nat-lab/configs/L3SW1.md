```plaintext
L3SW1#show running-config 
Building configuration...

Current configuration : 1731 bytes
!
version 12.2(37)SE1
no service timestamps log datetime msec
no service timestamps debug datetime msec
no service password-encryption
!
hostname L3SW1
!
!
!
!
!
!
ip routing
!
!
!
!
!
!
!
!
!
!
!
!
!
!
!
spanning-tree mode pvst
!
!
!
!
!
!
interface Port-channel1
 switchport trunk allowed vlan 200
!
interface FastEthernet0/1
 switchport trunk allowed vlan 200
 channel-group 1 mode active
!
interface FastEthernet0/2
 switchport trunk allowed vlan 200
 channel-group 1 mode active
!
interface FastEthernet0/3
 shutdown
!
interface FastEthernet0/4
 shutdown
!
interface FastEthernet0/5
!
interface FastEthernet0/6
!
interface FastEthernet0/7
!
interface FastEthernet0/8
!
interface FastEthernet0/9
!
interface FastEthernet0/10
!
interface FastEthernet0/11
!
interface FastEthernet0/12
!
interface FastEthernet0/13
!
interface FastEthernet0/14
!
interface FastEthernet0/15
!
interface FastEthernet0/16
!
interface FastEthernet0/17
!
interface FastEthernet0/18
!
interface FastEthernet0/19
!
interface FastEthernet0/20
!
interface FastEthernet0/21
!
interface FastEthernet0/22
!
interface FastEthernet0/23
!
interface FastEthernet0/24
!
interface GigabitEthernet0/1
 switchport trunk allowed vlan 200
!
interface GigabitEthernet0/2
 no switchport
 ip address 100.200.0.2 255.255.255.252
 duplex auto
 speed auto
!
interface Vlan1
 no ip address
 shutdown
!
interface Vlan200
 mac-address 000c.cfda.3101
 ip address 192.168.200.1 255.255.255.0
!
router ospf 10
 router-id 7.7.7.7
 log-adjacency-changes
 network 100.200.0.0 0.0.0.3 area 0
 network 100.100.0.0 0.0.0.3 area 0
 network 192.168.200.0 0.0.0.255 area 0
!
ip classless
!
ip flow-export version 9
!
!
!
!
!
!
!
!
line con 0
!
line aux 0
!
line vty 0 4
 login
!
!
!
!
end
```
