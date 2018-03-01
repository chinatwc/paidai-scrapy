# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
from paidai.items import PaidaiItem

class PaidaiSpider(scrapy.Spider):
    name = 'paidai'
    # allowed_domains = ['http://bbs.paidai.com']
    start_urls = ['http://bbs.paidai.com/list/hot']

    def parse(self, response):
        post_urls = response.css('.m2-li-r-1 a::attr(href)').extract() # css选择器提取文章链接
        for post_url in post_urls:
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse_detil)

            # 提取下一页
            next_url = response.css('.page-sep-l::attr(href)').extract_first() # css选择器提取下一页链接
            if next_url is not None:
                next_url = response.urljoin(next_url)
                # yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse)
                yield scrapy.Request(next_url, callback=self.parse)


    def parse_detil(self,response):
        item = PaidaiItem()
        item['title']=response.css('.t_title::text').extract_first()
        item['author'] = response.css('.t_info span a::text').extract_first()
        item['time'] = response.css('.t_info span::text').extract()[1]
        item['fav_nums'] = response.css('.fav_btn_box a em::text').extract_first().strip()
        item['connent'] = response.css('#topic_content').extract()
        yield item


        #从首页爬取标题 作者
        # item = PaidaiItem()
        # text = response.css('.content-bottom-l-2-m2 ul li')
        # for v in text:
        #     item['title'] = v.css('span.m2-li-r-1 a::text').extract_first()
        #     item['author'] = v.css('.m2-li-r-2 a::text').extract_first()
        #     item['readNum'] = v.css('.readNum::text').extract_first()
        #     item['collectNum'] = v.css('.collectNum::text').extract_first()
        #     yield item
        #
        # next_page = response.css('.page-sep-l::attr(href)').extract_first() # css选择器提取下一页链接
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)  # 提交给parse继续抓取下一页
        pass




