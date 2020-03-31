from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField, StringField, IntegerField
from wtforms.validators import DataRequired


class JobsForm(FlaskForm):
    job = StringField('Название работы', validators=[DataRequired()])
    team_leader = IntegerField("Фамилия и имя ответственного id")
    work_size = IntegerField('Продолжительность в часах')
    collaborators = StringField("Список id команды")
    is_finished = BooleanField("Завершена или нет")
    submit = SubmitField('Добавить')
