import requests


class HtmlDownloader(object):

    def __init__(self):
        self.header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
        }

    def downloadhtml(self, url, json=False):
        response = requests.get(url, headers=self.header)
        if json:
            return response.json
        else:
            return response.text