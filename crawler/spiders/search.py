# -*- coding: utf-8 -*-
import time

import scrapy


class SearchSpider(scrapy.Spider):
    name = 'search'
    allowed_domains = []
    start_urls = []

    site_url = ""

    match_words = []  # 要匹配的关键词
    filter_words = []  # 要过滤的关键词
    pageNum = 1
    fid = 1

    filename = "test_%s.html" % (time.strftime("%Y%m%d%H%M", time.localtime()))

    def start_requests(self):

        with open(self.filename, "w") as f:
            f.write("<meta charset='UTF-8'>\n")

        for i in range(1, self.pageNum):
            url = "%sthread.php?fid=%d&page=%d" % (self.site_url, self.fid, i)
            cookie = '4bd54_ol_offset=362586; 4bd54_ipstate=1518578446; 4bd54_lastpos=F26; 4bd54_threadlog=%2C8%2C37%2C26%2C; 4bd54_c_stamp='+(str)(int(time.time()))+'; 4bd54_lastvisit=1385%091518579820%09%2Fbbs%2Fthread.php%3Ffid26; sc_is_visitor_unique=rx4629288.1518579971.6729F05AFDA84F1B8748B27E26A9E2E1.2.2.2.2.2.2.2.2.2'
            headers = {
                'Cookie': cookie,
                'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
                'Accept': 'text/html,application/json,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.101 Safari/537.36'
            }
            yield scrapy.Request(url=url,
                                 headers=headers,
                                 callback=self.parse)
            # time.sleep(0.1)

    def parse(self, response):

        xpath = "/html/body/div[@class='wrap']/div[@class='main-wrap']/div[@id='main']/div[@id='pw_content']/div[@id='sidebar']/div[@class='content_thread cc']/div[@class='content_ie']/div[@class='pd15'][2]/div[@id='ajaxtable']/div[@class='z threadCommon']/table/tbody[@id='threadlist']/tr[@class='tr3']/td[@class='subject']"

        subject_sections = response.xpath(xpath)
        # print response.body
        # print subject_sections

        with open(self.filename, "w") as f:
            for section in subject_sections:

                texts = section.css("a::text").extract()
                subject = texts[0].encode("utf-8")
                is_continue = True

                # filter
                for word in self.filter_words:
                    if subject.find(word) >= 0:
                        is_continue = False
                        break

                if not is_continue:
                    continue

                # match
                for word in self.match_words:
                    if subject.find(word) >= 0:
                        links = section.css("a::attr(href)").extract()
                        name = texts[0].encode("utf-8")
                        link = str(self.site_url + links[0])
                        res = "<a href='%s' target='_blank'>%s</a>" % (link, name)
                        f.write(res + "<br>\n")
                        break
