from xm import settings
import random


class RandomProxy(object):
    def process_request(self,request,spider):
        proxy = random.choice(settings.PROXIES)
        proxy = 'http://%s:%d' % (proxy['host'], proxy['port'])
        request.meta['proxy'] = proxy  # 设置代理
