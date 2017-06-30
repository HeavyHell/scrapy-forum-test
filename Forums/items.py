# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class TopicItem(Item):
    url = Field()
    forum = Field()
    title = Field()
    number = Field()
    username = Field()
    date = Field()
    content = Field()
    hash = Field()
    scraping_date = Field()


class CommentItem(Item):
    topic_number = Field()
    order = Field()
    forum = Field()
    username = Field()
    date = Field()
    content = Field()
    hash = Field()
    scraping_date = Field()

