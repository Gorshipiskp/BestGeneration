import os
import config

lang_tr = config.language.lower()


def transl(translatable: str) -> str | None:
    return lang_tr.translate.get(translatable) if not not_tr else translatable


def show_error(err_id: int) -> str | None:
    return f"({lang_tr.translate.get('descriptions').get(str(err_id))})" if not not_tr else ''


not_tr = False

try:
    open("lang_tr.py", "w+", encoding="UTF-8").write(open(f"languages/{lang_tr}.py", "r", encoding="UTF-8").read())
    import lang_tr
except Exception:
    try:
        open("lang_tr.py", "w+", encoding="UTF-8").write(open(f"languages/english.py", "r", encoding="UTF-8").read())
        import lang_tr
    except Exception:
        not_tr = True


os.remove("lang_tr.py")

drs = os.listdir("dlcs")

open("modules_dlcs.py", "w+")
p = open("modules_dlcs.py", "a")

for i in drs:
    p.write(f'''\n\n"""{i.replace(".py", "").capitalize()}"""\n\n''')
    txt = "".join(open(f"dlcs/{i}", "r").readlines())
    p.write(f"{txt}\n")
p.close()

try:
    import modules_dlcs as mn
except:
    print(f"{transl('ERROR')} 001 {show_error(1) if config.show_errors_description else ''}")

os.remove("modules_dlcs.py")
