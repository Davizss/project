# -*- coding: utf-8 -*-

# Scrapy settings for coin_market_cap project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'coin_market_cap'

SPIDER_MODULES = ['coin_market_cap.spiders']
NEWSPIDER_MODULE = 'coin_market_cap.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'coin_market_cap (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

DOWNLOAD_DELAY = 0.5

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

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
    'coin_market_cap.pipelines.CoinMarketCapPipeline': 300,
    'scrapy_redis.pipelines.RedisPipeline': 999,
}

LOG_LEVEL = 'DEBUG'

# redis连接信息
REDIS_HOST = '39.107.115.117'
REDIS_PORT = 6379
# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    'coin_market_cap.middlewares.ProxyMiddleware': 100,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'coin_market_cap.middlewares.RotateUserAgentMiddleware': 430
}

# 使用 SPIDER_CONTRACTS 设置来加载自定义的contracts
SPIDER_CONTRACTS = {
   'coin_market_cap.contracts.CoinMarketCapContract': 10,
}