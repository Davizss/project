import pymysql

import threading
from queue import Queue
import requests
from lxml import etree

conn = pymysql.connect('127.0.0.1', 'root', '123456', 'tencent', charset='utf8')
cursor = conn.cursor()

def getProxy():
    proxy_q = Queue()

    sql = 'select * from xici'
    try:
        cursor.execute(sql)
        res = cursor.fetchall()
        for proxy in res:
            proxy_q.put(proxy)
    except Exception as e:
        print(e)
    return proxy_q

def close():
    cursor.close()
    conn.close()

class ProxyManager(threading.Thread):
    def __init__(self,proxy_q,lock):
        super(ProxyManager, self).__init__()
        self.proxy_q = proxy_q
        self.lock = lock

    def run(self):
        base_url = 'http://www.baidu.com/s?wd=ip'
        while not self.proxy_q.empty():
            proxy = self.proxy_q.get()
            proxy_info = {
                'http' : 'http://' + proxy[1] + ":" + str(proxy[2])
            }
            try:
                response = requests.get(url=base_url,proxies=proxy_info,timeout=5)
                if not (200 <= response.status_code <= 300):
                    # 删除代理
                    with self.lock:
                        self.drop_proxy(proxy[1])
                else:
                    html = etree.HTML(response.text)
                    if not html.xpath('//span[@class="c-gap-right"]/text()'):
                        # 删除代理
                        with self.lock:
                            self.drop_proxy(proxy[1])
                    else:
                        print(proxy)
            except Exception as e:
                # 异常需要从数据库删除代理
                print(e)
                with self.lock:
                    self.drop_proxy(proxy[1])

    def drop_proxy(self,host):
        sql = 'delete from xici where host="%s"' % host
        try:
            cursor.execute(sql)
            conn.commit()
            print('删除%s' % host)
        except Exception as e:
            print(e)
            conn.rollback()

if __name__ == '__main__':
    proxy_q = getProxy()
    thread_list = []
    lock = threading.Lock()

    for i in range(1):
        t = ProxyManager(proxy_q=proxy_q,lock=lock)
        t.start()
        thread_list.append(t)

    for t in thread_list:
        t.join()

    close()
