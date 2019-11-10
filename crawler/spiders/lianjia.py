# -*- coding: utf-8 -*-
import time

import scrapy
from scrapy_splash import SplashRequest


class SearchSpider(scrapy.Spider):
    name = "lianjia"
    allowed_domains = ["lianjia.com","airbnb.cn"]

    start_urls = [
    ]
    meta = {}

    html_url = "https://sh.lianjia.com/chengjiao/jinganxincheng/pg{0}/?sug=%E9%9D%99%E5%AE%89%E6%96%B0%E5%9F%8E"
    html_headers = {
        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4"
    }

    filename = "lianjia_%s.csv" % (time.strftime("%Y%m%d%H%M", time.localtime()))

    def start_requests(self):
        for i in range(1, 43):
            url = self.html_url.format(i)
            yield scrapy.Request(url=url,
                                 callback=self.parse)

    def parse(self, response):
        path = "/html/body/div[@class='content']/div[@class='leftContent']/ul[@class='listContent']/li/div[@class='info']"
        name_path = "div[@class='title']/a/text()"
        link_path = "div[@class='title']/a/@href"
        time_path = "div[@class='address']/div[@class='dealDate']/text()"
        transaction_price_path = "div[@class='address']/div[@class='totalPrice']/span[@class='number']/text()"
        deal_cycle_path = "div[@class='dealCycleeInfo']/span[@class='dealCycleTxt']/span"
        # sticker_price_path = "div[@class='dealCycleeInfo']/span[@class='dealCycleTxt']/span[1]/text()"
        # duration_path = "div[@class='dealCycleeInfo']/span[@class='dealCycleTxt']/span[2]/text()"
        unit_price_path = "div[@class='flood']/div[@class='unitPrice']/span[@class='number']/text()"
        position_info_path = "div[@class='flood']/div[@class='positionInfo']/text()"
        house_info_path = "div[@class='address']/div[@class='houseInfo']/text()"

        sections = response.xpath(path)
        with open(self.filename, "a") as f:
            for item in sections:
                name = item.xpath(name_path).extract()[0].encode("utf-8")
                link = item.xpath(link_path).extract()[0].encode("utf-8")
                time = item.xpath(time_path).extract()[0].encode("utf-8")
                transaction_price = item.xpath(transaction_price_path).extract()[0].encode("utf-8")
                deal_cycle = item.xpath(deal_cycle_path)
                if len(deal_cycle) == 1:
                    sticker_price = '挂牌0万'
                    duration = deal_cycle.xpath("text()").extract()[0].encode("utf-8")
                else:
                    sticker_price = deal_cycle.xpath("text()").extract()[0].encode("utf-8")   
                    duration = deal_cycle.xpath("text()").extract()[1].encode("utf-8")       
                    pass
                # sticker_price = item.xpath(sticker_price_path).extract()[0].encode("utf-8")
                # duration = item.xpath(duration_path).extract()[0].encode("utf-8")
                unit_price = item.xpath(unit_price_path).extract()[0].encode("utf-8")
                position_info = item.xpath(position_info_path).extract()[0].encode("utf-8")
                house_info = item.xpath(house_info_path).extract()[0].encode("utf-8")

                f.write(name + ",")
                f.write(link + ",")
                f.write(time + ",")
                f.write(transaction_price + ",")
                f.write(sticker_price + ",")
                f.write(duration + ",")
                f.write(unit_price + ",")
                f.write(position_info + ",")
                f.write(house_info + "\n")
        return
        
        #     for section in subject_sections:
        #         print section
        #         texts = section.css("a::text").extract()
        #         subject = texts[0].encode("utf-8")
        #         is_continue = True

        #         # filter
        #         for word in self.filter_words:
        #             if subject.find(word) >= 0:
        #                 is_continue = False
        #                 break

        #         if not is_continue:
        #             continue

        #         # match
        #         for word in self.match_words:
        #             if subject.find(word) >= 0:
        #                 links = section.css("a::attr(href)").extract()
        #                 name = texts[0].encode("utf-8")
        #                 link = str(self.site_url + links[0])
        #                 res = "<a href='%s'>%s</a>" % (link, name)
        #                 f.write(res + "<br>\n")
        #                 break
