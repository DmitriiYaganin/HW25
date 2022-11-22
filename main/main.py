# -*- coding: utf-8 -*-
import json
import logging

from flask import Blueprint, render_template, request, jsonify

from utils import get_posts_all, get_comments_by_post_id, get_post_by_pk, search_for_posts, get_posts_by_user, for_views

logging.basicConfig(filename='logs/api.log', level=logging.INFO)
logger = logging.getLogger(__name__)

# делаем экземпляр класса блюпринт
main_blueprint = Blueprint('main_blueprint', __name__, template_folder='templates')


@main_blueprint.route('/')
def main_page():
    """
    вьюшка блюпринт на главную страницу
    :return:
    """
    posters = get_posts_all()

    return render_template('index.html', posters=posters)


@main_blueprint.route('/posts/<int:postid>')
def post_page(postid):
    post_pk = get_post_by_pk(postid)
    post_comms = get_comments_by_post_id(postid)
    com_len = len(post_comms)
    return render_template('post.html', post_pk=post_pk, post_comms=post_comms, com_len=com_len)


@main_blueprint.route('/results/', methods=['POST', 'GET'])
def page_search_results():
    answer = request.values.get('query')
    post_results = search_for_posts(answer)
    len_post_results = len(post_results)
    return render_template('search-results.html', post_results=post_results, len_post_results=len_post_results)
    # return redirect(url_for('main_blueprint.search_posts'))


@main_blueprint.route('/users/<username>')
def users_page(username):
    post_for_usernames = get_posts_by_user(username)
    return render_template('user-feed.html', post_for_usernames=post_for_usernames)


@main_blueprint.route('/api/posts')
def api_posts_page():
    logging.info("запрос на все посты")
    with open('data/data.json', "r", encoding="utf-8") as f:
        post_data = json.load(f)
    return jsonify(post_data)


@main_blueprint.route('/api/posts/<int:post_id>')
def api_get_posts_by_user(post_id):
    logging.info("запрос на один пост")
    with open('data/data.json', 'r', encoding="utf-8") as f:
        post_data = json.load(f)
    post_for_pk = []
    for post in post_data:
        if post_id == post['pk']:
            post_for_pk.append(post)
    return jsonify(post_for_pk)
