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

    filename = "test_%s.html" % (time.strftime("%Y%m%d%H%M", time.localtime()))

    def start_requests(self):

        with open(self.filename, "w") as f:
            f.write("<meta charset='UTF-8'>\n")

        for i in range(1, 200):
            url = "%s?page=%d" % (self.site_url, i)
            yield scrapy.Request(url=url,
                                 callback=self.parse)

    def parse(self, response):

        xpath = "/html/body/div[@class='wrap']/div[@class='main-wrap']/div[@id='main']/div[@id='pw_content']/div[@id='sidebar']/div[@class='content_thread cc']/div[@class='content_ie']/div[@class='pd15'][2]/div[@id='ajaxtable']/div[@class='z threadCommon']/table/tbody[@id='threadlist']/tr[@class='tr3']/td[@class='subject']"

        subject_sections = response.xpath(xpath)

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
                        res = "<a href='%s'>%s</a>" % (link, name)
                        f.write(res + "<br>\n")
                        break
