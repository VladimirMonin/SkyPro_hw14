from config import *
import sqlite3
import json


class VideosDao:

    def get_sqlite_connection(self, sqlite_query):
        """Делает запрос с нужными параметрами
        параметры надо сформировать другими методами и передать через поле объекта self.sqlite_query"""
        with sqlite3.connect(DATA_BASE) as connection:
            cursor = connection.cursor()
            sqlite_query = sqlite_query
            result = cursor.execute(sqlite_query)
            return result.fetchall()

    def get_last_by_title(self, title):
        """Поиск по названию. Если таких фильмов несколько, выводит самый свежий.
         Возвращает данные в виде словаря"""

        sqlite_query = f"""
                SELECT title, country, MAX(release_year), listed_in, description
                FROM netflix
                WHERE title LIKE "%{title}%"
                LIMIT 1

        """
        result = self.get_sqlite_connection(sqlite_query)

        film_dict = {}
        for film in result:
            film_dict['title'] = film[0]
            film_dict['country'] = film[1]
            film_dict['release_year'] = film[2]
            film_dict['genre'] = film[3]
            film_dict['description'] = film[4].strip('\n')

        return film_dict

    def get_film_by_years_range(self, start, finish):
        """Поиск по диапазону лет. На каждый год ограничение выдачи не более 100 тайтлов"""

        start = int(start)  # Интуем
        finish = int(finish)

        results_list = []

        for year in range(finish, start - 1, -1):  # Цикл по диапазону лет +1

            sqlite_query = f"""
                        
                        SELECT title, release_year
                        FROM netflix
                        WHERE release_year = {year}
                        LIMIT 100
                            """
            result = self.get_sqlite_connection(sqlite_query)  # Для 1 года - 1 запрос

            for film in result:
                film_dict = {}
                film_dict['title'] = film[0]
                film_dict['release_year'] = film[1]
                results_list.append(film_dict)

        return results_list

    def get_rating_by_category(self, category):
        """Поиск фильмов по запутанным американским рейтингам возрастных категорий (категории в конфиге)"""

        if category.lower() in RAITING_KATEGORIES.keys():
            results_list = []
            categorys_list = RAITING_KATEGORIES[category]
            query_str = ""

            for cat in categorys_list:  # Возможно для этого есть более простой способ?
                category = '"' + cat + '" OR '
                query_str += category

            query_str = query_str.rstrip(' OR')

            sqlite_query = f"""
            SELECT title, rating, description
            FROM netflix
            WHERE rating = {query_str}
            """

            result = self.get_sqlite_connection(sqlite_query)

            for film in result:
                film_dict = {}
                film_dict['title'] = film[0]
                film_dict['rating'] = film[1]
                film_dict['description'] = film[2].strip('\n')
                results_list.append(film_dict)

            return results_list

        else:
            return {'Оповещение!': 'Категории не существует. Но тут могла быть ваша реклама :)'}

    def get_10fresh_by_genre(self, genre):
        """Возвращает самые свежие 10 фильмов жанра"""
        genre = str(genre)
        sqlite_query = f"""
                   SELECT title, description
                   FROM netflix
                   WHERE listed_in LIKE "%{genre}%"
                   ORDER BY release_year DESC
                   LIMIT 10
                   """
        result = self.get_sqlite_connection(sqlite_query)

        results_list = []
        for film in result:
            film_dict = {}
            film_dict['title'] = film[0]
            film_dict['description'] = film[1].strip('\n')
            results_list.append(film_dict)

        return results_list

    def get_json_dumps(self, data):
        """Делает json_dumps того, что в неё передадут"""
        result = json.dumps(data, ensure_ascii=False, indent=4)
        return result

    def get_friendly_acting_team(self, name1, name2):
        """Получает пару актеров и ищет тех кто играл с ними 2 и более раз"""
        sqlite_query = f"""

                    SELECT "cast"
                    FROM netflix
                    WHERE "cast" LIKE "%{name1}%"
                    AND "cast" LIKE "%{name2}%"

                        """
        result = self.get_sqlite_connection(sqlite_query)

        buffer_list = []
        for film in result:
            for actor in film[0].split(', '):
                if actor not in [name1, name2]:
                    buffer_list.append(actor)

        result_dict = {}
        for actor in buffer_list:
            played_count = buffer_list.count(actor)
            if played_count >= 2:
                result_dict[actor] = played_count
        return self.get_json_dumps(result_dict)

    def get_by_type_genre_year(self, type, genre, year):
        """Получает жанр тип и год и возвращает подборку фильмов/сериалов"""
        sqlite_query = f"""
        
                    SELECT title, type, listed_in
                    FROM netflix
                    WHERE type = "{type}"
                    AND release_year = "{year}"
                    AND listed_in LIKE "%{genre}%"
                    
                        """
        result = self.get_sqlite_connection(sqlite_query)

        return self.get_json_dumps(result)

