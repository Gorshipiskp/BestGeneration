from base import lang_tr
from base import transl
from base import show_error
from base import error_print
import os
import config

os.remove("lang_tr.py")

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
    except:
        from generation import Person

        print(f"{transl('ERROR')} 001 {show_error(1) if config.show_errors_description else ''}")

if not config.debug:
    os.remove("modules_dlcs.py")
