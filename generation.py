import config
import sqlite3 as sq
from base import transl
from base import show_error
from base import error_print


def exists_db() -> None:
    try:
        sq.connect(f'{config.db_name}.db').cursor().execute(
            f"""
        CREATE TABLE IF NOT EXISTS PEOPLES(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, surname TEXT, 
        {'patronymic TEXT, ' if config.patronymic else ''}{'money INT, ' if config.patronymic else ''}alive BOOL, 
        history TEXT, gender INT, educations TEXT, age INT, parents TEXT)
""")
    except Exception:
        error_print(2)


exists_db()


class Person:

    def __init__(self, id_pers):
        self.id = id_pers

    def get(self, what: str) -> int | str:
        return list(sq.connect(f"{config.db_name}.db").cursor().execute(f"SELECT {what} FROM peoples WHERE id={self.id}"))[0][0]
