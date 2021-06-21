import json
import pandas as pd
from textblob import TextBlob
import sys

sys.path.insert(0, '\\')


def read_json(json_file: str) -> list:
    """
    json file reader to open and read json files into a list
    Args:
    -----
    json_file: str - path of a json file
    
    Returns
    -------
    length of the json file and a list of json
    """

    tweets_data = []
    for tweets in open(json_file, 'r'):
        tweets_data.append(json.loads(tweets))

    return len(tweets_data), tweets_data


class TweetDfExtractor:
    """
    this function will parse tweets json into a pandas dataframe
    
    Return
    ------
    dataframe
    """

    def __init__(self, tweets_list):

        self.tweets_list = tweets_list

    # an example function
    def find_statuses_count(self) -> list:
        statuses_count = [x['statuses_count'] for x in self.tweets_list]
        return list(statuses_count)

    def find_full_text(self) -> list:
        text=[]
        for x in self.tweets_list:
            if 'retweeted_status' in x:
                if 'extended_tweet' in x['retweeted_status']:
                    text.append(x['retweeted_status']['extended_tweet']['full_text'])
                else:
                    text.append(x['retweeted_status']['text'])
            else:
                text.append(x['text'])
        return text

    def find_sentiments(self, text) -> list:
        polarity = []
        subjectivity = []
        for i in text:
            blob = TextBlob(i)
            sentiment = blob.sentiment
            polarity.append(sentiment.polarity)
            subjectivity.append(sentiment.subjectivity)
        return [polarity, subjectivity]

    def find_created_time(self) -> list:

        return [x['created_at'] for x in self.tweets_list]

    def find_source(self) -> list:
        source = [x['source'] for x in self.tweets_list]

        return source

    def find_screen_name(self) -> list:
        screen_name = [x['user']['screen_name'] for x in self.tweets_list]
        return screen_name

    def find_followers_count(self) -> list:
        followers_count = [x['user']['followers_count'] for x in self.tweets_list]
        return followers_count

    def find_friends_count(self) -> list:
        friends_count = [x['user']['friends_count'] for x in self.tweets_list]
        return friends_count

    def is_sensitive(self) -> list:
        is_sensitive = [x['possibly_sensitive'] if 'possibly_sensitive' in x else 'None'  for x in self.tweets_list]
        return is_sensitive

    def find_favourite_count(self) -> list:
        return [x['retweeted_status']['favorite_count'] if 'retweeted_status'in x else x['favorite_count'] for x in self.tweets_list]

    def find_retweet_count(self) -> list:
        retweet_count = [x['retweeted_status']['retweet_count'] if 'retweeted_status'in x else x['retweet_count'] for x in self.tweets_list]
        return retweet_count

    def find_hashtags(self) -> list:
        hashtags=[]
        for x in self.tweets_list:
            if len(x['entities']['hashtags'])>0:
                hashtags.append('\n'.join([i['text'] for i in x['entities']['hashtags']]))
            else:
                hashtags.append('')
        return hashtags

    def find_mentions(self) -> list:
        mensions=[]
        for x in self.tweets_list:
            if len(x['entities']['user_mentions'])>0:
                mensions.append('\n'.join([i['screen_name'] for  i in x['entities']['user_mentions'] ]))
            else:
                mensions.append('')
        return mensions
    def find_location(self) -> list:
        location = [x['user']['location'] if 'user' in x and 'location' in x['user']  else '' for x in self.tweets_list]
        return location

    def find_lang(self):
        return [x['lang'] for x in self.tweets_list]

    def get_tweet_df(self, save=False) -> pd.DataFrame:
        """required column to be generated you should be creative and add more features"""

        columns = ['created_at', 'source', 'original_text', 'polarity', 'subjectivity', 'lang', 'favorite_count',
                   'retweet_count',
                   'original_author', 'followers_count', 'friends_count', 'possibly_sensitive', 'hashtags',
                   'user_mentions', 'place']

        created_at = self.find_created_time()
        source = self.find_source()
        text = self.find_full_text()
        polarity, subjectivity = self.find_sentiments(text)
        lang = self.find_lang()
        fav_count = self.find_favourite_count()
        retweet_count = self.find_retweet_count()
        screen_name = self.find_screen_name()
        follower_count = self.find_followers_count()
        friends_count = self.find_friends_count()
        sensitivity = self.is_sensitive()
        hashtags = self.find_hashtags()
        mentions = self.find_mentions()
        location = self.find_location()
        data = zip(created_at, source, text, polarity, subjectivity, lang, fav_count, retweet_count, screen_name,
                   follower_count, friends_count, sensitivity, hashtags, mentions, location)
        df = pd.DataFrame(data=data, columns=columns)

        if save:
            df.to_csv('processed_tweet_data.csv', index=False)
            print('File Successfully Saved.!!!')

        return df


if __name__ == "__main__":
    # required column to be generated you should be creative and add more features
    columns = ['created_at', 'source', 'original_text', 'clean_text', 'sentiment', 'polarity', 'subjectivity', 'lang',
               'favorite_count', 'retweet_count',
               'original_author', 'screen_count', 'followers_count', 'friends_count', 'possibly_sensitive', 'hashtags',
               'user_mentions', 'place', 'place_coord_boundaries']
    _, tweet_list = read_json("data/covid19.json")
    print(tweet_list[4])
    tweet = TweetDfExtractor(tweet_list)
    tweet_df = tweet.get_tweet_df()
    tweet_df.to_csv('output.csv')
    # use all defined functions to generate a dataframe with the specified columns above
