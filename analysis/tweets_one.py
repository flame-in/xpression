import tweepy
from analysis.dbcode import insert_data


def tweepybot(query, no_of, tpn_type="mixed"):
    consumer_key = ""
    consumer_secret = ""

    auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


    tweets_list = []

    unique_tweet = set()
    tpn = "mixed"
    type_of_tweet_needed = tpn

    for tweet in tweepy.Cursor(api.search, q=query, lang='en', result_type=tpn, tweet_mode='extended').items(no_of):

        created_at = tweet.created_at

        tweet_loaded = tweet._json


        tweet_id = tweet_loaded["id_str"]
        text = tweet_loaded["full_text"]
        entities = tweet_loaded["entities"]

        if tweet_id in unique_tweet:
            print("duplicate")
            continue
        unique_tweet.add(tweet_id)


        single_tweet = {"_id": tweet_id, "q": query,
                        "data":
                            {"text": text,
                             "created_at": created_at,
                             "hashtags": entities["hashtags"],
                             "symbols": entities["symbols"],
                             "followers_count": tweet_loaded["user"]["followers_count"],
                             "retweet_count": tweet_loaded["retweet_count"],
                             "favorite_count": tweet_loaded["favorite_count"]
                             }
                        }

        tweets_list.append(single_tweet)

    if len(unique_tweet) == 0:
        # raise Exception("No tweet found")
        status = "No tweet found"
        return status
    print(f"Successful, total number of tweets collected {len(unique_tweet)}")

    status = insert_data(tweets_list)
    return status
