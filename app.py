from flask import Flask, request, render_template, jsonify
from videos_dao import VideosDao
import logging

logging.basicConfig(encoding='utf-8', level=logging.INFO)

dao = VideosDao()
app = Flask(__name__)

@app.route('/movie/<title>/')
def get_post_by_id(title):
    """ Шаг 1. Поиск по названию самого свежего """
    logging.info(f'Поисковая фраза до обработки: {title}')

    # title = title.replace('%', ' ')
    # logging.info(f'Поисковая фраза после replace: {title}')

    single_post_dict = dao.get_last_by_title(title)  # Словарь с данными по ОДНОМУ посту
    logging.info(f'dao.get_last_by_title вернул: {single_post_dict}')

    return jsonify(single_post_dict)


app.run(debug=True)