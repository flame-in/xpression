from pymongo import MongoClient, DESCENDING
from pymongo.errors import BulkWriteError

from datetime import datetime
from itertools import chain


def database_setup():
    
    client = MongoClient('localhost', 27017)
    # print(client.list_database_names())
    db = client.twitter_database
    collection_returning = db.tweets_data
    return collection_returning


def date_setup(start, end):
    
    s_date = "0001/01/01"
    e_date = "9999/12/31"

    if not start:
        start = s_date
    if not end:
        end = e_date

    start = datetime.strptime(start, "%Y/%m/%d")
    end = datetime.strptime(end, "%Y/%m/%d")
    return start, end


def total_data_of_keyword(keyword_id):
    
    collection = database_setup()
    return collection.count_documents({"q": keyword_id})


# def retrieve_data(keyword_id, start_date, end_date, destination):
    
#     collection = database_setup()
#     start_date, end_date = date_setup(start_date, end_date)

#     query = {
#         "q": keyword_id,
#         "data.created_at": {
#             "$gte": start_date,
#             "$lte": end_date
#         }
#     }

#     if destination == "sentiment":
#         projection = {"_id": 1, "data.text": 1}

#     elif destination == "frontend":
#         # "sentiment_data": 0
#         projection = {"_id": 0, "data": 1, "sentiment_data": 1}

#     # result = collection.find(query)
#     result = collection.find(query, projection)


#     first = next(result, None)
#     if first is None:
#         return "keyword doesnt exist", ()
#     return "Keyword exist", chain((first,), result)


def delete_data_of_keyword(keyword_id):

    collection = database_setup()
    collection.delete_many({"q": keyword_id})
    print(f"document with keyword {keyword_id} deleted")

def retrieve_data(keyword_id, start_date, end_date, destination):
    
    collection = database_setup()
    start_date, end_date = date_setup(start_date, end_date)

    if destination == "sentiment":
        query = {
            "q": keyword_id,
            "sentiment_data": {"$exists": False},
            "data.created_at": {
                "$gte": start_date,
                "$lte": end_date
            }
        }
        projection = {"_id": 1, "data.text": 1}

    elif destination == "frontend":
        # "sentiment_data": 0
        query = {
            "q": keyword_id,
            "data.created_at": {
                "$gte": start_date,
                "$lte": end_date
            }
        }
        projection = {"_id": 1, "data": 1, "sentiment_data": 1}

    # result = collection.find(query)
    result = collection.find(query, projection)

    result = list(result)
    first = len(result)
    if first == 0:
        return "Keyword doesnt exist in DB. Adding.", ()
    return "Keyword exists in DB. Continuing.", result


def insert_data(tweets_list):

    collection = database_setup()
    element_present = collection.find_one({})

    if not element_present:
        collection.create_index([("q", DESCENDING)])

    try:
        collection.insert_many(tweets_list, ordered=False)
    except BulkWriteError as bwe:
        # print(bwe.details)
        pass

    return "Added Tweets."

def insert_sentiment_data(new_data):

    collection = database_setup()
    collection.update_one({'_id': new_data["_id"]},
                          {"$set": {"sentiment_data": new_data["sentiment_data"]}}
                          )
    return "Added sentiment data."


