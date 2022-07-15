import os
import config

not_tr = False
lang_tr = config.language.lower()

try:
    open("lang_tr.py", "w+", encoding="UTF-8").write(open(f"languages/{lang_tr}.py", "r", encoding="UTF-8").read())
    import lang_tr
except Exception:
    try:
        open("lang_tr.py", "w+", encoding="UTF-8").write(open(f"languages/english.py", "r", encoding="UTF-8").read())
        import lang_tr
    except Exception:
        not_tr = True


def num_zeros(numnum: int, *number: int | str) -> str:
    strw = ""
    for i in number[::-1]:
        strw += str(i)
    return f"{'0' * (numnum - len(strw))}{strw}"


def transl(translatable: str) -> str | None:
    return lang_tr.translate.get(translatable) if not not_tr else translatable


def error_print(error_id: int) -> print:
    print(
        f"{transl('ERROR')} {num_zeros(3, error_id)} {show_error(error_id) if config.show_errors_description else ''}")


def show_error(err_id: int) -> str | None:
    return f"({lang_tr.translate.get('descriptions').get(str(err_id))})" if not not_tr else ''


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
    except Exception:
        error_print(4)

if not config.debug:
    os.remove("lang_tr.py")
