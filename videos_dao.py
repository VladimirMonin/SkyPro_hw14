from config import *
import sqlite3


class VideosDao:

    def __init__(self):
        self.sqlite_query = None

    def get_sqlite_connection(self):
        """Делает запрос с нужными параметрами
        параметры надо сформировать другими методами и передать через поле объекта self.sqlite_query"""
        with sqlite3.connect(DATA_BASE) as connection:
            cursor = connection.cursor()
            sqlite_query = self.sqlite_query
            result = cursor.execute(sqlite_query)
            return result.fetchall()

    def get_last_by_title(self, title):
        pass