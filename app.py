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
    pass


app.run(debug=True)