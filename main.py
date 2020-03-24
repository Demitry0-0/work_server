from flask import Flask, render_template
from werkzeug.utils import redirect
from data import db_session
from data.users import User
from data.jobs import Jobs
from data.registrform import RegisterForm
from data.news import News
from data.resource import NewsResource, NewsListResource
from data import jobs_api
from flask_restful import Api
import datetime

db_session.global_init("db/blogs.sqlite")

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route("/")
def index():
    session = db_session.create_session()
    jobs = session.query(Jobs)
    return render_template("index.html", jobs=jobs)


@app.route('/login')
def login():
    return 'робит четко!'


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(surname=form.surname.data,
                    name=form.name.data,
                    age=form.age.data,
                    position=form.position.data,
                    speciality=form.speciality.data,
                    address=form.address.data,
                    email=form.email.data
                    )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


def main():
    db_session.global_init("db/blogs.sqlite")
    app.register_blueprint(jobs_api.blueprint)
    app.run()


def main1():
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

    job = Jobs()
    job.team_leader = 1
    job.job = 'deployment of residential modules 1 and 2'
    job.work_size = 15
    job.collaborators = '2, 3'
    job.start_date = datetime.datetime.now()
    job.is_finished = False
    session.add(job)

    job = Jobs()
    job.team_leader = 2
    job.job = 'deployment of residential modules 1 and 2'
    job.work_size = 15
    job.collaborators = '2, 3'
    job.start_date = datetime.datetime.now()
    job.is_finished = False
    session.add(job)

    job = Jobs()
    job.team_leader = 3
    job.job = 'deployment of residential modules 1 and 2'
    job.work_size = 15
    job.collaborators = '2, 3'
    job.start_date = datetime.datetime.now()
    job.is_finished = False
    session.add(job)

    session.add(captain)
    session.add(colonist)
    session.add(cook)
    session.add(pirat)
    session.commit()

    app.run()


if __name__ == '__main__':
    try:
        main1()
    except:
        main()
