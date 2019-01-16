import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from timeit import default_timer as timer
from urllib.parse import urlparse
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')
en_stops = set(stopwords.words('english'))

start_time = timer()
minutes_passed = 0
twitter_data = []
timed_twitter_data = []


def print_user_tweets_report(minutes_passed):

    if len(timed_twitter_data) <= 5:
        most_recent_twitter_data = timed_twitter_data
    else:
        most_recent_twitter_data = timed_twitter_data[-1:-6:-1]

    user_tweets_map = {}
    for data in most_recent_twitter_data:
        for tweet in data:
            user_id = tweet['user'].get('id')
            screen_name = tweet['user'].get('screen_name')
            name = tweet['user'].get('name')
            if user_id not in user_tweets_map.keys():
                user_tweets_map[user_id] = [screen_name, name, 1]
            else:
                user_tweets_map[user_id][2] += 1

    print("USER TWEETS REPORT AT MINUTE {}".format(minutes_passed))
    print('##################################################################')
    for key, value in user_tweets_map.items():
        print(value[0], ',', value[1], ',', value[2])
    print('##################################################################')


def print_links_report(minutes_passed):

    if len(timed_twitter_data) <= 5:
        most_recent_twitter_data = timed_twitter_data
    else:
        most_recent_twitter_data = timed_twitter_data[-1:-6:-1]

    total_link_count = 0
    unique_domains = {}
    for data in most_recent_twitter_data:
        for tweet in data:
            links = []
            for url in tweet['entities']['urls']:
                links.append(url['expanded_url'])
            total_link_count += len(links)
            for link in links:
                parsed_link = urlparse(link)
                domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_link)
                if domain not in unique_domains.keys():
                    unique_domains[domain] = 1
                else:
                    unique_domains[domain] += 1

    print("LINKS REPORT AT MINUTE {}".format(minutes_passed))
    print('##################################################################')
    print("Total links found:", total_link_count)
    for key, value in sorted(
            unique_domains.items(), key=lambda x: x[1], reverse=True):
        print(key, value)
    print('##################################################################')


def print_content_report(minutes_passed):

    if len(timed_twitter_data) <= 5:
        most_recent_twitter_data = timed_twitter_data
    else:
        most_recent_twitter_data = timed_twitter_data[-1:-6:-1]

    unique_words = set()
    word_count_map = {}
    for data in most_recent_twitter_data:
        for tweet in data:
            tweet_text = tweet['text']
            # remove stop words from tweet text
            filtered_tweet_words = []
            for word in tweet_text.split():
                if word not in en_stops:
                    filtered_tweet_words.append(word)
            filtered_tweet_text = ' '.join(filtered_tweet_words)

            for word in filtered_tweet_text.split():
                unique_words.add(word)
                if word not in word_count_map.keys():
                    word_count_map[word] = 1
                else:
                    word_count_map[word] += 1

    print("CONTENT REPORT AT MINUTE {}".format(minutes_passed))
    print('##################################################################')
    print("Unique words count:", len(unique_words))
    limit = 10
    for key, value in sorted(
            word_count_map.items(), key=lambda x: x[1], reverse=True):
        print(key, value)
        limit -= 1
        if not limit:
            break
    print('##################################################################')


# custom listener extending StreamListener
class MyStreamListener(StreamListener):

    def on_data(self, data):
        global start_time, twitter_data, timed_twitter_data, minutes_passed
        current_time = timer()
        elapsed_time = current_time - start_time
        if int(elapsed_time) > 60:
            minutes_passed += 1
            start_time = current_time
            timed_twitter_data.append(twitter_data)
            twitter_data = []
            print_user_tweets_report(minutes_passed)
            print_links_report(minutes_passed)
            print_content_report(minutes_passed)
        twitter_data.append(json.loads(data))
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    keyword = input("Enter keyword: ")
    # input credentials required to access twitter API
    access_token = input("Enter access token: ")
    access_token_secret = input("Enter access token secret: ")
    consumer_key = input("Enter consumer key: ")
    consumer_secret = input("Enter consumer secret: ")

    # twitter authentication and connection to twitter streaming API
    my_stream_listener = MyStreamListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, my_stream_listener)

    # filter twitter stream data by keyword
    stream.filter(track=[keyword])
