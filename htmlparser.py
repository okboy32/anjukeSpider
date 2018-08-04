import datetime

from bs4 import BeautifulSoup
from models import ZuFangInfo
class HtmlParser(object):

    def __init__(self):
        self.soup = None
        self.city = None
        self.id = []

    def parse(self, html):
        self.soup = None
        self.soup = BeautifulSoup(html, 'html.parser')

    def getpage(self):
        pages = self.soup.find('div',class_='multi-page').find_all('a')
        pages_url = [page['href'] for page in pages]
        return pages_url

    def getcity(self):
        city = self.soup.find('div', id='switch_apf_id_5').contents[0].replace('\n','').replace(" ", '')
        self.city = city
        return city

    def get_zu_items_data(self):
        zu_items = self.soup.find_all('div', class_='zu-itemmod')
        return len([ZuFangInfo(**self.__get_zu_item_data(zu_item)) for zu_item in zu_items])

    def __get_zu_item_data(self,zu_item):
        zu_info = zu_item.find('div', class_='zu-info')
        href = zu_info.find('h3').find('a')['href']
        id = href.split('/')[-1]
        title = zu_info.find('h3').get_text().replace('\n', '').replace(' ', '')
        house_type = zu_info.find('p', class_='tag').contents[::2]
        address = [s.replace(' ', '') for s in zu_info.find('address').get_text().split('\n')]
        keywords = [ keyword.get_text() for keyword in zu_info.find('p', class_='clearfix').find_all()]
        zu_side = zu_item.find('div', class_='zu-side')
        price = zu_side.find('strong').get_text()
        unit = zu_side.find('p').get_text()
        return {
            'id': id,
            'title': title,
            'house_type': house_type,
            'address': address,
            'keywords': keywords,
            'price': price,
            'unit': unit,
            'city': self.city,
            'href': href,
            'add_time': datetime.datetime.now().date()
        }
