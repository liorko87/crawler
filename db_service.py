import sqlite3


class DbService:
    def __init__(self):
        try:
            self.conn = sqlite3.connect('pastebin.db', check_same_thread=False)
            self.cursor = self.conn.cursor()
            sqlite_create_table_query = '''CREATE TABLE IF NOT EXISTS pastebinData (
                                url text PRIMARY KEY,
                                username TEXT NOT NULL,
                                title text NOT NULL,
                                creation_date datetime,
                                content text NOT NULL);'''
            print("Successfully Connected to SQLite")
            self.cursor.execute(sqlite_create_table_query)
            self.conn.commit()
            print("SQLite table created")

        except sqlite3.Error as error:
            print("Error while creating a sqlite table", error)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    def insert_data(self, data):
        try:
            sqlite_insert_query = f'''
                                         Insert INTO `pastebinData`
                                         (url, username, title, creation_date, content)
                                         VALUES (?, ?, ?, ?, ?)
                                         '''
            self.cursor.execute(sqlite_insert_query, (data.url, data.username, data.title,
                                                              data.creation_date, data.content))
            self.conn.commit()

        except sqlite3.Error as error:
            print("Error while inserting data", error)

