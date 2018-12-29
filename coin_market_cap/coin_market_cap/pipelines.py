# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from coin_market_cap.items import CoinMarketCapBasicItem, CoinMarketCapDetailItem, CoinMarketCapChasrtsItem, CoinMarketCapHistoricalDataItem, CoinMarketCapDominanceItem


class CoinMarketCapPipeline(object):
    """
    将得到的数据存入数据库
    """
    def process_item(self, item, spider):

        if isinstance(item, CoinMarketCapBasicItem):
            item['collection_name'] = 'coin_market_cap_basic'
        if isinstance(item, CoinMarketCapDetailItem):
            item['collection_name'] = 'coin_market_cap_detail'
        if isinstance(item, CoinMarketCapChasrtsItem):
            item['collection_name'] = 'coin_market_cap_historical_charts'
        if isinstance(item, CoinMarketCapHistoricalDataItem):
            item['collection_name'] = 'coin_market_cap_historical_data'
        if isinstance(item, CoinMarketCapDominanceItem):
            item['collection_name'] = 'coin_market_cap_dominance'

        return item



