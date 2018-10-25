import json
import redis
from tweet import Tweet

class TweetStore:

    # Redis Configuration
    redis_host = "localhost"
    redis_port = 6379
    redis_password = ""

    # Tweet Configuration
    redis_key = 'tweets'
    num_tweets = 20
    trim_threshold = 100

    def __init__(self):
        self.db = r = redis.Redis(
            host=self.redis_host,
            port=self.redis_port,
            password=self.redis_password
        )
        self.trim_count = 0

    def tweets(self, limit=15):
        tweets = []

        for item in self.db.lrange(self.redis_key, 0, limit-1):
            tweet_obj = json.loads(item)
            tweets.append(Tweet(tweet_obj))

        return tweets

    def push(self, data):
        self.db.lpush(self.redis_key, json.dumps(data))
        self.trim_count += 1

        # Periodically trim the list so it doesn't grow too large.
        if self.trim_count > 100:
            self.db.ltrim(self.redis_key, 0, self.num_tweets)
            self.trim_count = 0
