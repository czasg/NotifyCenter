# coding: utf-8
import datetime
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()


class User(base):
    __tablename__ = 'users'

    id = Column(Integer(), autoincrement=True, primary_key=True)
    alias = Column(Text())
    username = Column(Text())
    password = Column(Text())
    created_time = Column(DateTime(), default=datetime.datetime.now)
    updated_time = Column(DateTime(), default=datetime.datetime.now)


class Group(base):
    __tablename__ = 'groups'

    id = Column(Integer(), autoincrement=True, primary_key=True)
    alias = Column(Text())
    description = Column(Text())
    belong_to = Column(Integer())
    created_time = Column(DateTime(), default=datetime.datetime.now)
    updated_time = Column(DateTime(), default=datetime.datetime.now)


class UserGroup(base):
    __tablename__ = 'user_groups'

    id = Column(Integer(), autoincrement=True, primary_key=True)
    group_id = Column(Integer())
    user_id = Column(Integer())


class Label(base):
    __tablename__ = 'labels'

    id = Column(Integer(), autoincrement=True, primary_key=True)
    name = Column(Text())
    description = Column(Text())
    is_public = Column(Boolean(), default=False)
    belong_to = Column(Integer())
    created_time = Column(DateTime(), default=datetime.datetime.now)
    updated_time = Column(DateTime(), default=datetime.datetime.now)


class Notify(base):
    __tablename__ = 'notify'

    id = Column(Integer(), autoincrement=True, primary_key=True)
    mode = Column(Text())
    uri = Column(Text())
    created_time = Column(DateTime(), default=datetime.datetime.now)
    updated_time = Column(DateTime(), default=datetime.datetime.now)
