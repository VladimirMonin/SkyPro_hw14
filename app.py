from flask import Flask, request, render_template, jsonify
from videos_dao import VideosDao
import logging

logging.basicConfig(encoding='utf-8', level=logging.INFO)

dao = VideosDao()
app = Flask(__name__)


@app.route('/movie/<title>/')
def get_film_by_title(title):
    """ Шаг 1. Поиск по названию самого свежего """
    logging.info(f'Поисковая фраза: {title}')

    single_post_dict = dao.get_last_by_title(title)  # Словарь с данными по ОДНОМУ посту
    logging.info(f'dao.get_last_by_title вернул: {single_post_dict}')

    return jsonify(single_post_dict)


@app.route('/movie/<start_year>/to/<finish_year>/')
def get_film_by_range(start_year, finish_year):
    """ Шаг 2. Поиск фильмов по диапазону лет"""
    logging.info(f'Ищем фильмы в диапазоне от{start_year} и до {finish_year}')
    result = dao.get_film_by_years_range(start_year, finish_year)
    return jsonify(result)
    pass


@app.route('/rating/<category>/')
def get_rating_by_category(category):
    logging.info(f'Ищем фильмы с категорией{category}')
    result = dao.get_rating_by_category(category)
    return jsonify(result)


@app.route('/genre/<genre>/')
def get_data_by_genre(genre):
    logging.info(f'Ищем 10 самых свежих фильмов жанра:{genre}')
    result = dao.get_10fresh_by_genre(genre)
    return jsonify(result)


app.config['JSON_AS_ASCII'] = False

if __name__ == '__main__':
    app.run(debug=True)
