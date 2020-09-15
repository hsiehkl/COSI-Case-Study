# COSI-Case-Study

Task: Collect event, births, deaths data form [wikipedia](https://en.wikipedia.org/wiki/September_10) into a SQLite database for every day in a year. Handle it the way you would need to make use of it later.

Package Requirements: ```BeautifulSoup```

Idea: Creating tables that are easily joining and aggrating.

## Usage 1 (basic version):
```python run.py -YEAR```

example: ```python run.py 1990```

Resut:

Creating 5 tables:
* date table includes id, datetime, year, month, day, date_str columns
* event table includes id, date_id, event
* birth table includes id, date_id, person, description
* death table includes id, date_id, person, description
* link table includes id, date_id, title, link

Time taken: Around 190s

## Usage 2 (mutil-thread version):
```python run_multithreading.py -YEAR```

example: ```python run_multithreading.py 1990```

Resut:

Creating 4 tables:
* date table includes id, datetime, year, month, day, date_str columns
* event table includes id, date_id, event
* birth table includes id, date_id, person, description
* death table includes id, date_id, person, description

Time taken: Around 75s
