# -*- coding: utf-8 -*-
import sys
import os
import scrapy
import time
import json
import hashlib
from scrapy import Request
from scrapy_redis.spiders import RedisCrawlSpider
from datetime import datetime,timezone,timedelta
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
from coin_market_cap.items import CoinMarketCapBasicItem, CoinMarketCapDetailItem, CoinMarketCapDominanceItem, CoinMarketCapChasrtsItem, CoinMarketCapHistoricalDataItem


class CoinMarketCapSpider(RedisCrawlSpider):
    name = 'coin_market_cap'
    redis_key = 'coin_market_cap:starts_url'
    # 所有货币market_cap的URL地址
    basic_url = 'https://coinmarketcap.com/all/views/all/'
    # dominance url
    dominance_url = 'https://graphs2.coinmarketcap.com/global/dominance/'

    def __init__(self, data_mode="all", prod_mode='basic', *args, **kwargs):
        """
        添加了data_mode的参数，如果是all：抓取全部 如果是1d：抓取最近一天的 如果是3d：抓取最近三天的 如果是7d：抓取最近7天的 如果是1m：抓取最近30天的\
        添加prod_mode参数
        :param data_mode:抓取图标数据模式  all：抓取全部，1d：抓取最近一天的， 3d：抓取最近三天的， 7d：抓取最近7天的， 1m：抓取最近30天的
        :param prod_mode:抓取数据模式 all:所有, basic, dominance, detail, historical_charts和historical_data 默认all
        :param args: 原始crawler参数
        :param kwargs: 原始crawler参数
        """
        super(CoinMarketCapSpider, self).__init__(*args, **kwargs)
        self.data_mode = data_mode
        self.prod_mode = prod_mode

    def parse(self, response):
        """
        把market_cap的URL传入到parse_basic回调函数进行解析
        :param response:首页的响应
        :return:无
        """
        if self.prod_mode == 'all' or self.prod_mode == 'basic':
            yield Request(url=self.basic_url, callback=self.parse_basic)
        if self.prod_mode == 'all' or self.prod_mode == 'dominance':
            yield Request(url=self.dominance_url, callback=self.parse_dominance)

    def parse_dominance(self, response):
        """
        解析dominance_url,抓取货币市值占比
        :param response: dominance_url 的响应数据
        :return:
        执行contracts测试
        @url https://graphs2.coinmarketcap.com/global/dominance/
        @returns items 0 30000
        @returns requests 0 0
        @scrapes unique_id  last_updated_timestamp  timestamp coin_name_full market_percentage
        """
        data = json.loads(response.text)

        for k, v in data.items():
            if self.data_mode == '1d':
                v = v[-2:]
            if self.data_mode == '3d':
                v = v[-6:]
            if self.data_mode == '7d':
                v = v[-14:]
            if self.data_mode == '1m':
                v = v[-60:]
            for info in v:
                item = CoinMarketCapDominanceItem()
                unique_id = '%s%s' % (k.title(), info[0])
                item['unique_id'] = self.get_md5(unique_id)
                item['coin_name_full'] = k.title()
                item['last_updated_timestamp'] = str(int(time.time() * 1000))
                item['timestamp'] = str(info[0])
                item['market_percentage'] = '{:.2f}%'.format(info[1])

                yield item

    def parse_basic(self, response):
        """
        解析basic_url,抓取需要的数据
        :param response: basic 的响应数据
        :return:
        执行contracts测试
        @url https://coinmarketcap.com/all/views/all/
        @returns items 0 2000
        @returns requests 0 2000
        @scrapes unique_id last_updated_timestamp timestamp coin_name_full market_cap price volume_24h circulating_supply change_24h change_1h change_7d
        """
        # 数据更新时间戳
        timestamp = response.xpath(
            "//div[@class='col-lg-10']/div[@class='row']/div[@class='col-xs-12 text-center text-gray']/text()").extract_first()
        timestamp = self.get_time(timestamp)
        """先抓取到BTC,ETH,XRP,BCH,LTC的实时price,1小时该变量,24小时改变量和7天改变量，用于记算不同兑换币种下的市值,价格,交易量(24小时),1小时该变量,24小时改变量和7天改变量"""
        """由于在网页中可以直接抓取以BTC为兑换币种下的市值,价格,交易量(24小时),所以值抓取了BTC的1小时该变量,24小时改变量和7天该改变量"""
        # BTC 1小时该变量,24小时改变量和7天改变量
        btc_change_1h = response.xpath(
            "//table[@id='currencies-all']/tbody/tr[@id='id-bitcoin']/td[8]/@data-sort").extract_first()
        btc_change_1h = self.get_float(btc_change_1h)
        btc_change_24h = response.xpath(
            "//table[@id='currencies-all']/tbody/tr[@id='id-bitcoin']/td[9]/@data-sort").extract_first()
        btc_change_24h = self.get_float(btc_change_24h)
        btc_change_7d = response.xpath(
            "//table[@id='currencies-all']/tbody/tr[@id='id-bitcoin']/td[10]/@data-sort").extract_first()
        btc_change_7d = self.get_float(btc_change_7d)

        # ETH 实时price和1小时该变量,24小时改变量和7天改变量
        eth_price = response.xpath(
            "//table[@id='currencies-all']/tbody//tr[@id='id-ethereum']/td[5]/a/@data-usd").extract_first()
        eth_price = self.get_float(eth_price)
        eth_change_1h = response.xpath(
            "//table[@id='currencies-all']/tbody/tr[@id='id-ethereum']/td[8]/@data-sort").extract_first()
        eth_change_1h = self.get_float(eth_change_1h)
        eth_change_24h = response.xpath(
            "//table[@id='currencies-all']/tbody/tr[@id='id-ethereum']/td[9]/@data-sort").extract_first()
        eth_change_24h = self.get_float(eth_change_24h)
        eth_change_7d = response.xpath(
            "//table[@id='currencies-all']/tbody/tr[@id='id-ethereum']/td[10]/@data-sort").extract_first()
        eth_change_7d = self.get_float(eth_change_7d)

        # XRP 实时price和1小时该变量,24小时改变量和7天改变量
        xrp_price = response.xpath(
            "//table[@id='currencies-all']/tbody//tr[@id='id-ripple']/td[5]/a/@data-usd").extract_first()
        xrp_price = self.get_float(xrp_price)
        xrp_change_1h = response.xpath(
            "//table[@id='currencies-all']/tbody/tr[@id='id-ripple']/td[8]/@data-sort").extract_first()
        xrp_change_1h = self.get_float(xrp_change_1h)
        xrp_change_24h = response.xpath(
            "//table[@id='currencies-all']/tbody/tr[@id='id-ripple']/td[9]/@data-sort").extract_first()
        xrp_change_24h = self.get_float(xrp_change_24h)
        xrp_change_7d = response.xpath(
            "//table[@id='currencies-all']/tbody/tr[@id='id-ripple']/td[10]/@data-sort").extract_first()
        xrp_change_7d = self.get_float(xrp_change_7d)

        # BCH 实时price和1小时该变量,24小时改变量和7天改变量
        bch_price = response.xpath(
            "//table[@id='currencies-all']/tbody//tr[@id='id-bitcoin-cash']/td[5]/a/@data-usd").extract_first()
        bch_price = self.get_float(bch_price)
        bch_change_1h = response.xpath(
            "//table[@id='currencies-all']/tbody/tr[@id='id-bitcoin-cash']/td[8]/@data-sort").extract_first()
        bch_change_1h = self.get_float(bch_change_1h)
        bch_change_24h = response.xpath(
            "//table[@id='currencies-all']/tbody/tr[@id='id-bitcoin-cash']/td[9]/@data-sort").extract_first()
        bch_change_24h = self.get_float(bch_change_24h)
        bch_change_7d = response.xpath(
            "//table[@id='currencies-all']/tbody/tr[@id='id-bitcoin-cash']/td[10]/@data-sort").extract_first()
        bch_change_7d = self.get_float(bch_change_7d)

        # LTC 实时price和1小时该变量,24小时改变量和7天改变量
        ltc_price = response.xpath(
            "//table[@id='currencies-all']/tbody//tr[@id='id-litecoin']/td[5]/a/@data-usd").extract_first()
        ltc_price = self.get_float(ltc_price)
        ltc_change_1h = response.xpath(
            "//table[@id='currencies-all']/tbody/tr[@id='id-litecoin']/td[8]/@data-sort").extract_first()
        ltc_change_1h = self.get_float(ltc_change_1h)
        ltc_change_24h = response.xpath(
            "//table[@id='currencies-all']/tbody/tr[@id='id-litecoin']/td[9]/@data-sort").extract_first()
        ltc_change_24h = self.get_float(ltc_change_24h)
        ltc_change_7d = response.xpath(
            "//table[@id='currencies-all']/tbody/tr[@id='id-litecoin']/td[10]/@data-sort").extract_first()
        ltc_change_7d = self.get_float(ltc_change_7d)

        coin_list = response.xpath("//table[@id='currencies-all']/tbody/tr")

        for coin in coin_list:
            item = CoinMarketCapBasicItem()
            # 数字货币名称
            coin_name_full = coin.xpath(".//td[2]/a/text()").extract_first()
            # 数字货币详情页url地址
            coin_url = coin.xpath(".//td[2]/a/@href").extract_first()
            coin_url = 'https://coinmarketcap.com%s' % coin_url
            # unique_id为数字货币名称+数据更新时间戳(coin_name_full+timestamp)md5 hash code
            unique_id = '%s%s' % (coin_name_full, timestamp)
            unique_id = self.get_md5(unique_id)
            # ---------不同兑换币种下的市值---------
            market_cap_usd = coin.xpath(".//td[4]/@data-usd").extract_first()
            market_cap_usd = self.get_float(market_cap_usd)
            market_cap_btc = coin.xpath(".//td[4]/@data-btc").extract_first()
            market_cap_btc = self.get_float(market_cap_btc)
            market_cap_eth = market_cap_usd / eth_price
            market_cap_xrp = market_cap_usd / xrp_price
            market_cap_bch = market_cap_usd / bch_price
            market_cap_ltc = market_cap_usd / ltc_price
            # 不同兑换币种下的市值列表
            market_cap = [
                {'USD': int(market_cap_usd)},
                {'BTC': int(market_cap_btc)},
                {'ETH': int(market_cap_eth)},
                {'XRP': int(market_cap_xrp)},
                {'BCH': int(market_cap_bch)},
                {'LTC': int(market_cap_ltc)},
            ]
            # ---------不同兑换币种下的当前价格---------
            price_usd = coin.xpath(".//td[5]/a/@data-usd").extract_first()
            price_btc = coin.xpath(".//td[5]/a/@data-btc").extract_first()
            price_usd = self.get_float(price_usd)
            price_btc = '{:.8f}'.format(self.get_float(price_btc))
            price_eth = '{:.8f}'.format(price_usd / eth_price)
            price_xrp = '{:.8f}'.format(price_usd / xrp_price)
            price_bch = '{:.8f}'.format(price_usd / bch_price)
            price_ltc = '{:.8f}'.format(price_usd / ltc_price)
            # 不同兑换币种下的当前价格列表
            price = [
                {'USD': float(price_usd)},
                {"BTC": float(price_btc)},
                {"ETH": float(price_eth)},
                {"XRP": float(price_xrp)},
                {"BCH": float(price_bch)},
                {"LTC": float(price_ltc)},
            ]
            # ---------流通供给量---------
            circulating_supply = coin.xpath(".//td[6]/@data-sort").extract_first().strip()
            circulating_supply = int(self.get_float(circulating_supply))
            # ---------不同兑换币种下的24小时内的交易量----------
            volume_24h_usd = coin.xpath(".//td[7]/a/@data-usd").extract_first()
            volume_24h_btc = coin.xpath(".//td[7]/a/@data-btc").extract_first()
            volume_24h_btc = self.get_float(volume_24h_btc)
            volume_24h_usd = self.get_float(volume_24h_usd)
            volume_24h_eth = volume_24h_usd / eth_price
            volume_24h_xrp = volume_24h_usd / xrp_price
            volume_24h_bch = volume_24h_usd / bch_price
            volume_24h_ltc = volume_24h_usd / ltc_price
            #  不同兑换币种下的24小时内的交易量列表
            volume_24h = [
                {'USD': int(volume_24h_usd)},
                {'BTC': int(volume_24h_btc)},
                {'ETH': int(volume_24h_eth)},
                {'XRP': int(volume_24h_xrp)},
                {'BCH': int(volume_24h_bch)},
                {'LTC': int(volume_24h_ltc)},
            ]
            # ---------不同兑换币种下的1小时内的改变量---------
            change_1h_usd = coin.xpath(".//td[9]/@data-sort").extract_first()
            # 如果数据为-0.0001说明在网页中显示为'？'，所以记为'None'
            if change_1h_usd == '-0.0001':
                change_1h_usd = 'None'
                change_1h_eth = 'None'
                change_1h_xrp = 'None'
                change_1h_ltc = 'None'
                change_1h_btc = 'None'
                change_1h_bch = 'None'
            else:
                change_1h_usd = self.get_float(change_1h_usd)
                change_1h_btc = '{0:.2f}{1}'.format(change_1h_usd - btc_change_1h, '%')
                change_1h_eth = '{0:.2f}{1}'.format(change_1h_usd - eth_change_1h, '%')
                change_1h_xrp = '{0:.2f}{1}'.format(change_1h_usd - xrp_change_1h, '%')
                change_1h_bch = '{0:.2f}{1}'.format(change_1h_usd - bch_change_1h, '%')
                change_1h_ltc = '{0:.2f}{1}'.format(change_1h_usd - ltc_change_1h, '%')
                change_1h_usd = '{0:.2f}{1}'.format(change_1h_usd, '%')
            # 不同兑换币种下的1小时内的改变量列表
            change_1h = [
                {'USD': change_1h_usd},
                {'BTC': change_1h_btc},
                {'ETH': change_1h_eth},
                {'XRP': change_1h_xrp},
                {'BCH': change_1h_bch},
                {'LTC': change_1h_ltc},
            ]
            # ---------不同兑换币种下的24小时内的改变量---------
            change_24h_usd = coin.xpath(".//td[9]/@data-sort").extract_first()
            # 如果数据为-0.0001说明在网页中显示为'？'，所以记为'None'
            if change_24h_usd == '-0.0001':
                change_24h_usd = 'None'
                change_24h_eth = 'None'
                change_24h_xrp = 'None'
                change_24h_ltc = 'None'
                change_24h_btc = 'None'
                change_24h_bch = 'None'
            else:
                change_24h_usd = self.get_float(change_24h_usd)
                change_24h_btc = '{0:.2f}{1}'.format(change_24h_usd - btc_change_24h, '%')
                change_24h_eth = '{0:.2f}{1}'.format(change_24h_usd - eth_change_24h, '%')
                change_24h_xrp = '{0:.2f}{1}'.format(change_24h_usd - xrp_change_24h, '%')
                change_24h_bch = '{0:.2f}{1}'.format(change_24h_usd - bch_change_24h, '%')
                change_24h_ltc = '{0:.2f}{1}'.format(change_24h_usd - ltc_change_24h, '%')
                change_24h_usd = '{0:.2f}{1}'.format(change_24h_usd, '%')
            # 不同兑换币种下的24小时内的改变量列表
            change_24h = [
                {'USD': change_24h_usd},
                {'BTC': change_24h_btc},
                {'ETH': change_24h_eth},
                {'XRP': change_24h_xrp},
                {'BCH': change_24h_bch},
                {'LTC': change_24h_ltc},
            ]
            # ---------不同兑换币种下的7天内的改变量---------
            change_7d_usd = coin.xpath(".//td[9]/@data-sort").extract_first()
            # 如果数据为-0.0001说明在网页中显示为'？'，所以记为'None'
            if change_7d_usd == '-0.0001':
                change_7d_usd = 'None'
                change_7d_eth = 'None'
                change_7d_xrp = 'None'
                change_7d_ltc = 'None'
                change_7d_btc = 'None'
                change_7d_bch = 'None'
            else:
                change_7d_usd = self.get_float(change_7d_usd)
                change_7d_btc = '{0:.2f}{1}'.format(change_7d_usd - btc_change_7d, '%')
                change_7d_eth = '{0:.2f}{1}'.format(change_7d_usd - eth_change_7d, '%')
                change_7d_xrp = '{0:.2f}{1}'.format(change_7d_usd - xrp_change_7d, '%')
                change_7d_bch = '{0:.2f}{1}'.format(change_7d_usd - bch_change_7d, '%')
                change_7d_ltc = '{0:.2f}{1}'.format(change_7d_usd - ltc_change_7d, '%')
                change_7d_usd = '{0:.2f}{1}'.format(change_7d_usd, '%')
            # 不同兑换币种下的7天内的改变量列表
            change_7d = [
                {'USD': change_7d_usd},
                {'BTC': change_7d_btc},
                {'ETH': change_7d_eth},
                {'XRP': change_7d_xrp},
                {'BCH': change_7d_bch},
                {'LTC': change_7d_ltc},

            ]

            item['unique_id'] = unique_id
            item['last_updated_timestamp'] = str(int(time.time() * 1000))
            item['timestamp'] = timestamp
            item['coin_name_full'] = coin_name_full
            item['market_cap'] = market_cap
            item['price'] = price
            item['volume_24h'] = volume_24h
            item['circulating_supply'] = circulating_supply
            item['change_1h'] = change_1h
            item['change_24h'] = change_24h
            item['change_7d'] = change_7d

            yield item
            if self.prod_mode == 'all' or self.prod_mode == 'detail':
                yield Request(
                    url=coin_url,
                    callback=self.parse_detail,
                    meta={
                        'unique_id': unique_id,
                        'timestamp': timestamp,
                        'coin_name_full': coin_name_full,
                        'coin_url': coin_url
                        }
                    )

    def parse_detail(self, response):
        """
        解析详情页,抓取需要的数据,构建charts的api地址,并传到回调函数parse_charts
        :param response: 详情页的响应数据
        :return:无
        执行contracts测试
        @url https://coinmarketcap.com/currencies/bitcoin/
        @item_check
        @returns items 0 1
        @returns requests 0 2
        @scrapes unique_id last_updated_timestamp timestamp coin_name_full max_supply markets
        """
        # 最大供应量
        max_supply = response.xpath("//div[@class='coin-summary-item col-xs-6 col-md-3'][4]/div/span/@data-format-value").extract_first()
        max_supply = int(self.get_float(max_supply))
        market_list = response.xpath("//table[@id='markets-table']/tbody/tr")
        markets = []
        for market in market_list:
            content = dict()
            content['volume_percentage'] = market.xpath(".//td[6]/span/text()").extract_first() + '%'
            # 交易量占比为0，数据无意义，则舍掉该条数据
            if content['volume_percentage'] == '0.00%':
                continue
            content['market_name'] = market.xpath(".//td[2]/a/text()").extract_first()
            content['pair'] = market.xpath(".//td[3]/a/text()").extract_first()
            volume_24h = market.xpath(".//td[4]/@data-sort").extract_first()
            price = market.xpath(".//td[5]/@data-sort").extract_first()
            content['volume_24h'] = int(float(volume_24h))
            content['price'] = float(price)
            markets.append(content)
        item = CoinMarketCapDetailItem()
        item['unique_id'] = response.meta['unique_id']
        item['timestamp'] = response.meta['timestamp']
        item['coin_name_full'] = response.meta['coin_name_full']
        item['last_updated_timestamp'] = str(int(time.time() * 1000))
        item['max_supply'] = max_supply
        item['markets'] = markets

        meta = dict()
        meta['timestamp'] = response.meta['timestamp']
        meta['coin_name_full'] = response.meta['coin_name_full']
        meta['coin_url'] = response.meta['coin_url']
        # 根据coin_url 构建详情页 接收charts的api地址
        charts_url = meta['coin_url'].replace('//', '//graphs2.')

        # historical-data的end参数结束日期 默认今天
        time_stamp = int(time.time())
        end_date = self.now_to_date(time_stamp)
        # historical-data的start参数开始日期 默认是20130428
        start_date = '20130428'
        if self.data_mode == '1d':
            start_date = self.now_to_date(time_stamp - 86400)
        if self.data_mode == '3d':
            start_date = self.now_to_date(time_stamp - (86400 * 3))
        if self.data_mode == '7d':
            start_date = self.now_to_date(time_stamp - (86400 * 7))
        if self.data_mode == '1m':
            start_date = self.now_to_date(time_stamp - (86400 * 30))
        # 根据coin_url, end_date, start_date 构建historical-data的url
        historical_data_url = meta['coin_url'] + 'historical-data/?start=' + start_date + '&end=' + end_date
        yield item
        if self.prod_mode == 'all' or self.prod_mode == 'historical_data':
            yield Request(url=historical_data_url, callback=self.parse_historical_data, meta=meta)
        if self.prod_mode == 'all' or self.prod_mode == 'historical_charts':
            yield Request(url=charts_url, callback=self.parse_charts, meta=meta)

    def parse_charts(self, response):
        """
        解析charts的api,抓取需要的数据,构建historical_data地址,并传到回调函数parse_historical_data
        :param response: charts的api的响应数据
        :return:无
        执行contracts测试
        @url https://graphs2.coinmarketcap.com/currencies/bitcoin/
        @item_check
        @returns items 0 2000
        @returns requests 0 2
        @scrapes unique_id last_updated_timestamp timestamp coin_name_full price_btc price_usd market_cap_by_available_supply volume_usd
        """
        meta = dict()
        meta['timestamp'] = response.meta['timestamp']
        meta['coin_name_full'] = response.meta['coin_name_full']
        meta['coin_url'] = response.meta['coin_url']

        data = json.loads(response.text)
        price_btc = data['price_btc']
        price_usd = data['price_usd']
        available_supply = data['market_cap_by_available_supply']
        volume_usd = data['volume_usd']
        if self.data_mode == '1d':
            price_btc = price_btc[-2:-1]
            price_usd = price_usd[-2:-1]
            available_supply = available_supply[-2:-1]
            volume_usd = volume_usd[-2:-1]
        if self.data_mode == '3d':
            price_btc = price_btc[-4:-1]
            price_usd = price_usd[-4:-1]
            available_supply = available_supply[-4:-1]
            volume_usd = volume_usd[-4:-1]
        if self.data_mode == '7d':
            price_btc = price_btc[-8:-1]
            price_usd = price_usd[-8:-1]
            available_supply = available_supply[-8:-1]
            volume_usd = volume_usd[-8:-1]
        if self.data_mode == '1m':
            price_btc = price_btc[-31:-1]
            price_usd = price_usd[-31:-1]
            available_supply = available_supply[-31:-1]
            volume_usd = volume_usd[-31:-1]
        for i in price_btc:
            item = CoinMarketCapChasrtsItem()
            index = price_btc.index(i)
            item['timestamp'] = str(i[0])
            item['price_btc'] = i[1]
            item['price_usd'] = price_usd[index][1]
            item['market_cap_by_available_supply'] = available_supply[index][1]
            item['volume_usd'] = volume_usd[index][1]
            unique_id = '%s%s' % (meta['coin_name_full'], str(i[0]))
            item['coin_name_full'] = meta['coin_name_full']
            item['last_updated_timestamp'] = str(int(time.time() * 1000))
            item['unique_id'] = self.get_md5(unique_id)

            yield item

    def parse_historical_data(self, response):
        """
        解析historical-data,抓取需要的数据,并yield item
        :param response: historical-data的响应数据
        :return:无
        执行contracts测试
        @url https://coinmarketcap.com/currencies/bitcoin/historical_data
        @item_check
        @returns items 0 2
        @scrapes unique_id last_updated_timestamp timestamp coin_name_full charts max_supply markets historical_data
        """
        data_list = response.xpath("//table[@class='table']/tbody/tr")
        for data in data_list:
            item = CoinMarketCapHistoricalDataItem()
            date = data.xpath(".//td[1]/text()").extract_first()
            # 表示没有数据 舍掉
            if date == 'No data was found for the selected time period':
                continue
            item['timestamp'] = self.get_date(date)
            item['open_price'] = float(data.xpath(".//td[2]/@data-format-value").extract_first())
            item['high_price'] = float(data.xpath(".//td[3]/@data-format-value").extract_first())
            item['low_price'] = float(data.xpath(".//td[4]/@data-format-value").extract_first())
            item['close_price'] = float(data.xpath(".//td[5]/@data-format-value").extract_first())
            item['volume'] = int(float(data.xpath(".//td[6]/@data-format-value").extract_first()))
            item['market_cap'] = int(self.get_float(data.xpath(".//td[7]/@data-format-value").extract_first()))
            item['coin_name_full'] = response.meta['coin_name_full']
            item['last_updated_timestamp'] = str(int(time.time() * 1000))
            unique_id = '%s%s' % (item['coin_name_full'], item['timestamp'])
            item['unique_id'] = self.get_md5(unique_id)

            yield item

    def get_date(self, value):
        """
        数据处理函数，将抓取到的时间信息处理成13位的时间戳字符串
        :param value: 时间信息
        :return: 13位时间戳字符串
        """
        if value:
            # 转换为datetime
            timeArray = datetime.strptime(value, "%b %d, %Y")
            # 转换为utc时间戳 精确到秒
            value = timeArray.replace(tzinfo=timezone(timedelta(hours=0))).timestamp()
            # 13位时间戳字符串
            value = str(int(value * 1000))
            return value
        else:
            return 'None'

    def get_time(self, value):
        """
        数据处理函数，将抓取到的时间信息处理成13位的时间戳字符串
        :param value: 时间信息
        :return: 13位时间戳字符串
        """
        if value:
            # 去掉多余的字符串 合适的时间格式
            value = value.strip().strip('Last updated: ').strip(' UTC')
            # 转换为datetime
            timeArray = datetime.strptime(value, "%b %d, %Y %I:%M %p")
            # 转换为utc时间戳 精确到秒
            value = timeArray.replace(tzinfo=timezone(timedelta(hours=0))).timestamp()
            # 13位时间戳字符串
            value = str(int(value * 1000))
            return value
        else:
            return str(int(time.time() * 1000))

    def get_md5(self, value):
        """
        md5加密
        :param value: 字符串
        :return: md5值
        """
        md5 = hashlib.md5()
        md5.update(bytes(value, encoding='utf-8'))
        return md5.hexdigest()

    def get_float(self, value):
        """
        数据处理函数，将字符串转为浮点数，否则返回-1
        :param value: 字符串
        :return: 浮点数 或 -1
        """
        if value:
            if value == '?' or value == 'None' or value == '-':
                return -1
            return float(value)
        return -1

    def now_to_date(self, time_stamp):
        """
        将时间戳格式化输出
        :param time_stamp: 时间戳（int）
        :return:格式化时间
        """
        time_array = time.localtime(time_stamp)
        str_date = time.strftime("%Y%m%d", time_array)
        return str_date


