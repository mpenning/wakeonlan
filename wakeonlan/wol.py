from struct import pack
import logging
import time
import sys
import os
# Thanks Mike DiSimone...
#    http://stackoverflow.com/a/6705359/667301
sys.path.insert(0, os.path.join(os.path.dirname(sys.argv[0]), "scapy"))
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import Ether, IP, IPv6, UDP, Raw, sendp


"""
Send packets with scapy, which conform to AMD's Magic Packet (WOL) spec
Copyright (C) 2014  David Michael Pennington

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

## Docstring props: http://stackoverflow.com/a/1523456/667301
__version_tuple__ = (0,0,2)
__version__ = '.'.join(map(str, __version_tuple__))
__email__ = "mike /at\ pennington [dot] net"
__author__ = "David Michael Pennington <{0}>".format(__email__)
__copyright__ = "2014-{0}, {1}".format(time.strftime('%Y'), __author__)
__license__ = "GPLv2"
__status__ = "Production"

class WOL(object):
    def __init__(self, target_mac="", intf='eth0'):
        self.intf = intf
        self.target_mac = target_mac

        self.ETH_BROADCAST = "ff:ff:ff:ff:ff:ff"
        self.wol_payload = self.build_wol_payload(mac_str=target_mac)

    def build_wol_payload(self, mac_str=""):
        ## WOL PAYLOAD: FFFFFFFFFFFF + 16 repetitions of the computer mac

        # Pack the broadcast address in network byte order
        bcast_str = self.ETH_BROADCAST
        bcast_bin_list = [pack("!B", int(ii, 16)) for ii in bcast_str.split(':')]
        bcast_packed = b''.join(bcast_bin_list)

        # Pack the mac-address in network byte order
        mac_bin_list = [pack("!B", int(ii, 16)) for ii in mac_str.split(':')]
        mac_packed = b''.join(mac_bin_list)

        # Build the payload
        payload = b''.join([bcast_packed, 16*mac_packed])
        return payload

    def raw(self):
        # Ethertype 0x0842 + WOL Payload
        return sendp([Ether(type=int('0842', 16), dst=self.ETH_BROADCAST) / Raw(load=self.wol_payload)], iface=self.intf)

    def udp4(self):
        # UDP port 9 + WOL Payload
        return sendp([Ether(dst=self.ETH_BROADCAST) / IP(dst='255.255.255.255') / UDP(sport=32767, dport=9)/ Raw(load=self.wol_payload)], iface=self.intf)

    def udp6(self):
        # UDP port 9 + WOL Payload
        return sendp([Ether() / IPv6(dst='ff02::1') / UDP(sport=32767, dport=9)/ Raw(load=self.wol_payload)], iface=self.intf)

if __name__=="__main__":
    wol = WOL("00:30:1b:bc:a7:d7", intf="eth0")
    wol.raw()
    wol.udp4()
    wol.udp6()
