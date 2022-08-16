import sqlite3 as sq
import math
from random import choice, randint
import config
import time

person_parameters = ["id INT"] + config.pers_params
person_parameters_nf = ["id"] + config.pers_params_nf
person_parameters_full = {"id": ['INT', 0]} | config.db_values
default_requiments = config.default_requiments
not_tr = False
backslash = '\n'

try:
    lang_tr = __import__("languages", fromlist=[config.language])
    for i in dir(lang_tr):
        if "__" not in i:
            lang_tr = getattr(lang_tr, i)
except Exception:
    not_tr = True


def num_zeros(numnum: int, *number: int | str) -> str:
    strw = f"{''.join(list(f'{i}' for i in number[::-1]))}"
    return f"{'0' * (numnum - len(strw))}{strw}"


def transl(translatable: str) -> str | None:
    if not not_tr:
        return lang_tr.translate.get(translatable)
    else:
        return translatable


def error_print(error_id: int, *extends) -> print:
    try:
        if config.show_errors_description:
            sw_err = show_error(error_id).format(*extends)
        else:
            sw_err = ''
        print(f"""\033[91m\033[1m{transl('ERROR')} {num_zeros(3, error_id)} {sw_err}\033[0m""")
    except KeyError:
        if error_id != 9:
            error_print(9)
        else:
            print(
                f"\033[91m\033[1m{transl('ERROR')} - ERROR (ERROR'S ID NOT FIND, MAYBE SOMETHING WRONG WITH TRANSLATION FILE)\033[0m")


def uniq_list(lst: list) -> list:
    return list(dict.fromkeys(lst))


def show_error(err_id: int) -> str | None:
    return f"({lang_tr.translate.get('descriptions')[err_id]})" if not not_tr else ''


def get_sentence(sent_id: int) -> str | None:
    return lang_tr.translate.get('sentences')[sent_id]


def get_event_tr(event_id: int) -> str | None:
    return lang_tr.translate.get('events')[event_id]


def get_words_tr(event_id: int) -> str | None:
    return lang_tr.translate.get('words')[event_id]


def random_chance(obj, chance: int | float):
    if chance >= 100:
        return obj
    if chance - int(chance) > 0:
        exp = abs(int(math.log10(chance - int(chance))))
    else:
        exp = 0
    if chance * 10 ** exp > randint(0, 100 * 10 ** exp):
        return obj
    return False


class time_gen:
    def __init__(self):
        self.hours = 0

    def get_hours(self) -> int:
        return round(self.hours)

    def get_days(self) -> float | int:
        return round(self.hours / 24, config.num_round)

    def get_months(self) -> float | int:
        return round(self.hours / 24 / 30, config.num_round)

    def get_years(self) -> float | int:
        return round(self.hours / 24 / 30 / 12, config.num_round)

    def add(self, day: int = 1):
        self.hours += day


def rd_data(lst_parse: list) -> list:
    ready_list = []
    for i in lst_parse:
        if not i == 'id':
            if type(lst_parse[i]) is list:
                if (type(lst_parse[i][1]) is str) and not lst_parse[i][0] == "function":
                    if lst_parse[i][1] == '':
                        ready_list.append("'None'")
                    else:
                        ready_list.append(f"""'{lst_parse[i][1].replace(".", "-")}'""")
                elif (type(lst_parse[i][1]) is int) and not lst_parse[i][0] == "function":
                    ready_list.append(lst_parse[i][1])
                elif type(lst_parse[i][1]) is list:
                    if lst_parse[i][1][0] == "random":
                        try:
                            chss = []
                            need_num = lst_parse[i][2]
                            rem_same = lst_parse[i][3]
                            until_max = lst_parse[i][4]
                            for _ in range(need_num):
                                chss.append(f"'{choice(lst_parse[i][1][1])}'")
                            if rem_same:
                                if until_max:
                                    if need_num > len(lst_parse[i][1][1]):
                                        error_print(13, len(lst_parse[i][1][1]), need_num, lst_parse[i][1][1])
                                        ready_list.append(f"'{choice(lst_parse[i][1][1])}'")
                                    else:
                                        chss += list(f"'{choice(lst_parse[i][1][1])}'" for _ in range(need_num + 4))
                                        chss = uniq_list(chss)
                                        for p in range(abs(need_num - len(chss))):
                                            chss.pop(randint(0, len(chss) - 1))
                            ready_list.append(",".join(chss))
                        except:
                            ready_list.append(f"'{choice(lst_parse[i][1][1])}'")
                    elif lst_parse[i][1][0] == "function" or callable(lst_parse[i][1][1]):
                        try:
                            ready_list.append(f"'{lst_parse[i][1][1](*lst_parse[i][1][2])}'")
                        except Exception:
                            error_print(8, i)
                else:
                    error_print(7, lst_parse[i][1], type(lst_parse[i][1]))
            else:
                ready_list.append(f"'{lst_parse[i]}'")
    return ready_list


def create_humans(numbers_people: int = config.start_count, table: str = config.table_people_name) -> None:
    ready_fulls = list((rd_data(person_parameters_full)) for _ in range(numbers_people))
    with sq.connect(config.db_name) as con:
        curs = con.cursor()
        curs.executemany(
            f"INSERT INTO {table}({', '.join(person_parameters_nf[1:len(person_parameters_nf)])}) VALUES({','.join(list('?' for i in range(len(person_parameters_nf[1:len(person_parameters_nf)]))))})",
            ready_fulls)


def generate_needs(needs: dict = config.needs_default) -> None:
    with sq.connect(config.db_name) as con:
        curs = con.cursor()
        for name, val in needs.items():
            curs.execute(f"UPDATE {config.table_people_name} SET {name} = {name}+{val[0]} WHERE alive=1")


def do_time_stamp(t_gen: time_gen, hours: int = -1):
    if hours == -1:
        stamp = f"{num_zeros(2, int(t_gen.hours % 24))}:00 {num_zeros(2, int(t_gen.get_days() % 31))}.{num_zeros(2, t_gen.get_months() % 12)}.{num_zeros(4, t_gen.get_days() // 365)}"
    else:
        stamp = f"{num_zeros(2, int(hours))}:00 {num_zeros(2, int(t_gen.get_days() % 31))}.{num_zeros(2, int(t_gen.get_months() % 12))}.{num_zeros(4, int(t_gen.get_days() // 365))}"
    return stamp


class db_gen:

    def __init__(self):
        self.val_vals = person_parameters_full

    def get_table_length(self, table_name: str = config.table_people_name) -> int:
        with sq.connect(config.db_name) as con:
            curs = con.cursor()
            all_p = list(curs.execute(f"SELECT COUNT(*) FROM {table_name}"))
            return int(all_p[0][0])

    def get_all_from(self, table: str = config.table_people_name) -> list:
        with sq.connect(config.db_name) as con:
            curs = con.cursor()
            all_p = list(curs.execute(f"SELECT * FROM {table}"))
            return all_p

    def edit(self, id_per: int, what_edit: str, val_edit: str | int, table: str = config.table_people_name,
             is_set: bool = True) -> None:
        pers = Person(id_per, person_parameters_nf)
        if is_set:
            with sq.connect(config.db_name) as con:
                curs = con.cursor()
                if "TEXT" in self.val_vals[what_edit][0]:
                    val_edit = f"'{val_edit}'"
                elif "INT" in self.val_vals[what_edit] or "REAL" in self.val_vals[what_edit]:
                    val_edit = val_edit
                else:
                    error_print(19, self.val_vals[what_edit])
                curs.execute(f"UPDATE {table} SET {what_edit}={val_edit} WHERE ID={id_per}")
        else:
            with sq.connect(config.db_name) as con:
                if "TEXT" in self.val_vals[what_edit][0]:
                    if pers.get(what_edit).replace("'", "").replace('"', '') != 'None':
                        val_edit = f"""'{pers.get(what_edit).replace("'", "").replace('"', '')},{val_edit}'"""
                    else:
                        val_edit = f"'{val_edit}'"
                    curs = con.cursor()
                    curs.execute(f"UPDATE {table} SET {what_edit}={val_edit} WHERE ID={id_per}")
                elif "INT" in self.val_vals[what_edit] or "REAL" in self.val_vals[what_edit]:
                    curs = con.cursor()
                    curs.execute(f"UPDATE {table} SET {what_edit}={what_edit}+{val_edit} WHERE ID={id_per}")
                else:
                    error_print(19, self.val_vals[what_edit])


class Person:

    def __init__(self, id_pers: int, def_per_pars: list, table: str = config.table_people_name):
        self.id = id_pers
        self.infos = {}
        for i_id, i in enumerate(list(sq.connect(config.db_name).cursor().execute(
                f"SELECT * FROM {table} WHERE id={self.id}"))[0]):
            self.infos |= {def_per_pars[i_id]: i}

    def get(self, what: str):
        if what == "*":
            return list(self.infos.values())
        else:
            return self.infos[what]

    def edit_needs(self, need_name: str, num_edit: int, is_set: bool = False) -> None:
        db_gen().edit(self.id, need_name, num_edit, is_set=is_set)

    def add_history(self, text_to_add: list, time_stamp: time_gen, table: str = config.table_people_name):

        last = f"""{self.get('history').replace("'None'", "")},,,"""
        if last == ',,,':
            last = ''
        text_to_add = last + ',,,'.join(
            list(f'{do_time_stamp(time_stamp, t_i)} - {text_to_add[t_i]}' for t_i in range(len(text_to_add))))

        start = time.time()
        sq.connect(config.db_name).cursor().execute(f"UPDATE {table} SET history='{text_to_add}' WHERE ID={self.id}").close()
        print(f"{time.time() - start}")


def add_needs(needs: dict) -> dict | None:
    if not needs or type(needs) == bool:
        return None
    itg = {}
    try:
        for need, vals in needs.items():
            vals_range = []
            if "min" in vals and "max" in vals:
                vals_range = [needs[need]['min'], needs[need]['max']]
            elif "max" in vals:
                vals_range = [0, needs[need]['max']]
            elif "min" in vals:
                vals_range = [needs[need]['min'], 100]
            if vals_range:
                itg.update({need: vals_range})
        return itg
    except AttributeError:
        error_print(12, "add_needs", needs)
    except:
        error_print(11, f"add_needs({needs})")


def age_do(age: dict) -> list | None:
    if not age or type(age) == bool:
        return None
    vals_range = []
    for need, vals in age.items():
        if "min" in need and "max" in need:
            vals_range = [age['min'], age['max']]
        elif "max" in need:
            vals_range = [0, age['max']]
        elif "min" in need:
            vals_range = [age[need], 100]
    if vals_range:
        return vals_range
    return vals_range


def get_no_error(dictin: dict, what) -> dict | None:
    try:
        return dictin[what]
    except KeyError:
        return
    except:
        error_print(11, f'get_no_error({dictin}, {what})')


types_reqs = {
    1: add_needs,
    2: age_do
}


class Event:
    def __init__(self, def_reqs: dict, per_params, vals, event_id, func_todo):
        self.requiments = {}
        self.other = {}
        self.func = func_todo
        blacklist = ["after", 'need', 'history_add', 'standart_value', 'name_event']

        for name, type_f in def_reqs.items():
            if name in blacklist:
                if name == 'name_event':
                    if "TRANSLATE" in vals['name_event']:
                        self.other.update({name: get_event_tr(event_id)})
                    else:
                        self.other.update({name: vals['name_event']})
                elif type_f == 0:
                    self.other.update({name: get_no_error(vals, name)})
                else:
                    self.other.update({name: types_reqs[type_f](get_no_error(vals, name))})
            elif name in per_params:
                if type_f == 0:
                    self.requiments.update({name: get_no_error(vals, name)})
                else:
                    self.requiments.update({name: types_reqs[type_f](get_no_error(vals, name))})
            else:
                if type(get_no_error(vals, name)) is dict:
                    if type_f == 0:
                        self.requiments.update({name: get_no_error(vals, name)})
                    else:
                        self.requiments.update({name: types_reqs[type_f](get_no_error(vals, name))})
                elif get_no_error(vals, name) is None:
                    pass
                else:
                    error_print(14, name)

        for name, val in self.requiments.copy().items():
            if val is None:
                self.requiments.pop(name)

        for name, val in self.requiments.copy().items():
            if name not in per_params and name != 'needs':
                self.requiments.pop(name)
            elif type(get_no_error(vals, name)) is dict:
                for name_n, val_n in val.copy().items():
                    if name_n not in per_params:
                        self.requiments[name].pop(name_n)

    def get_requiments(self) -> dict:
        return self.requiments

    def get_other(self) -> dict:
        return self.other

    def start_func(self, **infs) -> dict:
        return self.func(infs)

    def can_do(self, pers_c: Person, person_parameters_indexes) -> bool | None:
        pers = pers_c.get("*")
        values_i = {}
        for name, id_name in person_parameters_indexes.items():
            values_i.update({'id': pers_c.id})
            try:
                values_i.update({name: pers[id_name + 1].replace("'", "").replace('"', "")})
            except AttributeError:
                values_i.update({name: pers[id_name + 1]})
            except:
                error_print(12, f"Event({self}).can_do({pers}, {person_parameters_indexes})", pers[id_name])

        for req_name, req_val in self.requiments.items():
            if req_val != {} and type(req_val) is dict:
                for need_name, need_val in req_val.items():
                    if not need_val[0] <= values_i[need_name] <= need_val[1]:
                        return False
            else:
                if req_val != values_i[req_name]:
                    return False
        return True


def add_person_parameter(name: str = "test", value_type: str = "TEXT", default=None, num: int = 1,
                         remove_same: bool = False, until_num: bool = False) -> None:
    person_parameters.append(f"{name} {value_type}")
    person_parameters_nf.append(name)
    person_parameters_full[name] = [value_type, default, num, remove_same, until_num]


def add_requiment(name: str, type_f: int) -> None:
    default_requiments.update({name: type_f})


def add_types_reqs(def_t: type(abs)) -> None:
    types_reqs.update({len(types_reqs) + 1: def_t})
