import sqlite3

class DbService:
    def __init__(self):
        try:
            self.sqliteConnection = sqlite3.connect('pastebin.db')
            sqlite_create_table_query = '''CREATE TABLE pastebinData (
                                url text PRIMARY KEY,
                                username TEXT NOT NULL,
                                title text NOT NULL UNIQUE,
                                pastebin_date datetime,
                                content text NOT NULL);
                                '''
            self.cursor = self.sqliteConnection.cursor()
            print("Successfully Connected to SQLite")
            self.cursor.execute(sqlite_create_table_query)
            self.sqliteConnection.commit()
            print("SQLite table created")

            self.cursor.close()

        except sqlite3.Error as error:
            print("Error while creating a sqlite table", error)
    

    def insert_data(self, url, username, title, date, content):
        sqlite_insert_query = f'''
                              Insert INTO `pastebinData`
                              (url, username, title, pastebin_date, content)
                              VALUES
                              ({url}, {username}, {title}, {date}, {content})
                              '''
        
        self.cursor = self.sqliteConnection.cursor()
        count = self.cursor.execute(sqlite_insert_query)
        self.sqliteConnection.commit()
        print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)
        self.cursor.close()
        