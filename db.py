import pymysql
from setting import PASSWORD, PORT, HOST, USER, DB as DB_

class DB:
    def __init__(self):
        self.conn = pymysql.connect(host=HOST, port=PORT, user=USER, password=PASSWORD, db=DB_)
        self.cur = self.conn.cursor()
        self.SQL = {}
        self.f = open('sql', 'w', encoding='utf-8')
        self.id_list= []

    def createSQL(self, name, value):
        if value is None:
            return
        if isinstance(value, dict):
            self.__createSQL_dict(name, **value)
        if isinstance(value, list):
            self.__createSQL_list(name, value)

    def __createSQL_dict(self, name, **kwargs):
        if self.__hasDuplication(kwargs['id']):
            return
        if len(kwargs) == 0:
            return
        keys = '(' + ' ,'.join(kwargs.keys()) + ')'
        values = "('"  +"' ,'".join([str(i).replace("'", '"') for i in kwargs.values()]) + "')"
        this = self.SQL.get(name, None)
        if this is None:
            self.SQL[name] = dict()
            self.SQL[name]['values'] = []
            self.SQL[name]['keys'] = keys
        if self.SQL[name]['keys'] == keys:
            self.SQL[name]['values'].append(values)

    def __createSQL_list(self, name, values):
        if len(values) == 0:
            return
        keys = "('" + "' ,'".join(values[0].keys()) + "')"
        this_keys = self.SQL.get(name, None)['keys']
        if this_keys is None:
            self.SQL[name]['keys'] = keys
        if this_keys == keys is self.SQL[name]:
            for value in values:
                if self.__hasDuplication(value['id']):
                    continue
                value = '(' + ' .'.join(value.values()) + ")"
                self.SQL[name]['values'].append(value)

    def __createTable(self, name, keys):
        pass

    def commit(self):
        for k, v in self.SQL.items():
            self.f.write('insert into %s ' %k)
            self.f.write(v['keys'])
            self.f.write('values\n')
            values_str = ''
            for value in v['values']:
                values_str += value + ',\n'
            self.f.write(values_str[:-2] + ';\n')
        self.SQL = {}
        self.conn.commit()

    def save(self):
        self.f.close()
        self.cur.close()
        self.conn.close()

    def __hasDuplication(self, id):
        if id in self.id_list:
            return True
        else:
            self.id_list.append(id)
            return False


db = DB()


