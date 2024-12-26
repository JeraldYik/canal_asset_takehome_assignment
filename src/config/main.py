from src.config.consts import *
from src.config.util import must_init
from src.util.util import singleton


@singleton
class Config:
    def __init__(self):
        self.IS_TWITTER_MOCK = bool(int(must_init(IS_TWITTER_MOCK_KEY)))
        print("IS_TWITTER_MOCK:", self.IS_TWITTER_MOCK)
        self.TWITTER_BEARER_TOKEN = must_init(TWITTER_BEARER_TOKEN_KEY)
        self.TWITTER_KEYWORDS = must_init(TWITTER_KEYWORDS_KEY).split(",")
        # Hashtag should be prepended with #
        self.TWITTER_HASHTAGS = must_init(TWITTER_HASHTAGS_KEY).split(",")
        self.TWITTER_MAX_RESULTS_PER_REQUEST = must_init(
            TWITTER_MAX_RESULTS_PER_REQUEST_KEY
        )
        self.TWITTER_RATE_LIMIT_IN_SECONDS = int(
            must_init(TWITTER_RATE_LIMIT_IN_SECONDS_KEY)
        )
        self.REDDIT_CLIENT_ID = must_init(REDDIT_CLIENT_ID_KEY)
        self.REDDIT_CLIENT_SECRET = must_init(REDDIT_CLIENT_SECRET_KEY)
        self.REDDIT_USERNAME = must_init(REDDIT_USERNAME_KEY)
        self.REDDIT_PASSWORD = must_init(REDDIT_PASSWORD_KEY)
        self.REDDIT_SUBREDDITS = must_init(REDDIT_SUBREDDITS_KEY).split(",")
        reddit_max_results_per_request = int(
            must_init(REDDIT_MAX_RESULTS_PER_REQUEST_KEY)
        )
        self.REDDIT_MAX_RESULTS_PER_REQUEST = (
            reddit_max_results_per_request if reddit_max_results_per_request else None
        )
        self.REDDIT_RATE_LIMIT_IN_SECONDS = int(
            must_init(REDDIT_RATE_LIMIT_IN_SECONDS_KEY)
        )


config = Config()

if __name__ == "__main__":
    pass
