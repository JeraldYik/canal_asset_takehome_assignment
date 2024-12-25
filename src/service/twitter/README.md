# Twitter Service

## Documentation

https://developer.x.com/en/docs/x-api/tweets/lookup/introduction

## General Flow

1. Initialise twitter client, as well as desired keywords & hashtags, form and split into different requests, with query string of up to 512 in length (refer to `Twitter::_build_queries()`)
2. On every query string's first request, `next_token` would be empty. On subsequent request, should `meta.next_token` be present in previous response, use this value to continue querying.
3. After each request, save result to database (SQLite)
4. Any non-explicit errors from http response are retried

## Mocking

Due to various constraints pertaining to calling Twitter API via `tweepy`, there is an option to mock the HTTP call. Below listed are the constraints encountered:

https://developer.x.com/en/docs/x-api/rate-limits#v2-limits-free

- Limited number of posts for Free Tier (100 posts/month)
- Extremely tight rate-limit for Free Tier (One HTTP call every 24 hours)
- Each API call has to have a minumum of 10 posts per response, limiting the number of HTTP calls to at most 10
- `"GET /2/tweets/search/recent"` does not return `author_id` and `created_at` from SDK, though the raw HTTP responses do return these fields. Refer to `sample_response_http.json` for a sample response from this endpoint. Refer to `sample_response_http_to_sdk.log` for the difference between HTTP response & SDK response.
