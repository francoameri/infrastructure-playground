```plaintext
BORDER#show running-config 
Building configuration...

Current configuration : 1545 bytes
!
version 15.1
no service timestamps log datetime msec
no service timestamps debug datetime msec
no service password-encryption
!
hostname BORDER
!
!
!
!
!
!
!
!
no ip cef
no ipv6 cef
!
!
!
!
license udi pid CISCO2901/K9 sn FTX1524FCEY-
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
interface GigabitEthernet0/0
 ip address 100.200.0.1 255.255.255.252
 ip access-group 1 out
 ip nat inside
 duplex auto
 speed auto
!
interface GigabitEthernet0/1
 ip address 100.100.0.1 255.255.255.252
 ip access-group 2 out
 ip nat inside
 duplex auto
 speed auto
!
interface Serial0/0/0
 ip address 172.0.0.1 255.255.255.252
 ip nat outside
!
interface Serial0/0/1
 ip address 172.0.0.14 255.255.255.252
 ip nat outside
 clock rate 2000000
!
interface Vlan1
 no ip address
 shutdown
!
router ospf 10
 router-id 8.8.8.8
 log-adjacency-changes
 network 100.100.0.0 0.0.0.3 area 0
 network 100.200.0.0 0.0.0.3 area 0
 default-information originate
!
ip nat inside source static 100.200.0.1 172.0.0.1 
ip nat inside source static 100.100.0.1 172.0.0.14 
ip classless
ip route 172.0.0.4 255.255.255.252 Serial0/0/0 
ip route 172.0.0.8 255.255.255.252 Serial0/0/1 
ip route 0.0.0.0 0.0.0.0 Serial0/0/0 
ip route 0.0.0.0 0.0.0.0 Serial0/0/1 
!
ip flow-export version 9
!
!
access-list 1 deny 192.168.100.0 0.0.0.255
access-list 1 permit any
access-list 1 deny 100.100.0.0 0.0.0.3
access-list 2 deny 192.168.200.0 0.0.0.255
access-list 2 deny 100.200.0.0 0.0.0.3
access-list 2 permit any
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
end
```
