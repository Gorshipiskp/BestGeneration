from standart_functions import *


def create_person(id, name):
    print(f"{id} - {name}")


def create_item(id, name, params):
    print(f"{id} - {name} - {params}")


____cities = ["Tver", "Moscow", "Saratov", "Saint-Petersburg", "Minsk"]


def rand_def(list_profs):
    return list_profs[randint(0, len(list_profs) - 1)]


def rand_def_ex(list_profs: list, *pl_profs):
    list_profs += pl_profs
    return list_profs[randint(0, len(list_profs) - 1)]


add_person_parameter("work", "REAL", default=100)
add_requiment('work', 0)

add_person_parameter("city", "TEXT", default=["random", ____cities], num=3, remove_same=True, until_num=True)


#  add_types_reqs(rand_def)
#  add_person_parameter("born", "DATA", default="05.06.2007")
#  add_person_parameter("country", "TEXT", default="Russia")
#  add_person_parameter("city", "TEXT", default=["random", ____cities])
#  add_person_parameter("prof", "TEXT", default=["function", rand_def, [["Mechanic", "Firefighter", "Musician"]]])
#  add_person_parameter("prof_ex", "TEXT", default=["function", rand_def_ex, [["Mechanic", "Firefighter", "Musician"], "Teacher", "Police man"]])
#  Person.create_item = create_item
#  Person.create_person = create_person
