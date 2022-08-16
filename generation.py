from standart_functions import *
import time


def simulate_day(all_events: dict, id_pers: int, person_parameters_indexes, current_time: time_gen, pars_nf: list):
    print(f"------------------------")
    pers, reqs = Person(id_pers, pars_nf), {'history_add': [], 'requests': [], 'needs': {}}
    for day in range(1, 24):
        can_event = {}
        for name_event, val_event in all_events.items():
            if val_event.can_do(pers, person_parameters_indexes):
                if get_no_error(val_event.get_other(), 'need'):
                    can_event.update({val_event: float(pers.get(val_event.get_other()['need']) * float(
                        config.needs_default[val_event.get_other()['need']][1]))})
                else:
                    try:
                        can_event.update({val_event: val_event.get_other()['standart_value']})
                    except KeyError:
                        error_print(15, name_event)
        choosen_funcs = sorted(can_event, key=can_event.get)
        if choosen_funcs:
            new_vals = choosen_funcs[0].start_func(person=pers, event=choosen_funcs[0], time=current_time,
                                                   returns={'requests': [], 'history_add': []})
            for name, val in new_vals.items():
                if type(val) is list and val:
                    try:
                        reqs[name] += val
                    except KeyError:
                        error_print(20, name, choosen_funcs[0])
                elif type(val) is dict and val:
                    try:
                        reqs[name] |= val
                    except KeyError:
                        error_print(20, name, choosen_funcs[0])
                elif (type(val) is str) or (type(val) is int) and val:
                    try:
                        reqs[name] = val
                    except KeyError:
                        error_print(20, name, choosen_funcs[0])
                elif not val:
                    ...
                else:
                    error_print(21, type(val), val, choosen_funcs[0])

    if reqs['history_add']:
        pers.add_history(reqs['history_add'], current_time)
    print(f"----------------------------")


def base_generation(all_events: dict, person_parameters_indexes: dict, cur_time: time_gen,
                    def_needs: dict, pars_nf: list):
    #  start = time.time()
    num_peoples = db_gen().get_table_length()
    generate_needs(def_needs)
    for i in range(1, num_peoples + 1):
        simulate_day(all_events, i, person_parameters_indexes, cur_time, pars_nf)
    cur_time.add(24)
    #  print(f"День №{cur_time.get_days()} ({round(time.time() - start, 2)}) ({round((time.time() - start) / config.start_count, 3)})")


def continue_generation(all_events: dict, person_parameters_indexes: dict, def_needs: dict, pars_nf: list):
    cur_time = time_gen()

    if config.age_limit == 0:
        while 1:
            base_generation(all_events, person_parameters_indexes, cur_time, def_needs, pars_nf)
    else:
        for n in range(1, config.age_limit + 1):
            base_generation(all_events, person_parameters_indexes, cur_time, def_needs, pars_nf)


def start_generation(all_events: dict, person_parameters_indexes: dict, def_needs: dict, pars_nf: list):
    if config.statistics:
        start = time.time()

    create_humans()

    if config.statistics:
        try:
            print(get_sentence(2).format(round((time.time() - start) / config.start_count, config.num_round * 2 + 2),
                                         round(time.time() - start, config.num_round)))
        except ZeroDivisionError:
            error_print(10)

    continue_generation(all_events, person_parameters_indexes, def_needs, pars_nf)
