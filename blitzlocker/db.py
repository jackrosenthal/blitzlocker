from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String
from sqlalchemy.types import *
from sqlalchemy.schema import ForeignKey
from os.path import expanduser

db_file_path = expanduser("~/.blitzlocker.db")

engine = create_engine('sqlite:///' + db_file_path)
Base = declarative_base()
Session = sessionmaker(bind=engine)
db = Session()

class Site(Base):
    __tablename__ = 'sites'

    id = Column(Integer, primary_key=True, autoincrement=True)
    base_url = Column(String, nullable=False)

    orgs = relationship('Org', back_populates='site')

class Org(Base):
    __tablename__ = 'orgs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    description = Column(String, nullable=True)

    site_id = Column(Integer, ForeignKey('sites.id', ondelete='CASCADE'), nullable=False)
    site = relationship('Site', back_populates='orgs')

class AppConfigItem(Base):
    __tablename__ = 'appconfig'

    key = Column(String, primary_key=True)
    value = Column(PickleType, nullable=False)

models = [Site, Org, AppConfigItem]

def seed():
    for m in models:
        m.metadata.drop_all(engine)
        m.metadata.create_all(engine)

