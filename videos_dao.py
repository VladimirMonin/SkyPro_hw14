from config import *
import sqlite3


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
        title_sqlite = '"' + "%" + str(title) + "%" + '"'
        sqlite_query = f"""
                SELECT title, country, MAX(release_year), listed_in, description
                FROM netflix
                WHERE title LIKE {title_sqlite}
                        
        """
        result = self.get_sqlite_connection(sqlite_query)
        result_dict = {}

        if result[0][0] is not None:
            key_list = ['title', 'country', 'release_year', 'genre', 'description']
            count = 0

            for key in key_list: # Это ведь лучше прямого назначения для КАЖДОГО ключа? По типу result_dict['country'] = result[0][1]
                result_dict[key] = result[0][count]
                if count == 4:  # Обрезаем символ \n который закрадывается из базы в ключ description
                    result_dict[key] = result[0][count].strip('\n')
                    break
                count += 1

        else:
            result_dict['is_search'] = False
        return result_dict

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
            return result

        else:
            return {'Оповещение!': 'Категории не существует. Но тут могла быть ваша реклама :)'}

    def get_10fresh_by_genre(self, genre):
        sqlite_query = f"""
                   SELECT title, rating, description, release_year
                   FROM netflix
                   WHERE listed_in LIKE "%{genre}%"
                   ORDER BY release_year DESC
                   LIMIT 10
                   """
        result = self.get_sqlite_connection(sqlite_query)
        return result


# dao = VideosDao()
# search = dao.get_10fresh_by_genre('Adventure')
# print(search)

