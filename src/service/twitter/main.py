import asyncio
import logging
from datetime import datetime
from time import time
from typing import Dict, List, NamedTuple, Tuple

from tweepy import Client

from src.config.main import config
from src.service.database.main import SOURCE_TWITTER, SocialMediaData, db
from src.util.util import singleton


# Response = namedtuple("Response", ("data", "includes", "errors", "meta"))
class Response(NamedTuple):
    data: List[Dict[str, any]]
    meta: Dict[str, any]
    includes: Dict[str, any]
    errors: Dict[str, any]


@singleton
class Twitter:
    def __init__(self):
        self.is_mock = config.IS_TWITTER_MOCK
        self.client = Client(bearer_token=config.TWITTER_BEARER_TOKEN)
        self.queries = self._build_queries(
            config.TWITTER_KEYWORDS, config.TWITTER_HASHTAGS
        )
        self.max_results = config.TWITTER_MAX_RESULTS_PER_REQUEST
        self.rate_limit_in_sec = config.TWITTER_RATE_LIMIT_IN_SECONDS

    async def fetch_latest_tweets_with_pagination(self):
        """
        Queries are not ran in an asynchronous fashion to simplify flow & rate limiting.

        An enhancement would be to implement asychronous logic, and test with Twitter developer account of higher tier.
        """
        for query in self.queries:
            tweets, next_token = self._fetch_latest_tweets_using_query_with_pagination(
                query, next_token=None
            )
            db.bulk_insert(tweets)
            while next_token:
                await asyncio.sleep(self.rate_limit_in_sec)
                tweets, next_token = (
                    self._fetch_latest_tweets_using_query_with_pagination(
                        query, next_token=next_token
                    )
                )
                db.bulk_insert(tweets)

    def _fetch_latest_tweets_using_query_with_pagination(
        self, query: str, next_token: str | None = None
    ) -> Tuple[List[SocialMediaData], str]:
        """
        tweepy::search_recent_tweets() returns Tweets from the last 7 days that match a search query.

        7 days is the assumption made for latest results

        Sample response from documentation: https://developer.x.com/en/docs/x-api/tweets/search/api-reference/get-tweets-search-recent#tab1

        Or view sample_response_http.json for actual HTTP response.
        """
        logging.info("Twitter query=%s", query)
        try:
            if self.is_mock:
                resp = self._mock_call(query)
            else:
                resp = self.client.search_recent_tweets(
                    query=query,
                    max_results=self.max_results,
                    # https://developer.x.com/en/docs/x-api/data-dictionary/object-model/tweet
                    # Header in HTTP request tweet.fields=id,text,author_id,created_at
                    tweet_fields=[
                        "id",
                        "text",
                        "author_id",
                        "created_at",
                    ],
                    next_token=next_token,
                )
            logging.info("Twitter resp=%s", resp)

            if resp.errors:
                logging.error("Twitter errors=%s", resp.errors)
                return [], None

            next_token = resp.meta.get("next_token", None)
            if not resp.data:
                return None, next_token

            def form_data_created_at(raw) -> datetime:
                if isinstance(raw, datetime):
                    return raw
                if isinstance(raw, str):
                    return datetime.fromisoformat(raw)
                return datetime.fromtimestamp("1970-01-01T00:00:00Z")

            return [
                SocialMediaData(
                    source=SOURCE_TWITTER,
                    data_id=d.get("id", ""),
                    text=d.get("text", ""),
                    author_id=d.get("author_id", ""),
                    data_created_at=form_data_created_at(
                        d.get("created_at", "1970-01-01T00:00:00Z")
                    ),
                    input_data=query,
                )
                for d in resp.data
            ], next_token

        # non-explicit error (exception). return next_token to retry
        except Exception as e:
            logging.error("Twitter error=%s", e)
            return [], next_token

    def _build_queries(self, keywords: List[str], hashtags: List[str]) -> List[str]:
        """
        https://developer.x.com/en/docs/x-api/tweets/search/integrate/build-a-query

        If you have Basic or Pro access, your query can be 512 characters long for recent search endpoint.

        If you have Pro access, your query can be 1,024 characters long for full archive search endpoint.

        We will limit our query to 512 characters, where we will build in a greedy fashion.
        """
        MAX_LENGTH = 512
        queries = []
        # Example: keyword OR #hashtag ...
        current_query = ""
        for keyword in keywords:
            if len(current_query) + 4 + len(keyword) > MAX_LENGTH:
                queries.append(current_query)
                current_query = keyword
            else:
                current_query += f" OR {keyword}" if current_query else keyword
        for hashtag in hashtags:
            if not hashtag.startswith("#"):
                raise ValueError("Hashtag does not start with #")
            if len(current_query) + 4 + len(hashtag) > MAX_LENGTH:
                queries.append(current_query)
                current_query = hashtag
            else:
                current_query += f" OR {hashtag}" if current_query else hashtag
        return queries + [current_query]

    def _mock_call(self, query: str) -> Response:
        """
        Due to Twitter's strict limit on number of posts retrieved per month

        (100/month - which is extremely little, especially when minimum results per HTTP call is 10),

        This mocking function would allow us to test the Twitter calls without actually making the actual HTTP request.

        In our mock response, next_token is always returned, hence there will be no end to our script unless explicitly killed with exit 1 signal.
        """
        return Response(
            meta={"next_token": "next_token"},
            data=[
                {
                    "id": f"id_{time()}",
                    "text": query,
                    "author_id": "123456789",
                    "created_at": "2021-03-19T19:59:10.000Z",
                }
            ],
            includes=None,
            errors=None,
        )


if __name__ == "__main__":
    pass
