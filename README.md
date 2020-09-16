# COSI-Case-Study

## Task: 
Collect event, births, deaths data form [wikipedia](https://en.wikipedia.org/wiki/September_10) into a SQLite database for every day in a year. Handle it the way you would need to make use of it later.

## Package Requirements: 
```BeautifulSoup```

## Idea:
 * Creating tables that are easily joining and aggregating.

## Result:
Database of year 1990: [db](https://github.com/hsiehkl/COSI-Case-Study/blob/master/wikipedia1990.db)

* Can easily answer quesitons like: in which month most people die and born.
* Can find direct widipeida page by given title.

## Usage 1 (basic version):
Command: ```python run.py -YEAR```

Example: ```python run.py 1990```

Creating 5 tables:
* date table includes id, datetime, year, month, day, date_str columns
* event table includes id, date_id, event
* birth table includes id, date_id, person, description
* death table includes id, date_id, person, description
* link table includes id, date_id, title, link

Time taken: around 190s

## Usage 2 (mutil-thread version):
Command: ```python run_multithreading.py -YEAR```

Example: ```python run_multithreading.py 1990```

Creating 4 tables:
* date table includes id, datetime, year, month, day, date_str columns
* event table includes id, date_id, event
* birth table includes id, date_id, person, description
* death table includes id, date_id, person, description

Time taken: Around 75s
