import json
from typing import List

from peewee import Model, SqliteDatabase, IntegerField, DateTimeField, TextField
from config_data.config import DB_PATH, DATE_FORMAT
from datetime import datetime

db = SqliteDatabase(DB_PATH)




class BaseModel(Model):
    class Meta:
        database=db


class SaveHistory(BaseModel):
    user_id = IntegerField()
    date = DateTimeField(default=datetime.now())
    film = TextField()


def save_db(user_id: int, film: dict) -> None:
    '''Сохраняем данные в бд'''
    data = json.dumps(film)
    with db.connection_context():
        SaveHistory.create(user_id=user_id,
                           film=data)


def get_history(user_id: int, offset: int=None) -> List[dict]:

    with db.connection_context():
        if offset is None:
            result = SaveHistory.select(SaveHistory.film).where(user_id=user_id).limit(10).order_by(SaveHistory.date)
        else:
            result = SaveHistory.select().where(user_id=user_id).offset(offset).limit(10)
    films = []
    for item in result:
        films.append(json.loads(item))

    return films