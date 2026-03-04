```plaintext
GOOGLE#show running-config 
Building configuration...

Current configuration : 994 bytes
!
version 15.1
no service timestamps log datetime msec
no service timestamps debug datetime msec
no service password-encryption
!
hostname GOOGLE
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
license udi pid CISCO2901/K9 sn FTX152498TQ-
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
 ip address 10.0.0.1 255.255.255.252
 duplex auto
 speed auto
!
interface GigabitEthernet0/1
 no ip address
 duplex auto
 speed auto
 shutdown
!
interface Serial0/0/0
 ip address 172.0.0.9 255.255.255.252
!
interface Serial0/0/1
 ip address 172.0.0.6 255.255.255.252
 clock rate 2000000
!
interface Vlan1
 no ip address
 shutdown
!
ip classless
ip route 172.0.0.12 255.255.255.252 Serial0/0/0 
ip route 172.0.0.0 255.255.255.252 Serial0/0/1 
ip route 0.0.0.0 0.0.0.0 Serial0/0/1 
ip route 0.0.0.0 0.0.0.0 Serial0/0/0 
ip route 10.0.0.0 255.255.255.252 GigabitEthernet0/0 
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
