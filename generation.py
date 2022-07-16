import config
import os
import time
import sqlite3 as sq
from standart_functions import error_print, person_parameters, Person

dbnm = config.db_name


if config.restart and not config.restart_always or config.restart_always:
    with open("config.py", "r") as i:
        new_lines = i.readlines()
        n, n_id = [o for o in new_lines if "restart = " in o][0].replace("True", "False"), \
                  [o_id for o_id, o in enumerate(new_lines) if "restart = " in o][0]
        new_lines[n_id] = n
    with open("config.py", "w+") as i:
        i.writelines(new_lines)
    try:
        os.remove(f"{config.db_name}.db")
    except PermissionError:
        error_print(3)
    except FileNotFoundError:
        error_print(5)
    except Exception:
        error_print(4)


def exists_db() -> None:
    try:
        sq.connect(f'{dbnm}.db').cursor().execute(
            f"""
        CREATE TABLE IF NOT EXISTS PEOPLES(id INTEGER PRIMARY KEY AUTOINCREMENT, {", ".join(person_parameters)})
""")
    except Exception:
        error_print(2)


exists_db()


def first_spawn():
    for p in range(config.start_count):
        Person(p).born()


def start_generation():
    first_spawn()
