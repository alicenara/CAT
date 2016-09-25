from scapy.all import sr1, IP, DNS, DNSQR, DNSRR, UDP, ICMP
import requests
import logging
import json


"""
What it should do:
- Probe www.torproject.org:
   x Try to download index page with HTTP GET with user agent legit.
   x Check IP to detect DNS poisoning. <- same IP all countries?
   x Try to reach other DNSs (like 8.8.8.8)
- Probe tor mirrors (some without 'tor' in domain name)
- Verify that port 443 of torproject is reachable
- Probe also bridges (bridges.torproject.org)
  
"""


class TestWebsite:
    def __init__(self):
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) ' \
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
        self.headers = {
            'User-Agent': self.user_agent
        }
        self.log = logging.getLogger('C_TestWebsite')
        self.website = None
        self.ip = None
        self.url = None
        self.words = None
        self.original_ip = None

    def json_to_dict(self, json_string):
        try:
            new_dict = json.loads(json_string)
        except Exception as err:
            self.log.error("Exception received while transforming json to dict: {}".format(err))
            return None
        return new_dict

    def basic_get_req(self, url=None):
        url = self.url if url is None else url
        try:
            self.website = requests.get(url, headers=self.headers, stream=True)
            self.ip = self.website.raw._connection.sock.getpeername()[0]
            if self.website.status_code in [200, 201, 202, 304]:
                return True
            else:
                self.log.error('Status code error: URL {} return an status code {}'.format(url, self.website.status_code))
        except requests.exceptions.Timeout as terr:
            self.log.error('Timeout error: URL {}, exception {})'.format(url, terr))
        except requests.exceptions.TooManyRedirects as tmrerr:
            self.log.error('TooManyRedirects error: URL {}, exception {}'.format(url, tmrerr))
        except requests.exceptions.RequestException as gerr:
            self.log.error('General exception: URL {}, exception {}'.format(url, gerr))
        self.website = None
        return False

    def check_ip(self, url=None, original_ip=None, neutral_dns_ip="8.8.8.8"):
        url = self.url if url is None else url
        original_ip = self.original_ip if original_ip is None else original_ip

        if self.ip == original_ip:
            self.log.info('IP is the same, DNS poisoning NOT detected (url: {})'.format(url))
            return True
        else:
            self.log.warning('Different IP detected: {}'.format(self.ip))
            dns_search = None
            try:
                dns_search = sr1(IP(dst=neutral_dns_ip) / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname=url)), verbose=0)
            except OSError as oserr:
                self.log.error('Error while trying to connect to DNS for URL {}: {}'. format(url, oserr))
                return False
            except Exception as exerr:
                self.log.error('Unexpected error in DNS check, URL {}: {}'.format(url, exerr))
                return False

            if dns_search is None or dns_search[DNSRR].rrname == '.':
                self.log.warning('URL ({}) not found in neutral DNS.'.format(url))
                return False

            obtained_ip = dns_search[DNSRR].rdata
            if original_ip == obtained_ip:
                self.log.warning('Neutral DNS returns original IP - DNS poisoning detected for URL {}'.format(url))
            elif self.ip == obtained_ip:
                self.log.warning('Neutral DNS returns given IP - maybe original IP not correct for URL {}'.format(url))
                return True
            else:
                self.log.warning('Unexpectedly, given IP is totally different: URL {} - IP {}'.format(url, obtained_ip))
            return False

    def search_keywords_content(self, words=None):
        words = self.words if words is None else words
        failed_words = []
        for w in words:
            if w not in self.website.text:
                failed_words.append(w)

        if len(failed_words):
            self.log.warning("Failed words for website {}: {}".format(self.website.url, failed_words))
            return False
        else:
            self.log.debug("All words found for website {}".format(self.website.url))
            return True

    def test_website(self, web_params):
        """
        Main process
        :param web_params: a dict
        :return:
        """
        necessary_params = ['url', 'words', 'ip']
        not_found_params = []

        for w in necessary_params:
            if w not in web_params:
                not_found_params.append(w)

        if len(not_found_params):
            self.log.error("Some parameters not found in received arguments: "
                           "missing parameters = {}, received parameters = {}".format(not_found_params, web_params))
            return False
        else:
            self.url = web_params['url']
            self.words = web_params['words']
            self.original_ip = web_params['ip']
            if self.basic_get_req():
                return self.search_keywords_content()
            else:
                return self.check_ip()








