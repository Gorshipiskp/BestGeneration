from base import lang_tr, transl, show_error, error_print
import os
import config

drs = os.listdir("dlcs")

open("modules_dlcs.py", "w+")
p = open("modules_dlcs.py", "a")
p.write("""from generation import Person""")

for i in drs:
    p.write(f'''

"""{i.replace(".py", "").replace("_", " ").capitalize()}"""\n

''')
    txt = "".join(open(f"dlcs/{i}", "r").readlines())
    p.write(f"{txt}")
p.close()

if config.debug:
    import modules_dlcs as mn
else:
    try:
        import modules_dlcs as mn
    except Exception:
        from generation import Person

        error_print(1)

if not config.debug:
    os.remove("modules_dlcs.py")
