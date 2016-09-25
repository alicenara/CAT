from scapy.all import sr1, IP, DNS, DNSQR, DNSRR, UDP, ICMP
import logging

"""
To test bridges, we need to try get one and also do obfs2 - 3 - 4 handshakes to detect DPI.
"""


class TestBridge:
    def __init__(self):
        self.ip = None
        self.url = None
        self.consensus = None
        self.consensus_file = None
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) ' \
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
        self.headers = {
            'User-Agent': self.user_agent
        }
        self.log = logging.getLogger('C_TestDirectoryAuthority')

    def ping_dir_aut(self, ip):
        ping_res = None
        try:
            ping_res = sr1(IP(dst=ip, ttl=60)/ICMP())
        except Exception as e:
            self.log.error("Exception when ping IP {}: {}".format(ip, e))
            return False

        if ping_res is None:
            self.log.error("Ping to IP {} returned None".format(ip))
        elif ping_res[ICMP].type == "echo-reply":
            self.log.debug("Ping successfully done to IP {}".format(ip))
            return True
        else:
            self.log.warning("Could not reach IP {}, {}".format(ip, ping_res[ICMP].type))
        return False