# -*- coding: utf-8 -*-
import json
import redis  # pip install redis
import pymysql

def main():
    # 指定redis数据库信息
    rediscli = redis.StrictRedis(host='39.107.115.117', port = 6379, db = 0)
    # 指定本地mysql数据库
    mysqlcli = pymysql.connect(host='127.0.0.1', user='root', passwd='123456', db='tencent', charset='utf8')

    # 无限循环
    while True:
        source, data = rediscli.blpop(["lagou:items"]) # 从redis里提取数据

        item = json.loads(data.decode('utf-8')) # 把 json转字典

        try:
            # 使用cursor()方法获取操作游标
            cur = mysqlcli.cursor()
            # 使用execute方法执行SQL INSERT语句
            sql = 'insert into lagou(jid,url,title,lowsalary,hisalary,location,exp,degree,job_type,tags,date_pub,advantage,industry,addr,company,spider_name,crawl_time) ' \
                  'VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) on duplicate key update jid=values(jid),url=VALUES(url)'
            cur.execute(sql, (item["jid"],item["url"], item["title"], item["lowsalary"], item["hisalary"], item["location"], item["exp"],item["degree"], item["job_type"], item["tags"], item["date_pub"], item["advantage"], item["industry"],item["add"], item["company"], item["spider"],item["crawled"]))

            # 提交sql事务
            mysqlcli.commit()
            #关闭本次操作
            cur.close()
            print ("插入 %s" % item['title'])
        except pymysql.Error as e:
            mysqlcli.rollback()
            print ("插入错误" ,str(e))

if __name__ == '__main__':
    main()