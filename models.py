from sqlalchemy import Table, Column, Integer, MetaData, create_engine, String
from sqlalchemy.orm import mapper
from flask_login import UserMixin


user_db = create_engine("sqlite:///database.db")
metadata = MetaData(bind = user_db)

with open("senators.txt", "r") as fp:
    senators = [name.rstrip() for name in fp.readlines()]

class Vote(object):
    def __getitem__(self, item): 
        return getattr(self, item)
    def __setitem__(self, item, value):
        return setattr(self, item, value)

votes = Table('votes', metadata, 
        Column('id', Integer, primary_key=True), 
        Column('name', String(40)),
        Column('vote_number', Integer),
        Column('description', String(500)),
        Column('topic', String(80)),
        Column('vote_date', String(10)),
        Column('year', Integer),
        *(Column(senator, String(40)) for senator in senators),
)

mapper(Vote, votes)

class User(UserMixin): pass

users = Table("users", metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(15), unique=True),
    Column("email", String(50), unique=True),
    Column("password", String(80)),
    *(Column(str(bill_id), String(40)) for bill_id in range(1, 214)),
)

mapper(User, users)

metadata.create_all()