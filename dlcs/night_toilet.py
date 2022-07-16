from random import randint


def create_person(id, name):
    print(f"{id} - {name}")


def create_item(id, name, params):
    print(f"{id} - {name} - {params}")


cities = ["Tver", "Moscow", "Saratov", "Saint-Petersburg", "Minsk"]


def rand_def(list_profs):
    return list_profs[randint(0, len(list_profs) - 1)]


def rand_def_ex(list_profs, *pl_profs):
    list_profs += pl_profs
    return list_profs[randint(0, len(list_profs) - 1)]


Person.create_item = create_item
Person.create_person = create_person
add_person_parameter("born", "DATA", default="05.06.2007")
add_person_parameter("country", "TEXT", default="Russia")
add_person_parameter("city", "TEXT", default=["random", cities])
add_person_parameter("prof", "TEXT", default=["function", rand_def, [["Mechanic", "Firefighter", "Musician"]]])
add_person_parameter("prof_ex", "TEXT", default=["function", rand_def_ex, [["Mechanic", "Firefighter", "Musician"], "Teacher", "Police man"]])
