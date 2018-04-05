from pymongo import MongoClient  # Database connector
from urllib.parse import urlparse
import datetime
import api


class DataModels:

    def __init__(self):
        self.today = datetime.date.today()
        self.collection = self.mongo_connect()
        if self.check_list() is False:
            self.delete_coin_list()
            self.insert_coin_list()

    @staticmethod
    def mongo_connect():
        '''
            for connect to mongodb heroku
        '''

        MONGO_URL = "mongodb://lexion13:1211333s@ds033096.mlab.com:33096/heroku_w8gqb97v"
        if MONGO_URL:
            # Get a connection
            connection = MongoClient(MONGO_URL)
            # Get the database
            db = connection[urlparse(MONGO_URL).path[1:]]
        else:
            # Not on an app with the MongoHQ add-on, do some localhost action
            connection = MongoClient('localhost', 27017)
            db = connection.cryptocurrency

        collection = db['coin_type']
        return collection

    def check_list(self):
        if self.collection.count() == 0:
            return False
        else:
            result = self.collection.find_one({'date': self.today.strftime('%Y-%m-%d')})
            if result is None:
                return False
            else:
                return True

    def insert_coin_list(self):

        coins_list_json = api.get_list_all()

        for key, value in coins_list_json['Data'].items():
            if 'ImageUrl' in value:
                image = os.path.basename(value.get('ImageUrl'))
            else:
                image = value.get('ImageUrl')
            self.collection.insert_one({'date': self.today.strftime('%Y-%m-%d'), 'coin': key, 'image': image, 'name': value['Name']})

        return True

    def delete_coin_list(self):
        self.collection.remove()
        return True

    def get_coin_list(self, offset, limit):
        currency = self.collection.find().skip(offset).limit(limit)
        return currency

    def get_one(self, coin):
        return self.collection.find_one({'coin': coin})

