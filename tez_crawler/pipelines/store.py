# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from twisted.enterprise import adbapi
import logging

import tez_crawler.pipelines.qunarProcess as QunarProcess
from tez_crawler.items.qunarItems import QunarAirTicketItem


class MysqlPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        name = settings['DB_SERVER']
        dbargs = settings['DB_CONNECT']
        dbpool = adbapi.ConnectionPool(name, **dbargs)
        return cls(dbpool)

    def process_item(self, item, spider):
        logging.info('############[Pipeline mysql store]############')

        if isinstance(item, QunarAirTicketItem):
            self.dbpool.runInteraction(QunarProcess.insert, item)
