# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisCrawlSpider
import datetime
from datetime import timedelta
import re
import hashlib
import requests

class MyprojectSpider(RedisCrawlSpider):
    name = 'lagou'
    redis_key = 'lagou:starts_url'
    custom_settings = {
        'COOKIES_ENABLED': False,
        'DEFAULT_REQUEST_HEADERS': {
            "Host": "www.lagou.com",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            "Upgrade-Insecure-Requests": "1",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cookie": "user_trace_token=20171224205240-10b81281-b8a5-4f27-92e5-b241dbe6f20a; _ga=GA1.2.1770214120.1514119962; LGUID=20171224205240-539aa732-e8a9-11e7-9e3b-5254005c3644; index_location_city=%E5%8C%97%E4%BA%AC; JSESSIONID=ABAAABAACDBABJB9171B4D7DA62313FD1020111A2E14D74; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1515545537,1515999652,1516245140,1516588707; _gid=GA1.2.2095905795.1516588707; LGSID=20180122140047-9795d0a6-ff39-11e7-b3ec-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; TG-TRACK-CODE=index_navigation; SEARCH_ID=aa7c547d647546f49cb6ab7531fdc9d3; X_HTTP_TOKEN=9de4c1038ca39d713c95b6dae72f4944; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1516602112; _gat=1; LGRID=20180122142151-8903a83c-ff3c-11e7-b407-525400f775ce",
        },
        # 'DOWNLOADER_MIDDLEWARES': {
        #     'xm.mymiddlewares.RandomProxy': 1,
        # }
    }

    rules = (
        Rule(LinkExtractor(allow=r'zhaopin/.*'), follow=True),
        Rule(LinkExtractor(allow=r'gongsi/'), follow=True),
        Rule(LinkExtractor(allow=r'gongsi/j\d+'), follow=True),
        Rule(LinkExtractor(allow=r'gongsi/j\d+'), follow=True),
        Rule(LinkExtractor(allow=r'xiaoyuan\.lagou\.com'), follow=True),
        # Rule(LinkExtractor(allow=r'jobs/list'),follow=True),

        # 详情页链接规则
        Rule(LinkExtractor(allow=r'jobs/\d+\.html'), follow=False, callback='parse_item',process_request='pr'),
    )

    def pr(self, request):
        request.priority = 1
        return request
    def parse_item(self, response):

        url = response.url
        jid = self.md5(url)

        title = response.xpath('//span[@class="name"]/text()').extract()[0]
        salary = response.xpath('//span[@class="salary"]/text()').extract()[0]
        lowsalary,hisalary=self.money(salary)
        location = response.xpath('//dd[@class="job_request"]/p/span[2]/text()').extract()[0]
        location = self.remove_slash(location)

        exp = response.xpath('//dd[@class="job_request"]/p/span[3]/text()').extract()[0]
        exp = self.remove_slash(exp)

        degree = response.xpath('//dd[@class="job_request"]/p/span[4]/text()').extract()[0]
        degree = self.remove_slash(degree)

        job_type = response.xpath('//dd[@class="job_request"]/p/span[5]/text()').extract()[0]
        tags = response.xpath('//ul[@class="position-label clearfix"]/li/text()').extract()
        tags = ','.join(tags)
        date_pub = response.xpath('//p[@class="publish_time"]/text()').extract()[0]
        date_pub = self.process_date(date_pub)

        advantage = response.xpath('//dd[@class="job-advantage"]/p/text()').extract()[0]
        industry = response.xpath('//dd[@class="job_bt"]/div/p//text()').extract()
        industry = ''.join(industry)

        add = response.xpath('//div[@class="work_addr"]/a/text()').extract()[:-1]
        add = ''.join(add)
        company = response.xpath('//h2[@class="fl"]/text()').extract()[0].strip()

        return {
            'jid': jid,
            'url':url,
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

    def remove_slash(self, value):
        return value.replace('/', '')

    def money(self,value):
        if "K" in value:
            res = value.replace('K', '').split('-')
        else:
            res = value.replace('k', '').split('-')
        lowsa = int(res[0]) * 1000
        hisa = int(res[1]) * 1000
        return lowsa, hisa
    def process_date(self, value):
        value = value.replace('\xa0', '').strip(' 发布于拉勾网')
        if '天前' in value:
            days = int(value.strip('天前'))
            days = timedelta(days=days)
            res = datetime.datetime.now() - days
            res = res.strftime('%Y-%m-%d')
        elif ':' in value:
            res = datetime.datetime.now().strftime('%Y-%m-%d')
        else:
            res = value

        return res

    def md5(self, value):
        md5 = hashlib.md5()
        md5.update(bytes(value, encoding='utf-8'))
        return md5.hexdigest()