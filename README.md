# COSI-Case-Study

## Task: 
Collect event, births, deaths data form [wikipedia](https://en.wikipedia.org/wiki/September_10) into a SQLite database for every day in a year. Handle it the way you would need to make use of it later.

## Package Requirements: 
```BeautifulSoup```

## Idea:
 * Creating tables that are easily joining and aggregating.

## Result:
Handy impletementing code for buliding db with a given year.
Example result: Database of year 1990, [wikipedia1990](https://github.com/hsiehkl/COSI-Case-Study/blob/master/wikipedia1990.db)

There are 5 tables:
* date table includes id, datetime, year, month, day, date_str columns
* event table includes id, date_id, event
* birth table includes id, date_id, person, description
* death table includes id, date_id, person, description
* link table includes id, date_id, title, link

With this db:
* Can easily answer quesitons like: in which month most people have died and borned.
* Can find direct widipeida link by given keyword.

## Usage 1 (basic version):
Command: ```python run.py -YEAR```

Example: ```python run.py 1990```

Time taken: around 190s

## Usage 2 (multi-thread version):
Command: ```python run_multithreading.py -YEAR```

Example: ```python run_multithreading.py 1990```

Time taken: around 75s
