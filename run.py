import sys
if __name__ == "__main__":
    from db import WikiDB
    from scraper import Scraper
    import time

    if len(sys.argv) == 2:

        # get year arguement
        year=str(sys.argv[1])

        start = time.time()

        # init a db includes tables
        wiki_db = WikiDB(year)

        # init a scraper for getting data from wekipeida
        scraper = Scraper(year)

        # parse data into db
        scraper.parse(wiki_db)

        # close db
        wiki_db.close()

        end = time.time()
        print("Time Taken: {:.6f}s".format(end-start))