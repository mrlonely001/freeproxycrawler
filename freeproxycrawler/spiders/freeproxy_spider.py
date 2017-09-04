# -*- coding:utf-8 -*-
import scrapy
import time
from freeproxycrawler.items import FreeProxyItem

class FreeProxySpider(scrapy.Spider):
    name = 'freeproxycrawler'

    header = {
            "Host":"www.xicidaili.com",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding":"gzip, deflate, sdch",
            "Connection":"keep-alive",
            "Cache-Control":"max-age=0",
            "Host":"www.xicidaili.com",
            "Referer":"http://www.xicidaili.com/wt/",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
        }

    def start_requests(self):
        base_url = "http://www.xicidaili.com/wn/<pageth>/"
        urls = []
        for i in range(1,3):
            urls.append(base_url.replace("<pageth>",str(i)))
        for urlOne in urls:
            time.sleep(2)
            yield scrapy.Request(url=urlOne, callback=self.parse, headers=self.header)

    def parse(self, response):
        trs = response.css("tr")
        time_format = "%Y-%m-%d %X"
        for trOne in trs:
            tdArr = trOne.css("td")
            if len(tdArr)!=0:
                item = FreeProxyItem()
                item['ip'] = tdArr[1].css("::text").extract_first()
                item['port'] = tdArr[2].css("::text").extract_first()
                item['type'] = tdArr[5].css("::text").extract_first()
                item['crawl_time'] = time.strftime(time_format,time.localtime())
                yield item

