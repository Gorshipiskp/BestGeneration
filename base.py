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
p.write("""from generation import Person""")

for i in drs:
    p.write(f'''
    
"""{i.replace(".py", "").capitalize()}"""\n

''')
    txt = "".join(open(f"dlcs/{i}", "r").readlines())
    p.write(f"{txt}")
p.close()

if config.debug:
    import modules_dlcs as mn
else:
    try:
        import modules_dlcs as mn
    except:
        from generation import Person
        print(f"{transl('ERROR')} 001 {show_error(1) if config.show_errors_description else ''}")

if not config.debug:
    os.remove("modules_dlcs.py")

print([i for i in dir(mn.Person) if not "__" in i])
mn.Person.new_event(1, "Sleep")
