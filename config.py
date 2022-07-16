#  Value parameters

language = "English"  # Program's language (Available: Russian and English)
start_count = 50  # How many peoples should spawn at start
age_limit = 10  # How many days must be simulated until simulating have stopped (0 - Never)
db_name = "humans"  # Filename of DB (without extension)

#  Bool parameters

mod_on = True  # Includes mods|DLCs?
immortal = False  # Should people die?
money = True  # Should money system is turn on?
debug = False  # Do debug is turn on?
show_errors_description = True  # Show error's description (like desc what went wrong for more understandable debug)?
history = True  # Is program must write every person's history (Their moves, actions etc.)?
patronymic = True  # Use patronymic? (Like surname, but father's name in surname style)
restart = False  # Should restart simulation and erase it data one time?
restart_always = True  # Should restart simulation and erase its data every run of simulation?

#  Big (Lists, Arrays) parameters

surnames_l = ["Demidov", "Tkachenko", "Pimenov", "Evdokimov", "Knyazev"]
names_l = ["Nikita", "Kirill", "Sergey", "Artyom", "Anton"]
patronymic_l = ["Sergeevich", "Andreevich"]
db_values = {
    "name": ["TEXT", ["random", names_l]],
    "surname": ["TEXT", ["random", surnames_l]],
    "patronymic": ["TEXT", ["random", patronymic_l]] if patronymic else '',
    "money": ["INT", "0"] if money else '',
    "parents": ["TEXT", ""],
    "educations": ["TEXT", ""],
    "age": ["INT", "0"],
    "alive": ["BOOL", "1"],
}  # Standard values, that every person has


#  Setting up config

if len(surnames_l) == 0:
    surnames_l = ["Doe"]
if len(names_l) == 0:
    surnames_l = ["John"]
if len(patronymic_l) == 0:
    surnames_l = ["Doevich"]

pers_params = [f"{i} {db_values[i][0]}" for i in db_values]
pers_params_nf = [f"{i}" for i in db_values]
