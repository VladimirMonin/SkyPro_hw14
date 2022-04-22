from config import *
import sqlite3


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

        for year in range(finish, start-1, -1):  # Цикл по диапазону лет +1

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

        if category.lower() in RAITING_KATEGORIES.keys():
            results_list = []
            categorys_list = RAITING_KATEGORIES[category]
            query_str = ""

            for cat in categorys_list:
                category = '"'+cat+'" OR '
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

    def get_by_type_gengre_year(self, type, genre, year):
        sqlite_query = f"""
        
                    SELECT title, type, listed_in
                    FROM netflix
                    WHERE type = "{type}"
                    AND release_year = "{year}"
                    AND listed_in LIKE "%{genre}%"
                    
                        """
        result = self.get_sqlite_connection(sqlite_query)

        return result




dao = VideosDao()
search = dao.get_by_type_gengre_year('TV Show', 'Adventure', 2019)
print(search)


# Структура таблицы
# -----------------------
# show_id — id тайтла
# type — фильм или сериал
# title — название
# director — режиссер
# cast — основные актеры
# country — страна производства
# date_added — когда добавлен на Нетфликс
# release_year — когда выпущен в прокат
# rating — возрастной рейтинг
# duration — длительность
# duration_type — минуты или сезоны
# listed_in — список жанров и подборок
# description — краткое описание
# -----------------------