# encoding=utf-8
import sqlalchemy
import re
import datetime
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import Column, Integer, String, DateTime, Text, text

class StandardItem(Base):
    __tablename__ = "standard_items"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    brand = Column(String(255))
    price = Column(Integer)
    specification = Column(String(255))
    item_attr = Column(Text(65536))
    
    def __repr__(self):
        return "<User(name='%s', id='%s', brand='%s')>" % (self.name, self.id, self.brand)


