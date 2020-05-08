from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField


class DepartamentForm(FlaskForm):
    title = StringField('Название департамента', validators=[DataRequired()])
    chief = IntegerField("id ответственного ", validators=[DataRequired()])
    members = StringField("Список id команды", validators=[DataRequired()])
    email = EmailField("Почта", validators=[DataRequired()])
    submit = SubmitField('Добавить')
