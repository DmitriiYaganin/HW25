import json

from flask import jsonify


def _open_comments():
    """
    открывает файл с комментами
    :return: список со словарями из файла comments.json
    """
    with open('data/comments.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def _count_posts():
    """
    ищем самый большой post_id
    :return: самый большой post_id, тип int
    """
    for i in range(len(_open_comments())):
        if _open_comments()[i]["post_id"] > _open_comments()[i - 1]["post_id"]:
            res = _open_comments()[i]["post_id"]
        else:
            res = _open_comments()[i + 1]["post_id"]
    return res


def get_posts_all():
    """
    возвращает посты из файла data.json
    :return: список с постами
    """
    with open("data/data.json", 'r', encoding='utf-8') as f:
        return json.load(f)


def _index_user():
    """
    составляем список с комментаторами
    :return: множество с комментаторами
    """
    commenter = set()
    for i in range(len(get_posts_all())):
        commenter.add(get_posts_all()[i]["poster_name"])
    return commenter


def get_posts_by_user(user_name):
    """
    Возвращает все посты определенного пользователя из файла data.json
    если пользователя нет, то ValueError
    если постов нет, то пустой список
    :param user_name: строка с никнэймом пользователя
    :return: список с постами пользователя
    """
    users_post = []
    if user_name in _index_user():
        for i in range(len(get_posts_all())):
            if get_posts_all()[i]["poster_name"] == user_name:
                users_post.append(get_posts_all()[i])
        return users_post
    raise ValueError('User not found')


def get_comments_by_post_id(post_id):
    """
    Возвращает комментарии определенного поста из файла comments.json
    если поста нет, то ValueError
    если комментов нет, то пустой список
    :param post_id: номер поста в инт
    :return:возвращает список с комментариями
    """
    file_with_comments = _open_comments()
    comments = []
    for i in range(len(file_with_comments)):
        if file_with_comments[i]['post_id'] == post_id:
            comments.append(file_with_comments[i])
    return comments


def search_for_posts(query):
    """
    Возвращает список постов по ключевому слову
    :param query: слово, тип строка
    :return: список постов
    """
    posts = []
    query = (str(query)).lower()
    for i in range(len(get_posts_all())):
        get_posts_all()[i]["content"] = (str((get_posts_all()[i]["content"]))).lower()
        if query in get_posts_all()[i]["content"]:
            posts.append(get_posts_all()[i])
    return posts


def get_post_by_pk(pk):
    """
    возвращает пост по его pk
    :param pk: число, тип int
    :return: словарь с постом
    """
    posts_by_pk = get_posts_all()
    for i in range(len(posts_by_pk)):
        if posts_by_pk[i]['pk'] == pk:
            return posts_by_pk[i]


def for_views():

    return 25


def api_posts_page():
    with open('data/data.json', "r", encoding="utf-8") as f:
        post_data = json.load(f)
    return jsonify(post_data)
