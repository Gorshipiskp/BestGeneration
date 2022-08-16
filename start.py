from standart_functions import *
from generation import start_generation
import os


def test_func_events(infos: dict):
    returns = infos['returns']
    per: Person = infos['person']
    returns['history_add'].append(f'{randint(0, 10)} - Насрал')
    return returns


def_needs = config.needs_default
def_reqs = config.default_requiments
def_events = config.default_events
def_skills = config.default_skills
def_habits = config.default_habits
def_abilities = config.default_abilities
person_parameters_indexes = {}


if config.mod_on:
    dlcs = {}
    for i in os.listdir("dlcs"):
        if "__" not in i and ".py" in i:
            try:
                md = __import__("dlcs", fromlist=[i])
                for p in dir(md):
                    if "__" not in p:
                        dlcs.update({i.split(".py")[0]: getattr(md, p)})
            except:
                error_print(1, i)
    for name, module in dlcs.items():
        try:
            for i in dir(module):
                if "____" in i:
                    globals().update({i.replace("____", ""): getattr(module, i)})
        except:
            error_print(6, name)

if config.restart and not config.restart_always or config.restart_always:
    with open("config.py", "r") as i:
        new_lines = i.readlines()
        n, n_id = [o for o in new_lines if "restart = " in o][0].replace("True", "False"), \
                  [o_id for o_id, o in enumerate(new_lines) if "restart = " in o][0]
        new_lines[n_id] = n
    with open("config.py", "w+") as i:
        i.writelines(new_lines)
    try:
        os.remove(f"{config.db_name}")
    except PermissionError:
        error_print(3)
    except FileNotFoundError:
        error_print(5)


def rand_ch(dct: dict, mode: int):
    if mode == 0:
        return ",".join(list(filter(lambda x: x, list(random_chance(name, chance) for name, chance in dct.items()))))
    else:
        return ",".join(list(filter(lambda x: x, list(random_chance(name, chance[0]) for name, chance in dct.items()))))


add_person_parameter("abilities", "TEXT", default=["function", rand_ch, [def_abilities, 0]])
add_person_parameter("habits", "TEXT", default=["function", rand_ch, [def_habits, 1]])

for name, val in def_skills.items():
    add_person_parameter(name, "REAL", default=val)

for par_id, par in enumerate(config.pers_params_nf):
    person_parameters_indexes.update({par: par_id})

all_events = {}

for event_id, vals in def_events.items():
    if not get_no_error(vals, 'disable'):
        try:
            vals['name_event']
        except KeyError:
            error_print(17, event_id)
            continue
        if "TRANSLATE" in vals['name_event']:
            name_event = get_event_tr(event_id)
        else:
            name_event = vals['name_event']
        try:
            func = vals['func_event']
            if type(func) == list:
                func = globals().get(vals['func_event'][0])
        except KeyError:
            error_print(16, name_event)
            continue
        except NameError:
            error_print(18, name_event)
            continue
        if func is None:
            error_print(18, name_event)
            continue
        all_events.update({name_event: Event(def_reqs, person_parameters_nf, vals, event_id, func)})

try:
    sq.connect(config.db_name).cursor().execute(
        f"""CREATE TABLE IF NOT EXISTS {config.table_people_name}(id INTEGER PRIMARY KEY AUTOINCREMENT, {",".join(person_parameters[1:len(person_parameters)])})""")
except Exception:
    error_print(2)

if __name__ == "__main__":
    start_generation(all_events, person_parameters_indexes, def_needs, person_parameters_nf)
