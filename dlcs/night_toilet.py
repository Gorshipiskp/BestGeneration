def create_person(id, name):
    print(f"{id} - {name}")


def create_item(id, name, params):
    print(f"{id} - {name} - {params}")


Person.create_item = create_item
Person.create_person = create_person
