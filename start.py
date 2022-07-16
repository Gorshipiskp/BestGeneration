from standart_functions import error_print
import os
import config


drs = os.listdir("dlcs")

if config.mod_on:
    open("modules_dlcs.py", "w+")
    p = open("modules_dlcs.py", "a")
    p.write("""from standart_functions import Person
from standart_functions import add_person_parameter
    
person_parameters = []""")

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
            from standart_functions import Person
            error_print(1)

    try:
        from modules_dlcs import person_parameters
    except Exception:
        error_print(6)

    if not config.debug:
        os.remove("modules_dlcs.py")

from generation import start_generation

start_generation()
start_generation()
start_generation()
