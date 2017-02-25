# -*- coding: utf-8 -*-
import scrapy
import sys
from scrapy.loader import ItemLoader
from scrapy_splash import SplashRequest
import datetime
import tez_crawler.utils as Utils
import json

from tez_crawler.items.qunarItems import QunarAirTicketItem


class QunarSpider(scrapy.Spider):
    name = "qunar"
    allowed_domains = ["qunar.com"]
    start_urls = [
    ]

    # 上海(SHA) to 首尔(SEL)
    html_url = "http://flight.qunar.com/site/interroundtrip_compare.htm?fromCity=%E4%B8%8A%E6%B5%B7&toCity=%E9%A6%96%E5%B0%94&fromDate={0}&toDate={1}&fromCode=SHA&toCode=SEL&from=fi_int_search&lowestPrice=null&isInter=true&favoriteKey=&showTotalPr=null&adultNum=&childNum=&cabinClass="
    api_url = "http://flight.qunar.com/twell/flight/inter/search?depCity=%E4%B8%8A%E6%B5%B7&arrCity=%E9%A6%96%E5%B0%94&depDate={0}&retDate={1}&adultNum=1&childNum=0&ex_track=&from=fi_int_search&direct=true&es=MP1%2BZg9O5PHTZg9OJ5BTZogOVxHVZ3gOMPBVZotRFN9bNg9uJ5BM%3D%3D%3D%3D%7C1479811022546"
    "http://flight.qunar.com/twell/flight/inter/search?depCity=%E4%B8%8A%E6%B5%B7&arrCity=%E9%A6%96%E5%B0%94&depDate=2017-03-02&retDate=2017-03-05&adultNum=1&childNum=0&ex_track=&from=fi_int_search&direct=true"

    html_headers = {
        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4"
    }

    api_headers = {
        "X-Requested-With": "XMLHttpRequest"
    }

    def start_requests(self):
        init_time = int(datetime.datetime.strptime('2017-03-01', '%Y-%m-%d').strftime("%s"))
        day_range = 100
        interval_day = 3
        for i in range(0, day_range):
            start_time = init_time + (i * 86400)
            weekday = datetime.datetime.fromtimestamp(start_time).weekday()+1
            if weekday < 4 or weekday == 7:
                continue
            end_time = start_time + (interval_day * 86400)
            start_day = Utils.format_timestamp_day(start_time)
            end_day = Utils.format_timestamp_day(end_time)
            url = self.html_url.format(start_day, end_day)
            meta = {'start_day': start_day, 'end_day': end_day}
            yield SplashRequest(url,
                                splash_headers=self.html_headers,
                                callback=self._parse_html,
                                args={
                                    'wait': 1,
                                },
                                meta=meta)

    def _parse_html(self, response):
        print "####################[response html]############################"
        url = self.api_url.format(response.meta['start_day'], response.meta['end_day'])
        meta = {'start_day': response.meta['start_day'], 'end_day': response.meta['end_day']}
        # print url
        yield SplashRequest(url,
                            splash_headers=self.api_headers,
                            callback=self._parse_api,
                            meta=meta)
        pass

    def _parse_api(self, response):
        print "####################[response api]############################"

        min_price = sys.maxint
        optimal_flight = []
        json_str = response.body[response.body.index('{'): response.body.rindex('}') + 1]
        data = json.loads(json_str)['result']['flightPrices']

        for d in data.values():
            go_flight = d['journey']['trips'][0]['flightSegments'][0]
            back_flight = d['journey']['trips'][1]['flightSegments'][0]

            # time filter
            go_arr_stand_time = datetime.datetime.strptime("14:00", '%H:%M').time()
            back_dep_stand_time = datetime.datetime.strptime("18:00", '%H:%M').time()
            go_arr_latest_time = datetime.datetime.strptime(go_flight['arrTime'], '%H:%M').time()
            back_dep_lastest_time = datetime.datetime.strptime(back_flight['depTime'], '%H:%M').time()
            if go_arr_latest_time > go_arr_stand_time or back_dep_lastest_time < back_dep_stand_time:
                continue

            # compare price
            if min_price > int(d['price']['lowTotalPrice']):
                optimal_flight = [go_flight, back_flight]
                min_price = int(d['price']['lowTotalPrice'])

        if min_price != sys.maxint:
            l = ItemLoader(item=QunarAirTicketItem())
            l.add_value("price", min_price)
            l.add_value("go_flight_code", optimal_flight[0]['flightCode'])
            l.add_value("back_flight_code", optimal_flight[1]['flightCode'])
            l.add_value("go_dep_time", "%s %s" % (optimal_flight[0]['depDate'], optimal_flight[0]['depTime']))
            l.add_value("back_dep_time", "%s %s" % (optimal_flight[1]['depDate'], optimal_flight[1]['depTime']))
            l.add_value("go_arr_time", "%s %s" % (optimal_flight[0]['arrDate'], optimal_flight[0]['arrTime']))
            l.add_value("back_arr_time", "%s %s" % (optimal_flight[1]['arrDate'], optimal_flight[1]['arrTime']))
            l.add_value("start_time", response.meta['start_day'])
            l.add_value("end_time", response.meta['end_day'])
            return l.load_item()
