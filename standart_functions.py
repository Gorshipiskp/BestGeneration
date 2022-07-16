import config
import os
import sqlite3 as sq
from random import randint


person_parameters = config.pers_params
person_parameters_nf = config.pers_params_nf
person_parameters_full = config.db_values
dbnm = config.db_name
not_tr = False
backslash = '\n'

try:
    open("lang_tr.py", "w+", encoding="UTF-8").write(open(f"languages/{config.language}.py", "r", encoding="UTF-8").read())
    import lang_tr
except Exception:
    try:
        open("lang_tr.py", "w+", encoding="UTF-8").write(open(f"languages/english.py", "r", encoding="UTF-8").read())
        import lang_tr
    except Exception:
        not_tr = True


if not config.debug:
    os.remove("lang_tr.py")


def num_zeros(numnum: int, *number: int | str) -> str:
    strw = ""
    for i in number[::-1]:
        strw += str(i)
    return f"{'0' * (numnum - len(strw))}{strw}"


def transl(translatable: str) -> str | None:
    return lang_tr.translate.get(translatable) if not not_tr else translatable


def error_print(error_id: int, *extends) -> print:
    print(
        f"""{transl('ERROR')} {num_zeros(3, error_id)} {show_error(error_id) if config.show_errors_description else ''} 
{f'{"-" if extends else ""} {", ".join(extends).capitalize()}'}{backslash if extends else ''}""")


def show_error(err_id: int) -> str | None:
    return f"({lang_tr.translate.get('descriptions').get(str(err_id))})" if not not_tr else ''


class time_gen:
    def __init__(self):
        self.day = 0

    def get(self) -> int:
        return self.day

    def add(self):
        self.day += 1


class db_gen:

    def __init__(self, db_name: str = dbnm):
        self.db = f"{db_name}"

    def insert(self, *values, table: str = "peoples"):
        #with sq.connect(f"{self.db}.db") as con:
        con = sq.connect(f"{self.db}.db")
        curs = con.cursor()

        def rd_data(lst_parse):
            ready_list = []
            for i in lst_parse:
                if type(lst_parse[i]) is list:
                    if (type(lst_parse[i][1]) is int or type(lst_parse[i][1]) is str) and not lst_parse[i][0] == "function":
                        ready_list.append("'None'" if lst_parse[i][1] == '' else f"""'{lst_parse[i][1].replace(".", "-")}'""")
                    elif type(lst_parse[i][1]) is list:
                        if lst_parse[i][1][0] == "random":
                            ready_list.append(f"'{lst_parse[i][1][1][randint(0, len(lst_parse[i][1][1]) - 1)]}'")
                        elif lst_parse[i][1][0] == "function" or callable(lst_parse[i][1][1]):
                            try:
                                ready_list.append(f"'{lst_parse[i][1][1](*lst_parse[i][1][2])}'")
                            except Exception:
                                error_print(8, i)
                    else:
                        error_print(7, i)
                else:
                    ready_list.append(f"'{lst_parse[i]}'")
            return ready_list
        curs.execute(f"INSERT INTO peoples({', '.join(person_parameters_nf)}) VALUES({', '.join(rd_data(person_parameters_full))})")

    def insert2(self, *values, table: str = "peoples"):
        with sq.connect(f"{self.db}.db") as con:
            con = sq.connect(f"{self.db}.db")
            curs = con.cursor()

            def rd_data(lst_parse):
                ready_list = []
                for i in lst_parse:
                    if type(lst_parse[i]) is list:
                        if (type(lst_parse[i][1]) is int or type(lst_parse[i][1]) is str) and not lst_parse[i][0] == "function":
                            ready_list.append("'None'" if lst_parse[i][1] == '' else f"""'{lst_parse[i][1].replace(".", "-")}'""")
                        elif type(lst_parse[i][1]) is list:
                            if lst_parse[i][1][0] == "random":
                                ready_list.append(f"'{lst_parse[i][1][1][randint(0, len(lst_parse[i][1][1]) - 1)]}'")
                            elif lst_parse[i][1][0] == "function" or callable(lst_parse[i][1][1]):
                                try:
                                    ready_list.append(f"'{lst_parse[i][1][1](*lst_parse[i][1][2])}'")
                                except Exception:
                                    error_print(8, i)
                        else:
                            error_print(7, i)
                    else:
                        ready_list.append(f"'{lst_parse[i]}'")
                return ready_list
            curs.execute(f"INSERT INTO peoples({', '.join(person_parameters_nf)}) VALUES({', '.join(rd_data(person_parameters_full))})")


class Person:

    def __init__(self, id_pers: int):
        self.id = id_pers

    def get(self, what: str) -> int | str:
        return list(sq.connect(f"{dbnm}.db").cursor().execute(f"SELECT {what} FROM peoples WHERE id={self.id}"))[0][0]

    def born(self, parents: list[int] | int | str = "") -> None:
        db_gen(dbnm).insert()

    def born2(self, parents: list[int] | int | str = "") -> None:
        db_gen(dbnm).insert()


def add_person_parameter(name: str = "test", value_type: str = "TEXT", default: str = ''):
    person_parameters.append(f"{name} {value_type}")
    person_parameters_nf.append(name)
    person_parameters_full[name] = [value_type, default]
