from scapy.all import sr1, IP, DNS, DNSQR, DNSRR, UDP, ICMP
import requests
import logging

"""
- Try to download consensus
    x Contact hard coded authorities
     check if 9 authorities and log its names. warning if they're not 9
     check also bridge authority
- ping authorities
- traceroutes authorities (TCP, UDP, ICMP)

"""


class TestDirAuth:
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

    def get_consensus(self):
        ip = self.ip
        url = self.url
        cfile = self.consensus_file
        try:
            self.consensus = requests.get("http://{}{}".format(ip, url), headers=self.headers, stream=True)
            if self.consensus.status_code in [200, 201, 202, 304]:
                with open(cfile, 'wb') as f:
                    for chunk in self.consensus.iter_content(chunk_size=1024):
                        if chunk:  # filter out keep-alive new chunks
                            f.write(chunk)
            else:
                self.log.error(
                    'Status code error: URL {} return an status code {}'.format(url, self.consensus.status_code))
        except requests.exceptions.Timeout as terr:
            self.log.error('Timeout error: URL {}, exception {})'.format(url, terr))
        except requests.exceptions.TooManyRedirects as tmrerr:
            self.log.error('TooManyRedirects error: URL {}, exception {}'.format(url, tmrerr))
        except requests.exceptions.RequestException as gerr:
            self.log.error('General exception: URL {}, exception {}'.format(url, gerr))

    def test_dir_auth(self, ip, url, cfile):
        self.ip = ip
        self.url = url
        self.consensus_file = cfile
        self.get_consensus()
        # Check consensus
        # Check if structure is consistent
        # Get all dir auth and check if i have them all
        # Get all nodes
        # Check differences between consensus?
