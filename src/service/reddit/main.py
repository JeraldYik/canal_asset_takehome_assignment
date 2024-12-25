import asyncio
import atexit
import logging
import signal
import sys
from datetime import datetime, timezone

import asyncpraw

from src.config.main import config
from src.service.database.main import SOURCE_REDDIT, SocialMediaData, db
from src.util.util import singleton


@singleton
class Reddit:
    def __init__(self):
        self.client = asyncpraw.Reddit(
            client_id=config.REDDIT_CLIENT_ID,
            client_secret=config.REDDIT_CLIENT_SECRET,
            username=config.REDDIT_USERNAME,
            password=config.REDDIT_PASSWORD,
            user_agent=f"local:canal_asset:v1 (by u/{config.REDDIT_USERNAME})",
        )
        self.subreddits = config.REDDIT_SUBREDDITS
        self.max_results = config.REDDIT_MAX_RESULTS_PER_REQUEST

        def handle_interrupt(sig, frame):
            sys.exit(0)

        async def handle_exit():
            await self.client.close()
            logging.info("Reddit client closed")

        def sync_exit():
            asyncio.run(handle_exit())

        signal.signal(signal.SIGINT, handle_interrupt)
        atexit.register(sync_exit)

    async def fetch_all(self):
        """
        Fetch all subreddit posts in an asynchronous manner.
        """
        for subreddit_name in self.subreddits:
            await self._fetch(subreddit_name)

    async def _fetch(self, subreddit_name: str):
        subreddit = await self.client.subreddit(subreddit_name)
        try:
            # Generator function - returns an iterator
            async for post in subreddit.new(limit=self.max_results):
                idx, title, text, author, created_at = (
                    post.id,
                    post.title,
                    post.selftext,
                    post.author.name if post.author else "",
                    datetime.fromtimestamp(post.created_utc, timezone.utc),
                )
                logging.info(
                    "Subreddit '%s' post details idx=%s, title=%s, text=%s, author=%s, created_at=%s",
                    subreddit_name,
                    idx,
                    title,
                    text,
                    author,
                    created_at.isoformat(),
                )
                db.add_one(
                    SocialMediaData(
                        source=SOURCE_REDDIT,
                        data_id=idx,
                        text=f"<{title}> {text}",
                        author_id=author,
                        data_created_at=created_at,
                        input_data=subreddit_name,
                    )
                )
                await asyncio.sleep(config.REDDIT_RATE_LIMIT_IN_SECONDS)
        except Exception as e:
            logging.error("Reddit error=%s. Retrying...", e)
            await asyncio.sleep(10)
            await self._fetch(subreddit_name)
        finally:
            logging.info("Finished fetching posts from subreddit '%s'", subreddit_name)


if __name__ == "__main__":
    pass
