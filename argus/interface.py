from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import mapper, create_session
from models import Vote
import random


def get_rand_bill_ids(query, topic, num):
    if (topic is not None):
        results = query.filter(Vote.topic == topic)
        print(results.count())

        if num >= results.count():
            indexes = range(results.count())
        else:
            print(results.count())
            indexes = random.sample(range(1, results.count()), num)

        ids = [results[index].id for index in indexes]

    else:
        if num > query.count():
            ids = range(results.count())
        else:
            ids = random.sample(range(1, query.count()), num)

    return ids


def get_bill_description(query, id):
    return query.get(id).description

def get_bill_name(query, id):
    return query.get(id).name

def get_bill_topic(query, id):
    return query.get(id).topic