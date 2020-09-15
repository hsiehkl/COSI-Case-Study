if __name__ == "__main__":
    from db import WikiDB
    import scraper
    import time

    start = time.time()
    year = '1990'
    wiki_db = WikiDB(year)
    scraper = scraper.Scraper(year)
    scraper.parse(wiki_db)
    wiki_db.close()

    end = time.time()
    print("Time Taken: {:.6f}s".format(end-start))