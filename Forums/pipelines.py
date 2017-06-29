# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.orm import sessionmaker
from datetime import datetime
from Forums.models import db_connect, create_deals_table, Topics, Comments
from Forums.items import TopicItem

import hashlib


class ForumPipeline(object):
    """Livingsocial pipeline for storing scraped items in the database"""
    def __init__(self):
        engine = db_connect()
        create_deals_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        item['date'] = self.reformat_date(item)
        item['hash'] = self.get_hash(item)
        item['scraping_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(item, TopicItem):
            md = Topics(**item)
            if not self.check_topic(item,session):
                return item
        else:
            md = Comments(**item)
            if not self.check_comment(item,session):
                return item

        try:
            session.add(md)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return item

    def reformat_date(self, item):
        month_names = [
            'января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
            'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'
        ]

        date = item['date'].split()
        day = date[0]
        month = month_names.index(date[1]) + 1
        year = date[2]

        if month < 10:
            month = '0' + str(month)
        else:
            month = str(month)
        return year + '-' + month + '-' + day

    def get_hash(self, item):
        st = item['username']+item['date']+item['content']
        hs = hashlib.md5(st.encode())
        return hs.hexdigest()

    def check_topic(self, item, session):
        num = item['number']
        hs = item['hash']
        if session.query(Topics).filter_by(number=num).count() == 0:
            return True
        elif session.query(Topics).filter_by(number=num).filter_by(hash=hs).count() == 0:
            return True
        else:
            return False

    def check_comment(self, item, session):
        num = item['topic_number']
        hs = item['hash']
        if session.query(Comments).filter_by(topic_number=num).count() == 0:
            return True
        elif session.query(Comments).filter_by(topic_number=num).filter_by(hash=hs).count() == 0:
            return True
        else:
            return False