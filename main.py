from flask import Flask, jsonify
from data import db_session
from data.users import User
from data.news import News
from data import jobs_api
from flask_restful import reqparse, abort, Api, Resource


class NewsResource(Resource):
    def get(self, news_id):
        abort_if_news_not_found(news_id)
        session = db_session.create_session()
        news = session.query(News).get(news_id)
        return jsonify({'news': news.to_dict(
            only=('title', 'content', 'user_id', 'is_private'))})

    def delete(self, news_id):
        abort_if_news_not_found(news_id)
        session = db_session.create_session()
        news = session.query(News).get(news_id)
        session.delete(news)
        session.commit()
        return jsonify({'success': 'OK'})


class NewsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        news = session.query(News).all()
        return jsonify({'news': [item.to_dict(
            only=('title', 'content', 'user.name')) for item in news]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        news = News(
            title=args['title'],
            content=args['content'],
            user_id=args['user_id'],
            is_published=args['is_published'],
            is_private=args['is_private']
        )
        session.add(news)
        session.commit()
        return jsonify({'success': 'OK'})


def abort_if_news_not_found(news_id):
    session = db_session.create_session()
    news = session.query(News).get(news_id)
    if not news:
        abort(404, message=f"News {news_id} not found")


def main():
    db_session.global_init("db/blogs.sqlite")
    app.register_blueprint(jobs_api.blueprint)
    app.run()


db_session.global_init("db/blogs.sqlite")

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
def hack():
    return '<center><h1>Ну че вроде робит</h1></center>'


parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('content', required=True)
parser.add_argument('is_private', required=True)
parser.add_argument('is_published', required=True)
parser.add_argument('user_id', required=True, type=int)


def main1():
    # app.run()
    session = db_session.create_session()
    captain = User()
    captain.surname = 'Scott'
    captain.name = 'Ridley'
    captain.age = 21
    captain.position = 'captain'
    captain.speciality = 'research engineer'
    captain.address = 'module_1'
    captain.email = 'scott_chief@mars.org'

    colonist = User()
    colonist.surname = 'Htata'
    colonist.name = 'Chupakabra'
    colonist.age = 228
    colonist.position = 'door'
    colonist.speciality = 'open door'
    colonist.address = 'door'
    colonist.email = 'open_door_pllz@makaka.door'

    cook = User()
    cook.surname = 'Ramzi'
    cook.name = 'Gordon'
    cook.age = 2
    cook.position = 'room cook'
    cook.speciality = 'covid cook'
    cook.address = 'cook home'
    cook.email = 'povar_virusa@gotov.edy'

    pirat = User()
    pirat.surname = 'Vorobushek'
    pirat.name = 'Jack'
    pirat.age = 19
    pirat.position = 'pirat'
    pirat.speciality = 'thief'
    pirat.address = 'None'
    pirat.email = 'shlupka_and_korable@ykral.money'

    session.add(captain)
    session.add(colonist)
    session.add(cook)
    session.add(pirat)
    session.commit()


if __name__ == '__main__':
    main1()
