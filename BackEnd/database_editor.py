import datetime
import logging
import sqlite3


class DataBaseEditor:
    def __init__(self):
        logging.getLogger().setLevel(logging.INFO)
        try:
            self.connection = sqlite3.connect('../users_key_files.db')
            cursor = self.connection.cursor()
            logging.info("""!!! База данных успешно подключена !!!""")
            cursor.execute("select sqlite_version();")
            sqlite_version = cursor.fetchall()
            logging.info("""!!! Версия sqlite - {} !!!""".format(sqlite_version[0][0]))
            cursor.close()
        except sqlite3.Error as SQLiteError:
            logging.warning("""!!! Ошибка подключения к SQLite !!!""", SQLiteError)
        self.__create_tables_if_not_exists()
        self.__clear_tables_where_date_some_older()

    def __create_tables_if_not_exists(self):
        cursor = self.connection.cursor()
        cursor.execute("""PRAGMA foreign_keys=on;""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS users_has_files (
                                                                        ID INTEGER PRIMARY KEY UNIQUE NOT NULL,
                                                                        printer_options TEXT DEFAULT '',
                                                                        pages_count INTEGER NOT NULL,
                                                                        file_path TEXT NOT NULL,
                                                                        file_type TEXT NOT NULL,
                                                                        request_time TIMESTAMP NOT NULL,
                                                                        request_date DATE NOT NULL
                                                                        );
                            """)

        cursor.execute("""CREATE TABLE IF NOT EXISTS users (ID INTEGER PRIMARY KEY UNIQUE NOT NULL,
                                                     user_id INTEGER,
                                                     row_id INTEGER NOT NULL,
                                                     FOREIGN KEY (row_id) REFERENCES users_has_files(ID));""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS printers (
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

        cursor.execute("""CREATE TABLE IF NOT EXISTS users_has_printers (
                                                                        ID INTEGER PRIMARY KEY NOT NULL UNIQUE,
                                                                        user_id INTEGER,
                                                                        printer_id INTEGER,
                                                                      FOREIGN KEY (user_id) REFERENCES users(user_id),
                                                                      FOREIGN KEY (printer_id) REFERENCES printers(ID)
                                                                          );
                                    """)
        self.connection.commit()
        cursor.close()

    def __clear_tables_where_date_some_older(self, max_days=2):
        cursor = self.connection.cursor()
        cursor.execute("""
                            SELECT request_date from users_has_files;
                            """)
        dates = cursor.fetchall()
        deleted_dates = [date[0] for date in dates if
                         (datetime.datetime.now() - datetime.datetime.strptime(date[0], "%Y-%m-%d")).days > max_days]
        for date in deleted_dates:
            cursor.execute(f"""
                                DELETE FROM users_has_files where request_date=?;
                                """, (date,))
            self.connection.commit()
        cursor.close()

    def get_last_id_into_users_has_files(self):
        cursor = self.connection.cursor()
        cursor.execute("""
                            SELECT max(ID) from users_has_files;
                            """)
        max_id = cursor.fetchone()
        cursor.close()
        if max_id[0] is None:
            return 0
        return int(max_id[0])

    def insert_user(self, user_id, values):
        cursor = self.connection.cursor()
        cursor.execute("""
                            INSERT INTO users_has_files (ID, printer_options, pages_count, file_path,
                                                        file_type, request_time, request_date) VALUES
                                                        (?, ?, ?, ?, ?, ?, ?);
                            """, values)
        self.connection.commit()
        row_id = values[0]
        cursor.execute("""
                            INSERT INTO users (user_id, row_id) VALUES (?, ?);
                            """, (user_id, row_id))
        self.connection.commit()
        cursor.close()
        self.close_connection()

    def check_city_isinstance(self, city):
        city = f'%{city[0].upper()}{city[1:].lower()}%'
        cursor = self.connection.cursor()
        cursor.execute("""
                            SELECT city from printers where city like ?
                            """, (city,))
        if cursor.fetchone() is not None:
            cursor.close()
            return True
        cursor.close()
        return None

    def get_all_houses_of_street(self, street, city):
        city = f'%{city[0].upper()}{city[1:].lower()}%'
        street = f'%{street[0].upper()}{street[1:].lower()}%'
        cursor = self.connection.cursor()
        cursor.execute("""select house from printers where city like ? and street like ?""", (city, street))
        houses = cursor.fetchall()
        cursor.close()
        if houses:
            houses = [x[0] for x in houses]
            return houses
        return None

    def get_printer_by_location(self, location):
        cursor = self.connection.cursor()
        cursor.execute("""
                        select ID from printers where city=? and street=? and house=?;
                        """, location)
        printer_id = cursor.fetchall()
        if printer_id:
            return printer_id[0][0]
        return None

    def get_all_coords_of_printers_location(self):
        cursor = self.connection.cursor()
        cursor.execute("""select x_coordinate, y_coordinate from printers;""")
        coords = cursor.fetchall()
        cursor.close()
        return coords

    def get_printer_info_by_coords(self, best_coords):
        cursor = self.connection.cursor()
        cursor.execute("""
                        select ID, street, house, printer_mark from printers where x_coordinate=? and y_coordinate=?;
                        """, best_coords)
        printer_info = cursor.fetchall()
        printer_info = dict(printer_id=printer_info[0][0],
                            street=printer_info[0][1],
                            house=printer_info[0][2],
                            printer_mark=printer_info[0][3])
        cursor.close()
        return printer_info

    def get_printer_info_by_id(self, printer_id):
        cursor = self.connection.cursor()
        cursor.execute("""select street, house, printer_mark from printers where ID=?""", (printer_id,))
        printer_info = cursor.fetchall()
        printer_info = dict(street=printer_info[0][0],
                            house=printer_info[0][1],
                            printer_mark=printer_info[0][2])
        cursor.close()
        return printer_info

    def check_printer_is_exists(self, user_printer_id):
        cursor = self.connection.cursor()
        cursor.execute("""
                        select ID from printers where ID = ?;
                        """, (user_printer_id,))
        printer_is_exists = cursor.fetchone()
        cursor.close()
        if printer_is_exists is not None:
            return printer_is_exists[0]
        return printer_is_exists

    def get_favorite_printers_by_users(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("""
                        select printer_id from users_has_printers where user_id=?;
                        """, (user_id, ))
        indexes_of_printers = cursor.fetchall()
        cursor.close()
        if indexes_of_printers:
            return [x[0] for x in indexes_of_printers]
        return None

    def close_connection(self):
        self.connection.close()


if __name__ == '__main__':
    obj = DataBaseEditor()
    print(obj.get_printer_info_by_coords((1, 2)))
