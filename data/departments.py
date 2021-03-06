import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Departaments(SqlAlchemyBase):
    __tablename__ = 'departaments'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    chief = sqlalchemy.Column(sqlalchemy.Integer,
                              sqlalchemy.ForeignKey("users.id"),
                              nullable=True)
    members = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user = orm.relation('User', back_populates='departaments')
