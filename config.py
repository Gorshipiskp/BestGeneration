#  Value parameters

language = "English"  # Program's language (Available: Russian and English)
start_count = 25  # How many peoples should spawn at start
num_round = 2  # Rounding accuracy (How many numbers should be after dot in numbers)
age_limit = 365  # How many days must be simulated until simulating have stopped (0 - Never)
db_name_raw = "humans"  # Filename of DB (without extension)
table_people_name = "PEOPLES"  # Name of table in DB where stores people's information

#  Bool parameters

mod_on = True  # Includes mods|DLCs?
immortal = False  # Should people die?
money = False  # Should money system is turn on?
debug = False  # Do debugging turn on?
show_errors_description = True  # Show error's description (like desc what went wrong for more understandable debug)?
history = True  # Is program must write every person's history (Their moves, actions etc.)?
patronymic = True  # Use patronymic? (Like surname, but father's name in surname style)
restart = False  # Should restart simulation and erase it data one time?
restart_always = True  # Should restart simulation and erase its data every run of simulation?
statistics = False  # Is need to show various statistics?

#  Big (Lists, Arrays) parameters

names_l = ["Nikita", "Kirill", "Sergey", "Artyom", "Anton"]  # Names
surnames_l = ["Demidov", "Tkachenko", "Pimenov", "Evdokimov", "Knyazev"]  # Surnames
patronymic_l = ["Sergeevich", "Andreevich"]  # Patronymics

surnames_l = list(dict.fromkeys(surnames_l))
names_l = list(dict.fromkeys(names_l))
patronymic_l = list(dict.fromkeys(patronymic_l))

db_values = {
    "name": ["TEXT", ["random", names_l]],
    "surname": ["TEXT", ["random", surnames_l]],
    "parents": ["TEXT", ""],
    "educations": ["TEXT", ""],
    "age": ["INT", 0],
    "alive": ["BOOL", 1],
    "food": ["REAL", 100],
    "sleep": ["REAL", 100],
    "leisure": ["REAL", 100],
    "hygiene": ["REAL", 100],
    "thirst": ["REAL", 100],
    "health": ["REAL", 100],
}  # Standard values, that every person has

needs_default = {
    "food": [-0.45, 0.95],
    "thirst": [-0.45, 0.75],
    "sleep": [-0.25, 0.9],
    "leisure": [-0.2, 0.9],
    "hygiene": [-0.2, 1.05],
    "health": [-0.05, 0.85],
}  # Standard needs, that every person has

default_requiments = {
    'needs': 1,
    'educations': 0,
    'after': 0,
    'age': 2,
    'name': 0,
    'thirst': 0,
    'habits': 0,
    'abilities': 0,
    'skills': 1,
    'need': 0,
    'surname': 0,
    'standart_value': 0,
    'history_add': 0,
    'name_event': 0,
}  # Mode (ID) of the function processing the value (for developers)

default_abilities = {
    "Studying": 25,
    "Cooking": 20,
    "Fitness": 15,
    "Beautiful": 5.5,
}  # Standard abilities of people and the chance of getting them by a person (in %)

default_habits = {
    "Smoking": [25, {'needs': {'health': -0.3}}],
    "Cooking": [25, {'skills': {'Cooking': 0.02}}],
    "Sport": [25, {'skills': {'Sportiness': 0.05}}],
}  # Standard habits of people and the chance of getting them by a person with their influence (in %, values affected by the habit)

default_skills = {
    "Learning": 20,
    "Art": 10,
    "Walking": 25,
    "Cooking": 5,
    "Sportiness": 10,
}  # Standard skills in humans and the chance of their initial value at birth

default_events = {
    1: {
        "name_event": "TRANSLATE",
        "need": 'thirst',
        "needs": {
            "thirst": {"max": 70},
        },
        "skills": {
            "Learning": {"max": 45, 'min': 10},
        },
    },
    2: {
        "name_event": "Eat",
        "need": 'food',
        "needs": {
            "thirst": {"max": 90},
            "food": {"max": 95, 'min': 10},
        },
        "skills": {
            "Learning": {"max": 45, 'min': 5},
        },
    },
    3: {
        "name_event": "Test",
        'surname': 'Pimenov',
        'standart_value': 25,
        'history_add': 'NASRAL',
        "func_event": ['test_func_events']
    },
}  # Standard actions performed by people depending on conditions, event=action, for clarity (Type:
# "name_event" = Name of the action,
# "func_event" = Function performed under successful conditions,
# "history_add" = What must be added to person's history after exec function (Optional),
# "need" = What need does the action relate to (what need is needed to perform the action. Optional) (!not to be confused with needs),
# "after" = What action must be exec after current,
# the rest = Conditions)

#  Setting up config

if patronymic:
    db_values.update({"patronymic": ["TEXT", ["random", patronymic_l]]})
    default_requiments.update({"patronymic": 0})

if money:
    db_values.update({"money": ["INT", 0]})
    default_requiments.update({"money": 0})

if history:
    db_values.update({"history": ["LONGTEXT", '']})

if len(surnames_l) == 0:
    surnames_l = ["Doe"]
if len(names_l) == 0:
    surnames_l = ["John"]
if len(patronymic_l) == 0:
    surnames_l = ["Doevich"]

pers_params = [f"{i} {db_values[i][0]}" for i in db_values]
pers_params_nf = [f"{i}" for i in db_values]

db_name = f"{db_name_raw}.db"
