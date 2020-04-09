# -*- coding: utf-8 -*-
import time

import scrapy
from scrapy_splash import SplashRequest

# 静安新城
# html_url = "https://sh.lianjia.com/chengjiao/jinganxincheng/pg{0}a2a3a4/"
# 闵行春申
# html_url = "https://sh.lianjia.com/chengjiao/chunshen/pg{0}a2a3a4/"
# 闵行莘庄
# html_url = "https://sh.lianjia.com/chengjiao/xinzhuang5/pg{0}a2a3a4/"
# 闵行七宝
# html_url = "https://sh.lianjia.com/chengjiao/qibao/pg{0}a2a3a4/"

area_dict = {
    # "chunshen": 44,
    "qibao": 42,
    "jinganxincheng": 36
    # "xinzhuang5": 66
}

class SearchSpider(scrapy.Spider):
    name = "lianjia"
    allowed_domains = ["lianjia.com"]

    start_urls = [
    ]
    meta = {}
    
    html_headers = {
        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4"
    }

    
    def start_requests(self):
        for (k,v) in area_dict.items():
            area = k
            page_num = v
            filename = "lianjia_%s_%s.csv" % (area, time.strftime("%Y%m%d%H%M", time.localtime()))
            html_url = "https://sh.lianjia.com/chengjiao/" + area + "/pg{0}a2a3a4/"
            for i in range(1, page_num):
                url = html_url.format(i)
                time.sleep(1)
                # print(url)
                yield scrapy.Request(url=url,
                                     meta={'filename':filename},
                                     callback=self.parse)
                pass
        

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
        with open(response.meta['filename'], "a") as f:
            for item in sections:
                name = item.xpath(name_path).extract()[0].encode("utf-8")
                name_arr = name.split(" ")
                cell_name = name_arr[0]
                cell_type = name_arr[1]
                cell_size = name_arr[2]
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
                position_arr = position_info.split(" ")
                floor = position_arr[0]
                building = position_arr[1]

                house_info = item.xpath(house_info_path).extract()[0].encode("utf-8")
                house_arr = house_info.split("|")
                direction = house_arr[0]
                fitment_type = house_arr[1]

                f.write(cell_name + ",")
                f.write(cell_type + ",")
                f.write(cell_size + ",")
                f.write(link + ",")
                f.write(time + ",")
                f.write(transaction_price + ",")
                f.write(sticker_price + ",")
                f.write(duration + ",")
                f.write(unit_price + ",")
                f.write(floor + ",")
                f.write(building + ",")
                f.write(direction + ",")
                f.write(fitment_type + "\n")
        return
