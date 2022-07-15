def new_event(id, name):
    for i in range(0, 100, 5):
        print(f"LOADING... ({i}%)")
    print("\nLOAD COMPLETED\n\n")
    print(f"New event - {id} - '{name}'")


Person.new_event = new_event
