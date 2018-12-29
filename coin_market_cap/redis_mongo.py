# -*- coding: utf-8 -*-
import json
import redis  # pip install redis
from pymongo import MongoClient
import logging


class DataLayerMongo(object):

    MONGO_SERVER = ''

    def __init__(self):
        # the db connection var
        self.main_db = MongoClient(self.MONGO_SERVER)

    def update_coin_market_cap_data(self, db_name, collection_name, data):
        """
        通过unique_id向mongodb相应数据库集合中更新插入一条数据
        :param db_name: 数据库名字 string
        :param collection_name: 集合名字 string
        :param data: 插入的数据 dict
        :return: 更新插入成功返回True 失败返回False bool
        """
        db = self.main_db[db_name][collection_name]
        # 将数据存入mongodb数据库
        try:
            logging.debug('[{}][{}]: 正在更新插入数据 {}: {}'.format(db_name, collection_name, 'unique_id', data['unique_id']))
            db.update_one(
                {'unique_id': data['unique_id']},
                {"$set": data},
                True
            )
            logging.debug('[{}][{}]: 数据更新插入成功: {}'.format(db_name, collection_name, data))
            return True
        except Exception as e:
            logging.critical(e)
            return False


class RedisToMongo(object):
    """
    Save data from redis to mongo
    """
    def __init__(self):
        # 指定redis数据库信息
        self.rediscli = redis.StrictRedis(host='39.107.115.117', port=6379, db=0)
        self.db = DataLayerMongo()

    def start(self):

        while True:
            source, data = self.rediscli.blpop(["coin_market_cap:items"])  # 从redis里提取数据
            item = json.loads(data.decode('utf-8'))  # 把json转字典
            self.db.update_coin_market_cap_data('coin_market_cap', item['collection_name'], item)


if __name__ == '__main__':
    rtm = RedisToMongo()
    rtm.start()
