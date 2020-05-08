import sqlalchemy
from data.db_session import SqlAlchemyBase

association_table = sqlalchemy.Table('jobs_to_category', SqlAlchemyBase.metadata,
                                     sqlalchemy.Column('jobs', sqlalchemy.Integer,
                                                       sqlalchemy.ForeignKey('jobs.id')),
                                     sqlalchemy.Column('jobscategory', sqlalchemy.Integer,
                                                       sqlalchemy.ForeignKey('jobscategory.id'))
                                     )


class JobsCategory(SqlAlchemyBase):
    __tablename__ = 'jobscategory'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
