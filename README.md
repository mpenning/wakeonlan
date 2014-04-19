## Wake On LAN

### Introduction

This library sends packets with [scapy], which conform to [AMD's Magic Packet spec].  When a computer is in sleep mode, has the correct hw / config, and plugged into the network, a packet arriving on the NIC will trigger a process to wake it from its sleep mode.

Specifically, three packets are implemented:

 - `udp4()`: send the WOL event as an IPv4 UDP broadcast packet, destination port 9
 - `raw()`: send the WOL event as a raw ethernet packet to Ethertype 0x0847
 - `udp6()`: send the WOL event as an IPv6 UDP packet to the all-hosts group (`ff02::1`), destination port 9.  `ff02::1` was recommended by the [Microsoft DLNA Interoperability guidelines](http://msdn.microsoft.com/en-us/library/ff361877.aspx)

Let's be clear, any one of these packets are not guaranteed to wake a computer up; a lot depends on your specific hardware.

I've personally had the most success with `udp4()` and `raw()`; I have never even seen a computer wake up with `udp6()`.  However, I saw a [question on the internet](http://networkengineering.stackexchange.com/q/7453/775) about using IPv6 to trigger Wake on LAN, and I wanted to try it out.

There are plenty of python implementations for WOL, but I couldn't find any that built all three packets (raw ethernet, IPv4 and IPv6).  As an exercise, I decided to try my own with [scapy].

### Usage

It's pretty simple... build an instance of the `WOL()` object with the target mac address, and call whichever WOL function you like on the mac; you can optionally specify the egress interface as well (the default is `eth0`).

I bundled [scapy] with the module so it's mostly plug-and-play, assuming you have python2 on your linux machine and root priviledges.

Call this script as root to send all three WOL packets to it...

    import WOL
    wol = WOL("00:30:1b:b0:f7:7d", intf="eth0")
    wol.raw()
    wol.udp4()
    wol.udp6()

[scapy]: http://www.secdev.org/projects/scapy/
[AMD's Magic Packet spec]: http://support.amd.com/TechDocs/20213.pdf#search=20213
