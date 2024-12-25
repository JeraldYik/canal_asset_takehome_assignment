# Database (local file-based SQLite)

Using SQLalchemy as the ORM to access SQLite database

When main script is run, database is first destroyed and then re-created. Even when main script is killed, the database still persists as a local file.

Use the `make db*` commands to query the database on data source

- `make db` to query all rows
- `make db_twitter` to query all rows from twitter
- `make db_reddit` to query all rows from reddit
