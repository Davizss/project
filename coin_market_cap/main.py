from scrapy import cmdline

import os

os.chdir('coin_market_cap/spiders')

cmdline.execute('scrapy runspider coin_market_cap_spider.py'.split())

