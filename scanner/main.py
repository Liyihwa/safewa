import socket
from .. import logwa
'''
    scanner是一个ip/port扫描器
'''


def scan_local_network():
    logwa.infof("localhost:{}", socket.gethostname())
    # ip_prefix = '.'.join(socket.gethostbyname(socket.gethostname()).split('.')[:-1])
    #
    # for i in range(1, 255):
    #     ip = f"{ip_prefix}.{i}"
    #     try:
    #         host_name = socket.gethostbyaddr(ip)[0]
    #         print(f"Found IP: {ip} ({host_name})")
    #     except socket.herror:
    #         pass
if __name__=='__main__':
    scan_local_network()