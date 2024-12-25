# Run this first to build the virtual environment
setup:
	python3 -m venv venv && source venv/bin/activate && export PYTHONPATH=./ && pip3 install -r requirements.txt

# Command to run the main script. Script should not terminate on its own, instead can only terminate on Ctrl-C
run:
	rm -f local.db && rm -f app.log && touch app.log && source env/.env && python3 main.py

# Only run this command after main script is run (main script can be still running or killed)
db:
	python3 src/service/database/query.py

db_twitter:
	python3 src/service/database/query.py --source twitter

db_reddit:
	python3 src/service/database/query.py --source reddit

 