# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QunarAirTicketItem(scrapy.Item):
    price = scrapy.Field()
    go_flight_code = scrapy.Field()
    back_flight_code = scrapy.Field()
    go_dep_time = scrapy.Field()
    go_arr_time = scrapy.Field()
    back_dep_time = scrapy.Field()
    back_arr_time = scrapy.Field()
    start_time = scrapy.Field()
    end_time = scrapy.Field()
    pass
