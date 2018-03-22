# -*- coding: utf-8 -*-

# Scrapy settings for xm project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'xm'

SPIDER_MODULES = ['xm.spiders']
NEWSPIDER_MODULE = 'xm.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent

USER_AGENT = 'scrapy-redis (+https://github.com/rolando/scrapy-redis)'

# 过滤系统设置为scrapy-redis的过滤器
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

# 调度器
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

# 是否可以暂停爬虫
SCHEDULER_PERSIST = True

# 请求队列模式
# 按优先级调度请求,priority 数字越大，优先级越高
SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"

# 先进先出队列
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"

# 先进后出
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderStack"


# 数据存储到redis中
ITEM_PIPELINES = {
    'xm.pipelines.XmPipeline': 300,
    'scrapy_redis.pipelines.RedisPipeline': 999,
}

LOG_LEVEL = 'DEBUG'

# Introduce an artifical delay to make use of parallelism. to speed up the
# crawl.
DOWNLOAD_DELAY = 0.5

# redis连接信息
REDIS_HOST = '39.107.115.117'
REDIS_PORT = 6379


# Obey robots.txt rules
#ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'xm.middlewares.XmSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'xm.pipelines.XmPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
PROXIES = [
    {'host': '124.133.230.254', 'port': 80},
    {'host': '39.137.83.132', 'port': 8080},
    {'host': '219.150.189.212', 'port': 9999},
    {'host': '39.137.83.131', 'port': 8080},
    {'host': '39.137.83.133', 'port': 80},
    {'host': '14.215.177.58', 'port': 80},
    {'host': '163.177.151.23', 'port': 80},
    {'host': '202.100.83.139', 'port': 80},
    {'host': '221.200.117.65', 'port': 8118},
    {'host': '61.160.190.147', 'port': 8090},
    {'host': '60.164.225.5', 'port': 80},
    {'host': '101.251.230.125', 'port': 3128},
    {'host': '101.132.127.71', 'port': 8888},
    {'host': '121.8.98.197', 'port': 80},
    {'host': '222.73.217.7', 'port': 8080},
    {'host': '39.137.83.130', 'port': 80},
    {'host': '180.149.131.67', 'port': 80},
    {'host': '121.8.98.198', 'port': 80},
    {'host': '123.125.142.40', 'port': 80},
    {'host': '123.125.142.40', 'port': 80},
    {'host': '202.100.83.139', 'port': 80},
    {'host': '39.137.83.133', 'port': 80},
    {'host': '124.133.230.254', 'port': 80},
    {'host': '121.8.98.197', 'port': 80},
    {'host': '121.8.98.196', 'port': 80},
    {'host': '122.225.17.123', 'port': 8080},
    {'host': '39.137.83.132', 'port': 80},
    {'host': '58.254.61.158', 'port': 8118},
    {'host': '111.62.243.64', 'port': 80},
    {'host': '61.160.190.147', 'port': 8090},
    {'host': '112.80.255.21', 'port': 80},
    {'host': '39.137.83.132', 'port': 8080},
    {'host': '39.137.83.130', 'port': 80},
    {'host': '163.177.151.23', 'port': 80},
    {'host': '101.132.127.71', 'port': 8888},
    {'host': '60.164.225.5', 'port': 80},
    {'host': '14.215.177.58', 'port': 80},
    {'host': '221.200.117.65', 'port': 8118},
    {'host': '39.137.83.131', 'port': 8080},
    {'host': '222.73.217.7', 'port': 8080},
    {'host': '180.149.131.67', 'port': 80},
    {'host': '180.97.104.14', 'port': 80},
]
