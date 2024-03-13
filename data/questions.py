import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Question(SqlAlchemyBase):
    __tablename__ = 'questions'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    # content = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    isCompleted = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    completed_date = sqlalchemy.Column(sqlalchemy.DateTime)
    job = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    importance_level = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    task_performance_evaluation = sqlalchemy.Column(sqlalchemy.Integer)
    image = sqlalchemy.Column(sqlalchemy.BLOB)
    # user = orm.relationship('User')
