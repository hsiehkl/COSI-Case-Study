# https://medium.com/@apbetahouse45/asynchronous-web-scraping-in-python-using-concurrent-module-a5ca1b7f82e4

import sys

if __name__ == '__main__':    
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd
    import datetime
    from concurrent.futures import ThreadPoolExecutor, as_completed
    import time
    from db_multithreading import WikiDB

    if len(sys.argv) == 2:

        # variables setup
        year = str(sys.argv[1])

        # for parsing
        id_list = ["Events", "Births", "Deaths"]
        base_url = 'https://en.wikipedia.org/wiki/'
        daterange = pd.date_range('{}-01-01'.format(year), '{}-12-31'.format(year))

        # for database
        wiki_db = WikiDB(year)

        # generate urls
        URLs = []
        for i_date in range(len(daterange)):
            date = daterange[i_date]
            date_time = date.strftime("%Y-%m-%d")
            date_str = date.strftime("%B_%d")
            date_id = wiki_db.insert_date(date_time, date.year, date.month, date.day, date_str)
            url = base_url + date_str
            URLs.append((url, date_id))

        def parse(args):
            """parse and return extracted data"""
            url, date_id = args

            event_list = []
            birth_list = []
            death_list = []
            link_list = []

            response = requests.get(url=url)
            soup = BeautifulSoup(response.content, 'html.parser')
            for id in id_list:
                lis = soup.find(id=id).findNext("ul").find_all("li")
                for li in lis:
                    text = [x.strip() for x in li.text.split(" – ")]
                    links = li.find_all('a')

                    if text[0] == year:
                        pass
                        if id == "Events":
                            event = text[1]
                            event_list.append((date_id, event))
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
                                birth_list.append((date_id, person, description))
                            elif id == "Deaths":
                                death_list.append((date_id, person, description))

                        link_data = [(link.get('title'), link.get('href')) for link in links]
                        [link_list.append((date_id, data[0], data[1])) for data in link_data]
            return (event_list, birth_list, death_list, link_list)


        # parese information in mutiple threads for speeding up
        threads = 4
        with ThreadPoolExecutor(max_workers=threads) as executor:
            print("Start parsing with {} threads".format(threads))
            start = time.time()
            futures = [ executor.submit(parse, (url[0], url[1])) for url in URLs ]
            event_results = []
            birth_results = []
            death_results = []
            link_results = []
            for result in as_completed(futures):
                data = result.result()
                if data[0] != []:
                    [event_results.append(event) for event in data[0]]
                if data[1] != []:
                    [birth_results.append(birth) for birth in data[1]]
                if data[2] != []:
                    [death_results.append(death) for death in data[2]]

                [link_results.append(link) for link in data[3]]

            wiki_db.insert_event(event_results)
            wiki_db.insert_birth(birth_results)
            wiki_db.insert_death(death_results)
            wiki_db.insert_link(link_results)
            end = time.time()
            print("Time Taken: {:.6f}s".format(end-start))
