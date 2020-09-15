# https://www.freecodecamp.org/news/scraping-wikipedia-articles-with-python/

import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed
import time

class Scraper():

    def __init__(self, year):
        """initialize a scraper"""
        self.year = year
        self.base_url = 'https://en.wikipedia.org/wiki/'
        self.headers = {
            'user-agent': 
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
            }

    def parse(self, db):
        """parse and transform data into db"""
        id_list = ["Events", "Births", "Deaths"]

        year = self.year

        daterange = pd.date_range('{}-01-01'.format(year), '{}-12-31'.format(year))

        for i_date in range(len(daterange)):
            date = daterange[i_date]
            date_time = date.strftime("%Y-%m-%d")
            date_str = date.strftime("%B_%d")
            date_id = db.insert_date(date_time, date.year, date.month, date.day, date_str)

            url = self.base_url + date_str
            response = requests.get(url=url, headers=self.headers)
            soup = BeautifulSoup(response.content, 'html.parser')

            for id in id_list:
                lis = soup.find(id=id).findNext("ul").find_all("li")
                for li in lis:
                    text = [x.strip() for x in li.text.split(" – ")]
                    links = li.find_all('a')

                    if text[0] == year:
                        if id == "Events":
                            event = text[1]
                            db.insert_event(date_id, event)
                        else:
                            person = None
                            description = None
                            try:
                                person_description = text[1].split(", ")
                                if len(person_description) > 1:
                                    person, description = person_description[0], person_description[1]
                                else:
                                    person = person_description[0]
                            except:
                                print(text)

                            if id == "Births":
                                db.insert_birth(date_id, person, description)
                            elif id == "Deaths":
                                db.insert_death(date_id, person, description)

                            link_data = [(link.get('title'), link.get('href')) for link in links]
                            [db.insert_link(date_id, data[0], data[1]) for data in link_data]
        return