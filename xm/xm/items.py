# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
from scrapy.item import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join


class ExampleItem(Item):
    jid = Field()
    url=Field()
    title = Field()
    lowsalary = Field()
    hisalary = Field()
    location = Field()
    exp = Field()
    degree = Field()
    job_type = Field()
    tags = Field()
    date_pub = Field()
    advantage = Field()
    industry = Field()
    add = Field()
    company = Field()
    spider = Field()
    crawled = Field()




class ExampleLoader(ItemLoader):
    default_item_class = ExampleItem
    default_input_processor = MapCompose(lambda s: s.strip())
    default_output_processor = TakeFirst()
    description_out = Join()
