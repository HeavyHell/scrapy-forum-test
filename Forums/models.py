
from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

from . import settings


DeclarativeBase = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**settings.DATABASE))


def create_deals_table(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)


class Topics(DeclarativeBase):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True)
    url = Column('url', String)
    title = Column('title', String)
    forum = Column('forum', Integer)
    number = Column('number', Integer)
    username = Column('username', String, nullable=True)
    date = Column('date', Date, nullable=True)
    scraping_date = Column('scraping_date', DateTime, nullable=True)
    content = Column('content', String, nullable=True)
    hash = Column('hash', String, nullable=True)

class Comments(DeclarativeBase):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    forum = Column('forum', Integer)
    topic_number = Column('topic_number', Integer)
    order = Column('order', Integer)
    username = Column('username', String, nullable=True)
    date = Column('date', Date, nullable=True)
    scraping_date = Column('scraping_date', DateTime, nullable=True)
    content = Column('content', String, nullable=True)
    hash = Column('hash', String, nullable=True)
