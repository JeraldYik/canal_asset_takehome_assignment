# Reddit Service

## Documentation

Using `asyncpraw` instead of `praw` due to asynchronous nature of the script, as recommended by documentation.

https://praw.readthedocs.io/en/latest/getting_started/multiple_instances.html#discord-bots-and-asynchronous-environments

https://asyncpraw.readthedocs.io/en/stable/getting_started/authentication.html

## General flow

`asyncpraw`/`praw` is a wrapper SDK that interacts with the Reddit API endpoint. `asyncpraw`/`praw` assists with authentication, formation of requests and responses to and from Reddit API respectively, as well as rate-limiting. It is recommended to close the client when the program is tearing down.

1. Initialise reddit client, as well as desired subreddits.
2. Each subreddit query request is run asynchronously.
3. `asyncpraw`/`praw` handles rate limit automatically, however we can still add our own rate limit value for greater control
4. Any non-explicit errors from http response are retried

## Mocking

https://www.reddit.com/r/redditdev/comments/1727p7b/how_many_posts_or_comments_can_i_retrieve_with/

Mocking is not necessary in this implementation, since Reddit is more lenient with their API rate & call limits. However, we can implement mocking for testing purposes in the future.
