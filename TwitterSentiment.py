"""
@author: Gautam K
"""

from json import load
from os import path
from re import sub
from sqlite3 import connect
from textblob import TextBlob
from tweepy import API, OAuthHandler

DIR_PATH = path.dirname(path.abspath(__file__))


class TwitterSentiment:
    """
    Twitter Sentiment Analyzer
    """
    def __init__(self):
        """
        Constructor
        """
        try:
            with open("twitter_api_keys.json") as f:
                api_keys = load(f)
            self.__consumer_key = api_keys["consumer_key"]
            self.__consumer_secret = api_keys["consumer_secret"]
            self.__access_token = api_keys["access_token"]
            self.__access_token_secret = api_keys["access_token_secret"]
        except (FileNotFoundError, IOError):
            print("[IOError] Twitter API Keys file not found.\nExiting...")
            exit(1)
        except KeyError:
            print("[KeyError] Appropriate Twitter API Keys not found in keys file.\nExiting...")
            exit(1)
        except Exception as exp:
            print("[ERROR] %s" % exp)
            exit(1)

    @staticmethod
    def __get_data():
        """
        Get the Celeb names from db.
        :return: List of celeb data.
        """
        try:
            with connect("celebData.db") as con:
                cur = con.cursor()
                # Return all the celeb names in db.
                cur.execute("SELECT NAME FROM CELEB_DATA;")
                return cur.fetchall()
        except Exception:
            print("!!! An Exception Occurred: Could not get celeb data from db !!!")
            return -1

    @staticmethod
    def __dump_data(data):
        """
        Update the sentiment data in db.
        :param data: list with dict of (celeb_name: sentiment)
        :return: None
        """
        try:
            with connect("celebData.db") as con:
                cur = con.cursor()
                for d in data:
                    # Update table with sentiment for the celeb.
                    for key in d.keys():
                        cur.execute("UPDATE CELEB_DATA SET SENTIMENT=? WHERE NAME=?;", (d.get(key, "NA"), key,))
                        con.commit()
        except Exception:
            print("!!! An Exception Occurred: "
                  "Could not update sentiment data in db !!!")
            return -1

    @staticmethod
    def __normalize_tweet(tweet):
        """
        Utility function to clean tweet text by removing links,
        special characters using simple regex statements.
        """
        return ' '.join(sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])"
                            "|(\w+://\S+)", "", tweet).split())

    def __get_tweet_polarity(self, tweet):
        """
        Get the tweets sentiment polarity.
        :param tweet: The tweet text.
        :return: Polarity of the sentiment of tweet.
        """
        analysis = TextBlob(self.__normalize_tweet(tweet))
        return analysis.sentiment.polarity

    def get_twitter_sentiment(self):
        """
        Analyze the tweet sentiment.
        :return: 1 if success else -1
        """
        try:
            print("Getting celeb data from db...")
            res = celeb_data = self.__get_data()
            if res == -1:
                return -1

            print("Authorizing app...")
            # Create OAuthHandler object
            auth = OAuthHandler(self.__consumer_key,
                                self.__consumer_secret)

            # Set access token and secret
            auth.set_access_token(self.__access_token,
                                  self.__access_token_secret)

            # Create tweepy API object to fetch tweets
            api = API(auth)

            # For each celeb in celeb list perform setiment analysis
            sentiment_list = list()
            print("\nPerforming Twitter Sentiment Analysis...Please Wait...")
            for celeb in list(celeb_data):
                """
                For each celeb, get the tweets, calculate sentiment and
                form a dict(celeb: sentiment)
                """
                celeb_sentiment = {}
                negative = 0
                positive = 0
                neutral = 0
                celeb_name = celeb[0]

                # Get the last 100 tweets from twitter for the celeb.
                tweets = api.search(q=celeb_name, count=100)
                if len(tweets) == 0:
                    celeb_sentiment[celeb_name] = "NA"
                    continue
                for tweet in tweets:
                    # get the tweets sentiment polarity
                    tweet_polarity = self.__get_tweet_polarity(tweet.text)

                    # decide positive negative or neutral based on polarity
                    if tweet_polarity > 0:
                        positive += 1
                    elif tweet_polarity == 0:
                        neutral += 1
                    else:
                        negative += 1
                # Decide the overall sentiment for the celeb
                if positive >= neutral and positive >= negative:
                    celeb_sentiment[celeb_name] = "POSITIVE"
                elif neutral >= positive and neutral >= negative:
                    celeb_sentiment[celeb_name] = "NEUTRAL"
                else:
                    celeb_sentiment[celeb_name] = "NEGATIVE"

                # Append the dict to sentiment list for later use.
                sentiment_list.append(celeb_sentiment)
            print("Twitter sentimental analysis completed...")

            print("Updated db with sentiment data...")
            res = self.__dump_data(sentiment_list)
            if res == -1:
                return -1
            print("Sentiment data successfully updated in db...")
            return 1
        except Exception as exp:
            print("!!! Exception: %s !!!" % exp)
            return -1
