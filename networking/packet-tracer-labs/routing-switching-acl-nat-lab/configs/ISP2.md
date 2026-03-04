```plaintext
ISP2#show running-config 
Building configuration...

Current configuration : 878 bytes
!
version 15.1
no service timestamps log datetime msec
no service timestamps debug datetime msec
no service password-encryption
!
hostname ISP2
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
license udi pid CISCO2901/K9 sn FTX1524VX2F-
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
 no ip address
 duplex auto
 speed auto
 shutdown
!
interface GigabitEthernet0/1
 no ip address
 duplex auto
 speed auto
 shutdown
!
interface Serial0/0/0
 ip address 172.0.0.10 255.255.255.252
 clock rate 2000000
!
interface Serial0/0/1
 ip address 172.0.0.13 255.255.255.252
!
interface Vlan1
 no ip address
 shutdown
!
ip classless
ip route 10.0.0.0 255.255.255.252 Serial0/0/0 
ip route 0.0.0.0 0.0.0.0 Serial0/0/0 
ip route 0.0.0.0 0.0.0.0 Serial0/0/1 
!
ip flow-export version 9
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
end
```
