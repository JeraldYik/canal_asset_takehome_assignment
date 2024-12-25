import asyncio
import logging

from src.service.reddit.main import Reddit
from src.service.twitter.main import Twitter

logging.basicConfig(level=logging.DEBUG, filename="app.log", force=True)


async def main():
    print("Script started. Logs are written to app.log")

    twitter = Twitter()
    reddit = Reddit()
    await asyncio.gather(
        twitter.fetch_latest_tweets_with_pagination(), reddit.fetch_all()
    )


if __name__ == "__main__":
    asyncio.run(main())
