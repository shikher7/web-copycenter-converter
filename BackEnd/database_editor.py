import datetime
import sqlite3


class DataBaseEditor:
    def __init__(self):
        self.connection = sqlite3.connect('users_key_files.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute("""PRAGMA foreign_keys=on;""")
        self.__create_users_table()
        self.__create_user_attribute()
        self.__create_printers_table()
        self.__create_selected_printers()
        self.__clear_tables_where_date_some_older()
        # self.__delete_all()

    def __create_users_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users (ID INTEGER PRIMARY KEY UNIQUE NOT NULL,
                                                     user_id INTEGER,
                                                     row_id INTEGER NOT NULL,
                                                     FOREIGN KEY (row_id) REFERENCES users_has_files(ID),
                                                     FOREIGN KEY (user_id) REFERENCES users_has_printers(user_id));""")
        self.connection.commit()

    def __create_user_attribute(self):
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS users_has_files (
                                                                        ID INTEGER PRIMARY KEY UNIQUE NOT NULL,
                                                                        printer_options TEXT DEFAULT '',
                                                                        receipt decimal(10, 2) NOT NULL,
                                                                        file_path TEXT NOT NULL,
                                                                        file_type TEXT NOT NULL,
                                                                        request_time TIMESTAMP NOT NULL,
                                                                        request_date DATE NOT NULL
                                                                        );
                            """)
        self.connection.commit()

    def __create_printers_table(self):
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS printers (
                                                                ID INTEGER PRIMARY KEY UNIQUE NOT NULL,
                                                                printer_name TEXT NOT NULL,
                                                                IP_ADDRES TEXT NOT NULL,
                                                                cost_by_list decimal(10, 2) NOT NULL,
                                                                city TEXT NOT NULL,
                                                                street TEXT NOT NULL,
                                                                house INTEGER NOT NULL,
                                                                printer_mark TEXT NOT NULL,
                                                                option_of_print INTEGER(1) DEFAULT 0
                                                                );
                            """)
        self.connection.commit()

    def __create_selected_printers(self):
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS users_has_printers (
                                                                          ID INTEGER PRIMARY KEY NOT NULL UNIQUE,
                                                                          user_id INTEGER,
                                                                          printer_id INTEGER,
                                                                      FOREIGN KEY (printer_id) REFERENCES printers(ID)
                                                                          );
                            """)

    def __clear_tables_where_date_some_older(self, max_days=2):
        self.cursor.execute("""
                            SELECT request_date from users_has_files;
                            """)
        dates = self.cursor.fetchall()
        deleted_dates = [date[0] for date in dates if
                         (datetime.datetime.now() - datetime.datetime.strptime(date[0], "%d.%m.%y")).days > max_days]
        for date in deleted_dates:
            self.cursor.execute(f"""
                                DELETE FROM users where request_date=?;
                                """, (date,))
            self.connection.commit()

    def insert_into_users(self, row_id, user_id, file_type, price, date):
        self.cursor.execute("""
                            INSERT INTO users (user_id, file_type, price, request_date, row_id) VALUES (?, ?, ?, ?, ?);
                            """, (user_id, file_type, price, date, row_id))
        self.connection.commit()

    def insert_into_users_has_files(self, values):
        self.cursor.execute("""
                            INSERT INTO users_has_files VALUES (?, ?, ?, ?, ?)
                            """, values)


if __name__ == '__main__':
    obj = DataBaseEditor()
    connection = sqlite3.connect('users_key_files.db')
    cur = connection.cursor()
    # cur.execute("""DROP TABLE users""")
    # cur.execute("""DROP TABLE users_has_files""")
    # cur.execute("""DROP TABLE printers""")
