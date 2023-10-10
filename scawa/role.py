
import globvar
class Role():
    def __init__(self, mac=globvar.LOCAL_MAC, ip=globvar.LOCAL_IPv4, port=None):
        self.mac = mac
        self.ip=ip
        self.port=port

