import os

import urlmanager
import htmldownloader
import htmlparser
from db import db
from setting import citys

class anjukeSpider:

    def __init__(self):
        self.root_url = r'https://sh.zu.anjuke.com/?pi=baidu-cpchz-sh-hexin1&kwid=63651556880&utm_term=%E7%A7%9F%E6%88%BF'
        self.htmlDownloader = htmldownloader.HtmlDownloader()
        self.urlmanager = urlmanager.UrlManager()
        self.anjukeParser = htmlparser.HtmlParser()
        self.log = open('log.txt', 'w', encoding='utf-8')

    def craw(self):

        for name, abbr in citys.items():
            page = 0
            city_url = 'https://%s.zu.anjuke.com/fangyuan/' % abbr
            self.urlmanager.add_new_url(city_url)
            count = 0
            print('开始爬 %s …' %name)
            try:
                while self.urlmanager.has_url():
                    page += 1
                    url = self.urlmanager.get_url()
                    html = self.htmlDownloader.downloadhtml(url, json=False)
                    if not os.path.exists('./data/%s' % name):
                        os.mkdir('./data/%s' % name)
                    with open('./data/%s/page%d.html' %(name, page), 'w', encoding='utf-8') as f:
                        f.write(html)
                    self.anjukeParser.parse(html)
                    urls = self.anjukeParser.getpage()
                    city = self.anjukeParser.getcity()
                    if city != name:
                         break
                    self.urlmanager.add_new_url(urls)
                    count += self.anjukeParser.get_zu_items_data()
                    db.commit()
                    print('当前正在 [%s] 爬取第%d' %(name, page) + '个页面' + '已爬取%s条' %count)
            except Exception as e:
                print(e)
                print(self.urlmanager.get_url())
                log_str = '爬取失败 [%s] %d' %(name, page)
                print(log_str)
                self.log.write(log_str)

        self.log.close()

if __name__ == '__main__':
    spider = anjukeSpider()
    spider.craw()