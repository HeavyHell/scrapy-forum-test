# -*- coding: utf-8 -*-

# Scrapy settings for forums project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Forums'

SPIDER_MODULES = ['Forums.spiders']
NEWSPIDER_MODULE = 'Forums.spiders'

ITEM_PIPELINES = {'pipelines.ForumPipeline': 100}

DATABASE = {
    'drivername': 'postgres',
    'host': 'localhost',
    'port': '5432',
    'username': 'postgres',
    'password': '',
    'database': 'forums'
}

DOWNLOAD_DELAY = 2

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

