from db import db
class BaseItem:

    def __init__(self, **kwargs):
        kwargs = self.validate(**kwargs)
        for k, v in kwargs.items():
            self.__setattr__(k,v)
        self.save()

    def validate(self, **kwargs):
        pass


    def save(self):
        db.createSQL(self.__class__.__name__.lower(), self.__dict__)

class ZuFangInfo(BaseItem):

    id = ''
    href = ''
    title = ''
    house_type = ''
    address = ''
    keywords = ''
    price = ''
    unit = ''
    area = ''
    district = ''
    size = ''
    loc = ''
    publisher = ''
    add_time = ''

    def validate(self,**kwargs):
        attrs = kwargs
        attrs['address'] = ' '.join(attrs['address'])
        if attrs['address'][0] == ' ':
            attrs['address'] = attrs['address'][1:]
        try:
            attrs['district'] = attrs['address'].split(' ')[1].split('-')[0]
            attrs['area'] = attrs['address'].split(' ')[0]
        except:
            attrs['district'] = attrs['area'] = ''
        try:
            attrs['house_type'] = [s.replace('\n', '').replace(' ','') for s in attrs['house_type']]
            if len(attrs['house_type']) == 4:
                attrs['house_type'], attrs['size'], attrs['loc'], attrs['publisher'] = attrs['house_type']
            else:
                attrs['house_type'], attrs['size'], attrs['loc'] = attrs['house_type']
        except:
            print(' '.join(attrs['house_type']).replace('  ', '').replace('\n', '').split(' '))
            print(attrs['house_type'])
            attrs['size'], attrs['loc'], attrs['publisher'] = '', '', ''
        attrs['keywords'] = ' '.join(attrs['keywords'])
        return attrs


class CityInfo(BaseItem):
    city = ''
    abbr = ''
    pages = ''



