import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    tg_username = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    tg_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    job = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    # questions = orm.relationship("questions", back_populates='user')
