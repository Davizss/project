# -*- coding: utf-8 -*-
import sys,os
from scrapy.contracts import Contract


class CoinMarketCapContract(Contract):
    """
    这个contract的作用:
    为文章解析函数的合约检查提供基础：加上meta['data']
    """
    name = 'item_check'

    def adjust_request_args(self, args):
        """
        对文章请求进行预处理：加上meta['data']
        :param args:文章请求的参数
        :return: 修改后的文章请求的参数
        """
        args['meta'] = {
                    'unique_id': 'unique_id',
                    'timestamp': 'timestamp',
                    'coin_name_full': 'bitcoin',
                    'coin_url': 'https://coinmarketcap.com/currencies/bitcoin/',
                    'max_supply': 'max_supply',
                    'charts': 'charts',
                    'markets': 'markets'
                    }
        args['dont_filter'] = True
        return args