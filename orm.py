import sqlite3
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils.types.choice import ChoiceType
import flask_sqlalchemy


engine = create_engine('sqlite://taxi_db')
Base = declarative_base

class Driver(Base):
    __tablename__ = 'driver'
    identifier = Column(Integer, primary_key=True, comment="Идентификатор игрока")