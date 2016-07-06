import requests
import logging
import json


class TestWebsite:
    def __init__(self):
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) ' \
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
        self.headers = {
            'User-Agent': self.user_agent
        }
        self.log = logging.getLogger('TestWebsite')
        self.website = None

    def json_to_dict(self, json_string):
        try:
            new_dict = json.loads(json_string)
        except Exception as err:
            self.log.error("Exception received while transforming json to dict: {}".format(err))
            return None
        return new_dict

    def basic_get_req(self, url):
        self.website = requests.get(url, headers=self.headers)

    def search_keywords_content(self, words):
        failed_words = []
        for w in words:
            if w not in self.website.content:
                failed_words.append(w)

        if len(failed_words):
            self.log.warning("Failed words for website {}: {}".format(self.website.url, failed_words))
            return False
        else:
            self.log.info("All words found for website {}".format(self.website))
            return True

    def test_website(self, web_params):
        """
        Main process
        :param web_params: a dict
        :return:
        """
        necessary_params = ['url', 'words']
        not_found_params = []

        for w in necessary_params:
            if w not in web_params:
                not_found_params.append(w)

        if len(not_found_params):
            self.log.error("Parameters not found in website dict: {} (dict: {})".format(not_found_params, web_params))
            return False
        else:
            self.basic_get_req(web_params['url'])
            return self.search_keywords_content(web_params['words'])








