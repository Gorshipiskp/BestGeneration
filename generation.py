import config


class Person:

    def __init__(self):
        self.id = 00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
        if config.history:
            self.history = []  # History of actions
        self.name = "Никита"  # First name
        self.surname = "Демидов"  # Second name
        self.patronymic = "Сергеевич"  # Middle name
        self.age = 0  # Days lived
        self.gender = 1  # Gender's ID
        self.parents = []  # Parents ID
        self.education = []  # Educations ID's

    def get_age(self):
        return self.age

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_surname(self):
        return self.surname

    def get_middle_name(self):
        return self.patronymic

    def get_full_name(self):
        return f"{self.surname} {self.name} {self.patronymic}"

    def get_education(self):
        return self.education

    def get_gender(self):
        return self.gender

    def get_parents(self):
        return self.parents

    if config.history:
        def get_history(self):
            return self.history


class register:

    def __init__(self):
        self.cls = Person

    def new_method_person(self, func):
        self.cls.test_def = func.__get__(self.cls)
