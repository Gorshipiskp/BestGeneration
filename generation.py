import config
import sqlite3
from base import transl
from base import show_error
from base import error_print


hm_bd = "humans.db"


def exists_db():
    try:
        sqlite3.connect('humans.db').cursor().execute("CREATE TABLE IF NOT EXISTS PEOPLES(id INTEGER PRIMARY KEY "
                                                      "AUTOINCREMENT, name TEXT, surname TEXT, "
                                                      "patronymic TEXT, alive BOOL, history TEXT, gender INT, "
                                                      "educations TEXT, age INT, parents TEXT)")
    except:
        error_print(f"{transl('ERROR')} 002 {show_error(2) if config.show_errors_description else ''}")


exists_db()


class Person:

    def __init__(self, id_pers):
        self.id = id_pers

    def get(self, what):
        return list(sqlite3.connect(hm_bd).cursor().execute(f"SELECT {what} FROM peoples WHERE id={self.id}"))[0][0]
