from scapy.arch import get_if_addr

BROADCAST_MAC= "FF:FF:FF:FF:FF:FF"
INTERFACE="以太网"
LOCAL_IPv4=get_if_addr("以太网")
LOCAL_MAC="98:FA:9B:9E:B3:52"