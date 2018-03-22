# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisSpider
import scrapy
from selenium import webdriver
import time
import datetime
from datetime import timedelta
import re
import hashlib
from lxml import etree
import jsonpath
import requests
import json
from urllib import request


class DjieSpider(RedisSpider):
    name = 'dajie'
    redis_key = 'dajie:starts_url'
    custom_settings = {
        'COOKIES_ENABLED': False,
        'ROBOTSTXT_OBEY':False,

        'DEFAULT_REQUEST_HEADERS': {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
            # 'Cookie': 'DJ_UVID=MTUxNjgwMTI5NzkzMzE1MTAw; login_email=17769047675; _close_autoreg=1517208297204; DJ_RF=empty; DJ_EU=http%3A%2F%2Fwww.dajie.com%2Fajax%2Findex%2Fjobs%3Fajax%3D1%26type%3D1%26page%3D307%26pageSize%3D10'
        },
        # 'DOWNLOADER_MIDDLEWARES': {
            # 'xm.mymiddlewares.RandomProxy': 1,
        # }
    }

    base_url='https://www.dajie.com/ajax/index/jobs?ajax=1&type=2&page=%d&pageSize=100'
    def parse(self, response):
        for i in range(1,1051):
            url=self.base_url % i
            yield scrapy.Request(url=url,callback=self.parsePage)
    def parsePage(self,response):
        # print(response.text)
        data = json.loads(response.text)
        res = jsonpath.jsonpath(data, '$..clickUrl')
        # print(res)
        for url in res:
            # print(url)

            yield scrapy.Request(url=url,callback=self.parse_item,priority=10)

    def parse_item(self, response):
        url = response.url
        # print(url)
        # return {
        #     'url':url
        # }
        # '''
        jid = self.md5(url)
        #
        title = response.xpath('//div[@class="p-wrap-box"]//span[@class="job-name"]/text()').extract()[0]
        salary = response.xpath('//span[@class="job-money"]/text()').extract()[0].strip('元/月')
        lowsalary,hisalary=self.money(salary)
        location = response.xpath('//li[@class="ads"]//text()').extract()[0]
        exp = response.xpath('//li[@class="exp"]//text()').extract()[0]
        degree = response.xpath('//li[@class="edu"]//text()').extract()[0]
        job_type = response.xpath('//span[@class="blue-icon"]/text()').extract()[0].strip('(').strip(')')
        tags = response.xpath('//div[@class="job-msg-bottom"]//li/text()').extract()
        tags = ','.join(tags)
        date_pub = response.xpath('//span[@class="date"]/text()').extract()[0].strip('发布于')


        advantage = response.xpath('//div[@class="job-msg-bottom"]//li/text()').extract()
        advantage = ','.join(advantage)
        industry = response.xpath('//div[@id="jp_maskit"]//text()').extract()
        industry = ','.join(industry).strip()
        add = response.xpath('//div[@class="ads-msg"]/span/text()').extract()[0].strip()
        company = response.xpath('//div[@class="i-corp-base-info"]/p/a/text()').extract()[0].strip()

        return {
            'jid': jid,
            'url': url,
            'title': title,
            'lowsalary': lowsalary,
            'hisalary': hisalary,
            'location': location,
            'exp': exp,
            'degree': degree,
            'job_type': job_type,
            'tags': tags,
            'date_pub': date_pub,
            'advantage': advantage,
            'industry': industry,
            'add': add,
            'company': company,
        }

    def money(self, value):
        if '面议' in value:
            lowsa=0
            hisa=0
        elif "+" in value:
            res = value.replace('K', '').split('+')
            lowsa=int(res[0]) * 1000
            hisa = int(res[0]) * 1000
        else:
            res = value.replace('K', '').split('-')
            lowsa = int(res[0]) * 1000
            hisa = int(res[1]) * 1000
        return lowsa, hisa
    def md5(self, value):
        md5 = hashlib.md5()
        md5.update(bytes(value, encoding='utf-8'))
        return md5.hexdigest()

