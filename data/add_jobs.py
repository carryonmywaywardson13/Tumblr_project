# на самом деле News_api

import flask
from flask import jsonify, request

from data import db_session
from data.news import News

blueprint = flask.Blueprint('news_api', __name__,
                            template_folder='templates')


@blueprint.route('/api/news')
def get_news():
    session = db_session.create_session()
    news = session.query(News).all()
    return jsonify(
        {
            'news':
                [item.to_dict(only=('title', 'content', 'user.name'))
                 for item in news]
        }
    )


@blueprint.route('/api/news/<int:news_id>', methods=['GET'])
def get_one_news(news_id):
    session = db_session.create_session()
    news = session.query(News).get(news_id)
    if not news:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'news': news.to_dict(only=('title', 'content',
                                       'user_id', 'is_private'))
        }
    )


@blueprint.route('/api/news', methods=['POST'])
def create_news():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['title', 'content', 'user_id', 'is_private']):  # 'is_published'
        return jsonify({'error': 'Bad request'})
    session = db_session.create_session()
    news = News(
        title=request.json['title'],
        content=request.json['content'],
        user_id=request.json['user_id'],
        is_private=request.json['is_private'],
        # is_published=request.json['is_published']
    )
    session.add(news)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/news/<int:news_id>', methods=['DELETE'])
def delete_news(news_id):
    session = db_session.create_session()
    news = session.query(News).get(news_id)
    if not news:
        return jsonify({'error': 'Not found'})
    session.delete(news)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/news/<int:news_id>', methods=['PUT'])
def change_news(news_id):
    print('Pobeda!')
    session = db_session.create_session()
    news = session.query(News).get(news_id)
    if not news or not request.json():
        return jsonify({'error': 'Not found'})
    for keys in request.json():
        print(keys)
        if keys == 'id':
            news.id = request.json[keys]
        elif keys == 'title':
            news.title = request.json[keys]
        elif keys == 'content':
            news.content = request.json[keys]
        elif keys == 'is_private':
            news.is_private = request.json[keys]
        elif keys == 'user_id':
            news.user_id = request.json[keys]
    session.commit()
    return jsonify({'success': 'OK'})