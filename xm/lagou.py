from scrapy import cmdline

import os

os.chdir('xm/spiders')

cmdline.execute('scrapy runspider lagou.py'.split())

