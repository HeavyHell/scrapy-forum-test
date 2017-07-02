# -*- coding: utf-8 -*-
import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request

from ..items import TopicItem, CommentItem


class MedSpider(CrawlSpider):
    name = 'medpred'
    allowed_domains = ['medpred.co.ua']
    start_urls = ['http://medpred.co.ua/forum']
    rules = (
        Rule(LinkExtractor(restrict_xpaths=('.//td[@class="row2" and @align="left"]/a')), callback='parse_item'),
        Rule(LinkExtractor(restrict_xpaths=('.//a[./text()="Далее"]')), follow=True),
        Rule(LinkExtractor(restrict_xpaths=('.//td[@class="row2" and @align="left"]/strong/a')), follow=True)
    )

    def parse_item(self, response):
        self.logger.info('Item %s', response.url)
        sel = Selector(response)
        table = sel.xpath('.//table[@class="ipbtable"][@cellspacing="1"]')
        forum = sel.xpath('//div[@style="font-weight:bold; font-size:12px;"]/a[3]/@href').extract_first(default='')
        forum = re.search(r'\d+', forum).group(0)


        if 'item' in response.meta:
            item = response.meta['item']
        else:
            item = TopicItem()
            item['url'] = response.url
            item['title'] = sel.xpath('(.//td[@width="99%"]/div/text())').extract_first(default='').strip()
            item['forum'] = forum
            item['number'] = re.search(r'\d+', response.url).group(0)
            topic_content = table.pop(0)
            table.pop()
            content = topic_content.xpath('.//span[@class="postcolor"]/div/text() |\
             .//span[@class="postcolor"]/div/*/text()').extract()
            item['content'] = ' '.join(content)
            item['username'] = topic_content.xpath('.//td[@class="row2"]/a/text()').extract_first()
            item['date'] = topic_content.xpath('.//div[@style="float:left;"]/text()').extract_first()

        if 'order' in response.meta:
            order = response.meta['order']
        else:
            order = 1

        next = sel.xpath('//a[./text()="Далее"]/@href').extract_first(default='')
        for post in table:
            comment = CommentItem()
            comment['forum'] = forum
            comment['topic_number'] = item['number']
            comment['order'] = order
            order = order + 1
            comment['username'] = post.xpath('.//td[@class="row2"]/a/text()').extract_first(default='')
            comment['date'] = post.xpath('.//div[@style="float:left;"]/text()').extract_first()
            content = post.xpath('.//span[@class="postcolor"]/div/text() | .//span[@class="postcolor"]/div/*/text()')
            content = content.extract()
            comment['content'] = '\n'.join(content)
            if comment['username'] != '':
                yield comment

        if next != '':
            request = Request(next, callback=self.parse_item)
            request.meta['item'] = item
            request.meta['order'] = order
            yield request
        else:
            yield item