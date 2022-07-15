#  Value parameters

language = "English"                # Program's language (Available: Russian and English)
start_count = 2                     # How many peoples should spawn at start
db_name = "humans"                  # Filename of DB (without extension)


#  Bool parameters

immortal = False                    # Should people die?
money = True                        # Should money system is turn on?
debug = False                       # Do debug is turn on?
show_errors_description = True      # Show error's description (like desc what went wrong for more understandable debug)?
history = True                      # Is program must write every person's history (Their moves, actions etc.)?
patronymic = True                   # Use patronymic? (Like surname, but father's name in surname style)
restart = False                     # Should restart simulation and erase it data one time?
restart_always = True               # Should restart simulation and erase its data every run of simulation?


#  Big (Lists, Arrays) parameters

surnames_l = ["Demidov", "Tkachenko", "Pimenov", "Evdokimov", "Knyazev"]
names_l = ["Nikita", "Kirill", "Sergey", "Artyom", "Anton"]
patronymic_l = ["Sergeevich", "Andreevich"]


#  Setting up config

if len(surnames_l) == 0:
    surnames_l = ["Doe"]
if len(names_l) == 0:
    surnames_l = ["John"]
if len(patronymic_l) == 0:
    surnames_l = ["Doevich"]
