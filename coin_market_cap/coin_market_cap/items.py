# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class CoinMarketCapItem(Item):
    unique_id = Field()


class CoinMarketCapBasicItem(Item):

    # 数字货币名称+数据更新时间戳 md5 hash code
    unique_id = Field()
    last_updated_timestamp = Field()
    timestamp = Field()
    # 数字货币全称
    coin_name_full = Field()
    # 不同兑换币种下的市值列表 (没有则为 -1）
    market_cap = Field()
    # 不同兑换币种下的当前价格(没有则为 -1）
    price = Field()
    # 不同兑换币种下的24小时内的交易量 (没有则为 -1）
    volume_24h = Field()
    # 不同兑换币种下的累计供应量(没有则为 -1）
    circulating_supply = Field()
    # 不同兑换币种下的24小时内的改变量(没有则为 'None'）
    change_24h = Field()
    # 不同兑换币种下的1小时内的改变量(没有则为 'None'）
    change_1h = Field()
    # 不同兑换币种下的7天内的改变量(没有则为 'None'）
    change_7d = Field()


class CoinMarketCapDetailItem(Item):

    # 数字货币名称+数据更新时间戳 md5 hash code
    unique_id = Field()
    last_updated_timestamp = Field()
    timestamp = Field()
    coin_name_full = Field()
    # 最大供给量
    max_supply = Field()
    """
    markets(list):过去24小时各个交易所情况,每个元素为字典格式其包含以下信息
    # 说明：有些交易所的交易数据出现异常或者更新时间不是最新的，导致交易量占比为0，数据无意义，则舍掉该条数据
    {
        market_name(string):交易所名字
        pair(string):币对
        volume_24h(int):24小时交易量
        price(float):价格
        volume_percentage(string):交易量占比
    }
    """
    markets = Field()


class CoinMarketCapChasrtsItem(Item):

    # 数字货币名称+数据时间戳 md5 hash code
    unique_id = Field()
    last_updated_timestamp = Field()
    coin_name_full = Field()
    timestamp = Field()
    market_cap_by_available_supply = Field()
    price_btc = Field()
    price_usd = Field()
    volume_usd = Field()


class CoinMarketCapHistoricalDataItem(Item):
    # 数字货币名称+数据时间戳 md5 hash code
    unique_id = Field()
    last_updated_timestamp = Field()
    coin_name_full = Field()
    timestamp = Field()
    open_price = Field()
    close_price = Field()
    high_price = Field()
    low_price = Field()
    volume = Field()
    market_cap = Field()


class CoinMarketCapDominanceItem(Item):

    # 数字货币名称+数据时间戳 md5 hash code
    unique_id = Field()
    last_updated_timestamp = Field()
    timestamp = Field()
    coin_name_full = Field()
    # 市值占比
    market_percentage = Field()
