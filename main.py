from flask import Flask, render_template, request, make_response, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import reqparse, abort, Api, Resource
from werkzeug.utils import redirect
from data import db_session
from data.newsform import NewsForm
from data.users import User
from data.jobs import Jobs
from data.jobsform import JobsForm
from data.registrform import RegisterForm
from data.loginform import LoginForm
from data.news import News
from data import jobs_api
from data import news_api
from data.news_resources import NewsResource, NewsListResource
from data.users_resource import UsersResource, UsersListResource
from data.jobs_resource import JobsResource, JobsListResource
import datetime

db_session.global_init("db/blogs.sqlite")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

api = Api(app)
# для списка объектов
api.add_resource(NewsListResource, '/api/v2/news')
api.add_resource(UsersListResource, '/api/v2/users')
api.add_resource(JobsListResource, '/api/v2/jobs')

# для одного объекта
api.add_resource(NewsResource, '/api/v2/news/<int:news_id>')
api.add_resource(UsersResource, '/api/v2/users/<int:user_id>')
api.add_resource(JobsResource, '/api/v2/jobs/<int:job_id>')

login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/")
def index():
    '''session = db_session.create_session()
    news = session.query(News).filter(News.is_private != True)[::-1]
    return render_template("index.html", news=news)'''
    return index_jobs()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route("/jobs")
def index_jobs():
    session = db_session.create_session()
    jobs = session.query(Jobs)
    return render_template("index_jobs.html", jobs=jobs)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/new_jobs', methods=['GET', 'POST'])
@login_required
def add_jobs():
    form = JobsForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        job = Jobs()
        job.job = form.job.data
        job.team_leader = form.team_leader.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.is_finished = form.is_finished.data
        # current_user.jobs.append(job)
        # session.merge(current_user)
        session.add(job)
        session.commit()
        return redirect('/jobs')
    return render_template('jobs.html', title='Добавление работы',
                           form=form)


@app.route('/new_job/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_job(id):
    form = JobsForm()
    if request.method == "GET":
        session = db_session.create_session()
        job = session.query(Jobs).filter(Jobs.id == id,
                                         (Jobs.user == current_user) | (1 == current_user.id)).first()
        if job:
            form.job.data = job.job
            form.team_leader.data = job.team_leader
            form.work_size.data = job.work_size
            form.collaborators.data = job.collaborators
            form.is_finished.data = job.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        job = session.query(Jobs).filter(Jobs.id == id,
                                         Jobs.user == current_user).first()
        if not job:
            job = session.query(Jobs).filter(Jobs.id == id,
                                             1 == current_user.id).first()
        if job:
            job.job = form.job.data
            job.team_leader = form.team_leader.data
            job.work_size = form.work_size.data
            job.collaborators = form.collaborators.data
            job.is_finished = form.is_finished.data
            session.commit()
            return redirect('/jobs')
        else:
            abort(404)
    return render_template('jobs.html', title='Редактирование работы', form=form)


@app.route('/job_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def job_delete(id):
    session = db_session.create_session()
    job = session.query(Jobs).filter(Jobs.id == id,
                                     Jobs.user == current_user).first()
    if not job:
        job = session.query(Jobs).filter(Jobs.id == id,
                                         1 == current_user.id).first()
    if job:
        session.delete(job)
        session.commit()
    else:
        abort(404)
    return redirect('/jobs')


@app.route('/news', methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        news = News()
        news.title = form.title.data
        news.content = form.content.data
        news.is_private = form.is_private.data
        current_user.news.append(news)
        session.merge(current_user)
        session.commit()
        return redirect('/')
    return render_template('news.html', title='Добавление новости',
                           form=form)


@app.route('/news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = NewsForm()
    if request.method == "GET":
        session = db_session.create_session()
        news = session.query(News).filter(News.id == id,
                                          News.user == current_user).first()
        if news:
            form.title.data = news.title
            form.content.data = news.content
            form.is_private.data = news.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        news = session.query(News).filter(News.id == id,
                                          News.user == current_user).first()
        if news:
            news.title = form.title.data
            news.content = form.content.data
            news.is_private = form.is_private.data
            session.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('news.html', title='Редактирование новости', form=form)


@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    session = db_session.create_session()
    news = session.query(News).filter(News.id == id,
                                      News.user == current_user).first()
    if news:
        session.delete(news)
        session.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


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
    app.register_blueprint(news_api.blueprint)
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
    captain.hashed_password = 'pbkdf2:sha256:150000$LkAJpQHX$7aafb27f30c177120cb83bed0160aedf1191ead14acfd0df5ce6f8792f1b474f'

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

    news = News(title="Первая новость", content="Привет блог!",
                user_id=2, is_private=False)
    session.add(news)
    session.commit()
    user = session.query(User).filter(User.id == 1).first()
    news = News(title="Вторая новость", content="Уже вторая запись!",
                user=user, is_private=False)
    session.add(news)
    session.commit()

    app.run()


if __name__ == '__main__':
    a = 80 * '*' + ' '
    print(f'{a}КАПИТАН\n{a}ПОЧТА: scott_chief@mars.org\n{a}ПАРОЛЬ: 123123')
    try:
        main1()
    except:
        main()
