import sqlalchemy
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True,
                           autoincrement=True)
    user_name = sqlalchemy.Column(sqlalchemy.String,
                                  nullable=False)
    user_telegram_id = sqlalchemy.Column(sqlalchemy.String,
                                         nullable=False)
    bin = sqlalchemy.Column(sqlalchemy.String,
                            nullable=False)
    price = sqlalchemy.Column(sqlalchemy.Integer,
                              nullable=False)

    def __repr__(self):
        return f'{self.user_name}:{self.user_telegram_id}:{self.bin}'
