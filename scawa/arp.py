from scapy.layers.l2 import Ether, ARP
from scapy.sendrecv import sendp
from role import *
import globvar


def arp_request(dst_ip, src=Role(mac=globvar.LOCAL_MAC, ip=globvar.LOCAL_IPv4), interface=globvar.INTERFACE):
    arp = Ether(src=src.mac, dst=globvar.BROADCAST_MAC) / ARP()  # 构造数据包
    arp[ARP].op = 1  # 设置为request
    arp[ARP].hwlen = 6
    arp[ARP].plen = 4
    arp[ARP].psrc = src.ip
    arp[ARP].hwsrc=src.mac
    arp[ARP].pdst = dst_ip

    response = sendp(arp, iface=interface)
    return arp, response


# 以src的身份告诉dst,src.ip的mac地址为src.mac
def arp_response(dst, src=Role(ip=globvar.LOCAL_IPv4, mac=globvar.LOCAL_MAC), interface=globvar.INTERFACE):
    arp = Ether(src=src.mac, dst=dst.mac) / ARP(hwdst=dst.mac,hwsrc=src.mac,pdst=dst.ip,psrc=src.ip)  # 构造数据包
    arp[ARP].op=2   # response
    arp[ARP].hwlen = 6
    arp[ARP].plen = 4
    response = sendp(arp, iface=interface)
    return arp, response
