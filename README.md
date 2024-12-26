# Take-Home Project: Social Media Data Scraper

## Objective

Develop a solution that continuously scrapes the latest data from Twitter and Reddit, storing it in a local database.

## Requirements

### Data Collection

#### Sources

Extract tweets using specific keywords/hashtags from Twitter and posts from specified subreddits on Reddit.

#### Tools

Suggested libraries include `Tweepy` for Twitter and `PRAW` for Reddit

### Data Storage

#### Database

Store data in a local relational database (e.g. SQLite)

#### Schema

Tables should include fields for `content`, `timestamp`, `author details` and `identifiers`

### Technical Specifications

#### Error Handling

Manage issues like `rate limits` and `connection losses`

#### Logging

Implement logging for tracking scraper activities

### Documentation

#### Content

Provide examples of database query and data scraping

## Comments from submitter

Refer to the `README.md` in the individual subfolders of `src/service` to view comments.

Refer to `Makefile` to view the executable commands.

Add `env/.env` environment variables, following the template defined in `env/template.env`.

Refer to `/sample_logs` for logs without running the main script.
