# Twitter Service

## Documentation

https://docs.tweepy.org/en/stable/client.html#tweet-lookup

https://developer.x.com/en/docs/x-api/tweets/lookup/introduction

## General Flow

`tweepy` is a wrapper SDK that interacts with the Twitter API endpoint. `tweepy` only responsible for formation of requests and responses to and from Twitter API respectively. It is not responsible for rate-limiting and error handling. It is not stated that we have to manually close the client, since the SDK only assists with HTTP requests on-demand.

1. Initialise twitter client, as well as desired keywords & hashtags, form and split into different requests, with query string of up to 512 in length (refer to `twitter._build_queries()`)
2. On every query string's first request, `next_token` would be empty. On subsequent request, should `meta.next_token` be present in previous response, use this value to continue querying.
3. After each request, save result to database (SQLite)
4. Any non-explicit errors from http response are retried

## Mocking

Due to various constraints pertaining to calling Twitter API via `tweepy`, there is an option to mock the HTTP call (`IS_TWITTER_MOCK` env variable). Below listed are the constraints encountered:

https://developer.x.com/en/docs/x-api/rate-limits#v2-limits-free

- Limited number of posts for Free Tier (100 posts/month)
- Extremely tight rate-limit for Free Tier (One HTTP call every 24 hours)
- Each API call has to have a minumum of 10 posts per response, limiting the number of HTTP calls to at most 10 per month, once per day.
- Refer to `sample_response_http.json` for a sample response from this endpoint.
