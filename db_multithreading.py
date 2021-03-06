import sqlite3

class WikiDB:

    def __init__(self, year):
        db_name = "wikipedia" + year + '.db'
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.build()

    def build(self):
        try:
            self.create_wikipedia_tables()
        except:
            self.drop_wikipedia_tables()
            self.create_wikipedia_tables()

    def close(self):
        """close sqlite3 connection"""
        self.connection.close()

    def create_wikipedia_tables(self):
        self.cursor.execute("""CREATE TABLE date(
                        id INTEGER PRIMARY KEY NOT NULL,
                        datetime DATETIME NOT NULL,
                        year INTEGER NOT NULL,
                        month INTEGER NOT NULL,
                        day INTEGER NOT NULL,
                        date_str VARCHAR(45) NOT NULL)""")
        self.cursor.execute("""CREATE TABLE event(
                        id INTEGER NOT NULL PRIMARY KEY,
                        date_id INTEGER NOT NULL,
                        event VARCHAR(255) NOT NULL, 
                        FOREIGN KEY(date_id) REFERENCES date(id))""")
        self.cursor.execute("""CREATE TABLE birth(
                        id INTEGER NOT NULL PRIMARY KEY,
                        date_id INTEGER NOT NULL,
                        person VARCHAR(255) NOT NULL, 
                        description VARCHAR(255) NULL, 
                        FOREIGN KEY(date_id) REFERENCES date(id))""")
        self.cursor.execute("""CREATE TABLE death(
                        id INTEGER NOT NULL PRIMARY KEY,
                        date_id INTEGER NOT NULL,
                        person VARCHAR(255) NOT NULL, 
                        description VARCHAR(255) NULL, 
                        FOREIGN KEY(date_id) REFERENCES date(id))""")
        self.cursor.execute("""CREATE TABLE link(
                        id INTEGER NOT NULL PRIMARY KEY,
                        date_id INTEGER NOT NULL,
                        title VARCHAR(255) NOT NULL, 
                        link VARCHAR(255) NULL, 
                        FOREIGN KEY(date_id) REFERENCES date(id))""")

    def drop_wikipedia_tables(self):
        self.cursor.execute("DROP TABLE date")
        self.cursor.execute("DROP TABLE event")
        self.cursor.execute("DROP TABLE birth")
        self.cursor.execute("DROP TABLE death")
        self.cursor.execute("DROP TABLE link")

    def insert_date(self, datetime, year, month, day, date_str):
        params = (datetime, year, month, day, date_str)
        self.cursor.execute("INSERT INTO date VALUES (NULL, ?, ?, ?, ?, ?)", params)
        date_id = self.cursor.lastrowid
        self.connection.commit()
        return date_id

    def insert_event(self, events):
        sql_data = tuple((None,) + a for a in events)
        self.cursor.executemany("INSERT INTO event VALUES (?, ?, ?)", sql_data)
        event_id = self.cursor.lastrowid
        self.connection.commit()
        return event_id

    def insert_birth(self, births):
        sql_data = tuple((None,) + a for a in births)
        self.cursor.executemany("INSERT INTO birth VALUES (?, ?, ?, ?)", sql_data)
        event_id = self.cursor.lastrowid
        self.connection.commit()
        return event_id

    def insert_death(self, deaths):
        sql_data = tuple((None,) + a for a in deaths)
        self.cursor.executemany("INSERT INTO death VALUES (?, ?, ?, ?)", sql_data)
        event_id = self.cursor.lastrowid
        self.connection.commit()
        return event_id

    def link_exist(self, value):
        """check if a link already existed"""
        if value:
            self.cursor.execute("SELECT title FROM link WHERE title=?", (value, ))
            result = self.cursor.fetchone()
            if result:
                return True
            else:
                return False
        else:
            return True

    def insert_link(self, links):
        for link in links:
            value = link[1]
            existed = self.link_exist(value)
            if not existed:
                self.cursor.execute("INSERT INTO link VALUES (NULL, ?, ?, ?)", link)
                event_id = self.cursor.lastrowid
                self.connection.commit()
