"""
Author: James Pirie
Program: Future Family Register Administration Program

**** RESUBMISSION NOTES ****
- Fixed an error where you couldn't re enter the change name when it was wrong
- Ensured the balance system works in full
- Ensured that the information is displayed on exit
"""


YES = ["yes", "y", "ya", "yeah"]
STARTING_CREDITS = 50000


class Family:
    """A family object, in which all the attributes of a family and
   methods will be stored in an object oriented manner"""
    global YES
    global STARTING_CREDITS

    def __init__(self, last_name):
        """Initialize every required variable for the family object"""
        self.surname = last_name  # last name of the family
        self.family_total = {}  # every member of the family with an alive or dead status
        self.list_of_duplicates = {}  # if there is a duplicate person, store how many duplicates there are
        self.list_of_clones = []  # a list of every clone owned by the family
        self.list_of_clone_numbers = {}  # a dictionary of the number of clones there are of a specific name
        self.balance = STARTING_CREDITS  # initializing the balance
        self.list_of_dead = []  # a list of every deceased family member
        self.order_of_birth_number = 1
        self.order_of_birth = {}
        self.list_of_transactions = []

    def birth(self):
        cost = -5000
        print(f"You have: {self.balance} dollars")
        """Register a new born member to the family object"""
        alive = True  # set the default status for a person to alive
        baby_name = input("What is the new born's name?: ")  # ask the user to choose a name for the child
        valid_name = verify_name(baby_name)  # ensure the name is valid
        if baby_name in self.family_total.keys():  # check if the name is already taken
            valid_name = False
        while not valid_name:  # if the name is already taken ask the user to readout the name
            print("Name must not be the same as any other family member, be at least 3 letters long "
                  "and contain only english characters")
            baby_name = input("What is the new born's name?:")
            valid_name = verify_name(baby_name)  # check the new name is valid
        baby = {baby_name.strip(): alive}  # if it is valid append it to the dictionary with the alive status
        if baby_name in self.list_of_duplicates.keys():  # add the name to the count of duplicates
            self.list_of_duplicates[baby_name] += 1  # mainly if someone used to be called this name
        else:  # if nobody has every been called this name create a new dictionary key
            baby_record = {baby_name.strip(): 1}
            self.list_of_duplicates.update(baby_record)
        self.family_total.update(baby)  # append it to the dictionary
        transaction = f"{baby_name} was born and the family received 5000 credits"
        self.list_of_transactions.append(transaction)
        self.balance -= cost
        menu()  # reprint the main menu

    def death(self):
        cost = -10000
        print(f"You have: {self.balance} dollars")
        """Register the death of a family member"""
        number_of_alive = len(list(self.list_of_duplicates))
        if number_of_alive > 0:  # make sure there are alive people to register as dead
            dead_name = input("What is the newly deceased name?: ")  # ask who has died
            person_is_alive = False  # change the individuals status from alive to dead
            while dead_name not in self.family_total:  # make sure the selected name is in the alive list
                print("This is not a family member")  # if not in the list ask for the name again
                dead_name = input("What is the newly deceased name?: ")

            if dead_name in self.family_total.keys():  # check if the new dead person is a duplicate
                person_is_alive = self.family_total[dead_name]  # set a for status boolean to be used later
            if self.list_of_duplicates[dead_name] > 1:  # check if there are more than one duplicates of dead
                number_of_choices = []
                for i in range(self.list_of_duplicates[dead_name]):  # print all alive people for user to choose
                    print(f"{i + 1}) {dead_name}")
                    number_of_choices.append(str(i + 1))
                which_to_kill = input(f"Which {dead_name} has died?")  # ask the user which one has died
                while which_to_kill not in number_of_choices:  # make sure the person that has died was alive
                    print("This is not an option")
                    which_to_kill = input(f"Which {dead_name} has died?")  # if not alive ask for name again
            exit_condition = False  # create an exit condition for a loop
            while not exit_condition:
                if dead_name in self.family_total.keys() and person_is_alive:  # register the dead guy as dead
                    self.family_total[dead_name] = False  # set the individual to dead in the dictionary
                    self.list_of_duplicates[dead_name] -= 1  # minus one from the count of people with the same name
                    self.list_of_dead.append(dead_name)  # add dead person to list of dead people
                    self.balance -= cost  # give the family 10k dollars
                    transaction = f"{dead_name} died and the family received 10000 credits"
                    self.list_of_transactions.append(transaction)
                    exit_condition = True  # exit the loop
                else:  # check for incorrect names
                    print("This person is either not in your family or already dead")
                    try_again = input("Would you like to try again?: ")  # if invalid name ask to try again
                    if try_again not in YES:  # if they say no end the loop
                        exit_condition = True
                    else:  # if they say yes ask again
                        print(f"The name you have entered is not a member of the family")
                        dead_name = input("What is the newly deceased name?: ")
        else:
            print("There are no alive people")
        menu()  # reprint the main menu

    def change_name(self):
        print(f"You have: {self.balance} dollars")
        """Register a name change for a member of the family object"""
        subject_name = input("What is the name of the person you would like to change?: ")  # ask which name will change
        cost = 10000  # check the family has enough money
        enough_money = self.balance > cost
        exit_condition = False
        if enough_money:
            while not exit_condition:  # error checking loop
                invalid_name = False
                subject_is_alive = False
                if subject_name.strip() in self.family_total.keys():
                    subject_is_alive = self.family_total[subject_name]
                if subject_name.strip() not in self.family_total.keys() or not subject_is_alive:
                    print("The person you have selected is not a member of your family")
                    invalid_name = True
                if invalid_name:  # if something is wrong with the name ask if they would like to try again
                    print("The person you entered either does not exist or is dead")
                    exit_loop = input("would you like to try again?")
                    if exit_loop.lower().strip() in YES:
                        display_living_people_in_family(self)
                        subject_name = input("Please re enter the name of the person: ")
                    else:
                        exit_condition = True
                else:  # if the name is valid then ask what the new name for the person should be
                    new_name = input(f"What would you like to change {subject_name}'s name to?: ")
                    new_name_filtered = new_name.strip()
                    valid_name = verify_name(new_name_filtered)  # ensure the name is valid
                    while not valid_name:  # if the name is not correct ask for it again
                        print("Name must only contain only english characters and be at least 3 letters long")
                        new_name = input(f"What would you like to change {subject_name}'s name to?: ")
                        new_name_filtered = new_name.strip()  # strip it for analysis
                        valid_name = verify_name(new_name_filtered)  # check it again to see if it has changed
                    if new_name_filtered in self.list_of_duplicates:  # if there is already a person with the name add
                        self.list_of_duplicates[new_name_filtered] += 1  # add to the number of people with same name
                    else:  # if there are no people with the name add the name to the possible duplicate dictionary
                        new_name_duplicate_record = {new_name_filtered: 1}
                        self.list_of_duplicates.update(new_name_duplicate_record)
                    new_name_record = {new_name_filtered: True}
                    self.family_total.update(new_name_record)
                    exit_condition = True
                    self.balance -= cost
                    transaction = f"{subject_name}'s name was changed for {cost} credits"
                    self.list_of_transactions.append(transaction)
            if subject_name in self.family_total:
                del self.family_total[subject_name]  # delete the old version of the name from the family total
                self.list_of_duplicates[subject_name] -= 1  # take away one from list of duplicates of the old name
        menu()  # print the main menu

    def order_a_clone(self):
        cost = int(STARTING_CREDITS / 2)  # set the cost of a clone to 25k
        print(f"You have: {self.balance} dollars")
        """Register a clone of a deceased member of the family object"""
        enough_money = self.balance > cost  # check if the user has enough money
        who_to_clone = input("Who would you like to clone?: ")  # if enough
        if len(who_to_clone) == 1:  # check if there is one word in the name
            who_to_clone_filtered = who_to_clone.strip()  # filter out extra speeches
        else:
            who_to_clone_filtered = who_to_clone  # if nothing wrong with the name leave it as is

        exit_condition = False
        while not exit_condition:  # create a loop to check of the user can actual make a clone
            # make sure the user has enough money and that the name being cloned actual is a person that is dead
            if who_to_clone_filtered in self.family_total.keys() and not \
                    self.family_total[who_to_clone_filtered] and enough_money:
                persons_first_name = who_to_clone.split()  # make it so only the first name is taken by the clone
                persons_first_name.append("Filler Name")  # if the user only has one name create filler to prevent error
                clone_first_name = persons_first_name[0]  # take only the first name and give it to the clone
                if clone_first_name not in self.list_of_clone_numbers.keys():  # keep track of how many clones there are
                    record_of_clone = {clone_first_name: 1}  # if the clone is not in the records add it to the records
                    self.list_of_clone_numbers.update(record_of_clone)  # add the clone to the record
                    new_clone_name = persons_first_name[0] + f"-{self.list_of_clone_numbers[clone_first_name]}"
                    self.list_of_clones.append(new_clone_name)  # append the clones final name with number to the record
                else:  # if the clone is the first clone of that person give it a name with the first number
                    self.list_of_clone_numbers[clone_first_name] += 1
                    new_clone_name = persons_first_name[0] + f"-{self.list_of_clone_numbers[clone_first_name]}"
                    self.list_of_clones.append(new_clone_name)  # add the new clone to the list
                transaction = f"{who_to_clone} was cloned for {cost} credits"
                self.list_of_transactions.append(transaction)
                self.balance -= cost  # pay for the clone
                exit_condition = True

            else:  # if the person types in a name that is not in the list ask if they want to try again
                print("The person you would like to clone either doesn't exist or is still alive or you don't have "
                      "enough money")
                try_again = input("Would you like to try again?")
                if try_again.strip().lower() in YES:  # if they do want to try again ask them for who they want to clone
                    who_to_clone = input("Who would you like to clone?: ")
                    print("The name you have entered is either alive or has never been alive")
                else:  # if they say no then exit the program
                    exit_condition = True

        menu()


def menu():
    """Display the options for the user"""
    # print out every option the user has
    print("---------- | Main Menu | ----------")
    print("1) Enter Death")
    print("2) Enter Birth")
    print("3) Create Clone")
    print("4) Name Change")
    print("5) View Data")
    print("Type 'exit' to exit")


def select_option(family_object):
    """Allow the user to pick from one of the options"""
    exit_menu = False  # create a exit condition for the loop
    while not exit_menu:
        # create a list of valid options for the user to choose from
        valid_options = ["one", "1", "two", "2",
                         "three", "3", "four", "4",
                         "five", "5", "exit", "enter death",
                         "enter birth", "create clone",
                         "name change", "view data"]
        # ask the user what they would like to pick from the menu
        what_to_do = input("type in what you would like to do or, the number next to it: ")  #
        what_to_do_filtered = what_to_do.strip().lower()  # filter the users message so it is easier to understand
        exit_condition = False
        while not exit_condition:  # value checking
            if what_to_do_filtered in valid_options:
                exit_condition = True

            else:  # if the user enters an invalid input ask again
                menu()  # reprint the menu so they can see the options again
                print("You have not entered a valid input")  # inform the user that they entered an invalid input
                what_to_do = input("type in what you would like to do or, the number next to it: ")
                what_to_do_filtered = what_to_do.strip().lower()  # test again for a valid input
        # setup the values associated with each option, so the program can better understand when a user chooses
        options = {"1": ["one", "1", "enter death"],
                   "2": ["two", "2", "enter birth"],
                   "3": ["3", "three", "create clone"],
                   "4": ["4", "four", "name change"],
                   "5": ["5", "five", "view data"]}

        if what_to_do_filtered == "exit":
            # if the user wants to exit the code exit
            display_living_people_in_family(family_object)
            display_dead_people_in_family(family_object)
            display_all_clones(family_object)
            exit_menu = True
        elif what_to_do_filtered in options["1"]:
            # if the user wants to register a death display a list of the living then call the death method
            display_living_people_in_family(family_object)
            family_object.death()
        elif what_to_do_filtered in options["2"]:
            # if the user wants to register a birth call the birth method
            family_object.birth()
        elif what_to_do_filtered in options["3"]:
            # if the user wants to order a clone display a list of the dead and call the clone method
            display_dead_people_in_family(family_object)
            family_object.order_a_clone()
        elif what_to_do_filtered in options["4"]:
            #  if the user wants to change a name display a list of living people and call the change name function
            display_living_people_in_family(family_object)
            family_object.change_name()
        elif what_to_do_filtered in options["5"]:
            #  if the user wants to view the family info display all the living members, all the dead and all the clones
            print("==========| Data |==========")
            display_living_people_in_family(family_object)
            display_dead_people_in_family(family_object)
            display_all_clones(family_object)
            display_financial_records(family_object)
            menu()  # reprint the main menu


def verify_name(name_parameter):
    """Check if the user has input a valid name"""
    name = name_parameter.strip().lower()  # remove all extra space and capital letters
    correct_name = False
    valid_characters = False
    correct_letters = 0
    for i in range(len(name)):  # check every character is an English letter
        if name[i].isalpha() or name[i].isspace():
            correct_letters += 1
    if correct_letters == len(name):  # if every letter is an English letter mark the name as correct
        valid_characters = True
    if valid_characters and len(name) >= 3:  # if the length of the name is at least 3 letters mark it as correct
        correct_name = True
    return correct_name  # if the name is not any of the above it will be marked as false


def create_family_object():
    """Create an instance of the family object and ensure a valid surname is input"""
    family_name = input("What is your family name: ")  # ask the user for a family name
    validated = verify_name(family_name)  # make sure it is a valid name
    exit_condition = False
    while not validated or exit_condition:  # if the name is not valid ask for the name again with an error message
        print("Name must only contain only english characters and be at least 3 letters long")
        family_name = input("What is your family name: ")
        validated = verify_name(family_name)
    family_obj = Family(family_name)  # create a family object with the surname
    return family_obj  # return the family object


def display_financial_records(family_object):
    print(f"{family_object.surname} financial records:")
    for i in range(len(family_object.list_of_transactions)):
        print(f"-{family_object.list_of_transactions[i]}")
    print(f"starting balance: {STARTING_CREDITS}")
    print(f"finale balance: {family_object.balance}")


def display_living_people_in_family(family_object):
    """Print out the living members of the family object"""
    list_of_names = list(family_object.list_of_duplicates)  # set the keys of the dictionary to a list of strings
    if len(list_of_names) == 0:  # if there are no members print this
        print(f"There are no living members of {family_object.surname}")
    else:  # if there are members iterate through the list, if there are duplicates print the duplicates
        print(f"Every living member of {family_object.surname}")
        for i in range(len(family_object.list_of_duplicates)):
            for x in range(family_object.list_of_duplicates[list_of_names[i]]):
                print(f"-{list_of_names[i]}")  # display a formatted name string


def display_dead_people_in_family(family_object):
    """Display all the deceased members of the family object"""
    if len(family_object.list_of_dead) == 0:  # check if there are dead people in the list
        print(f"There are no dead members of {family_object.surname}")
    else:  # if there are members iterate through the list, if there are duplicates print the duplicates
        print(f"Every dead member of {family_object.surname}")
    for i in range(len(family_object.list_of_dead)):
        print(f"-{family_object.list_of_dead[i]}")  # display a formatted name string


def display_all_clones(family_object):
    """Display all clones belonging to the family object"""
    print(f"All clones of the {family_object.surname} family")
    for i in range(len(family_object.list_of_clones)):  # iterate through the list of clones
        print(f"- {family_object.list_of_clones[i]}")


def main():
    """The main function for the code structure"""
    family = create_family_object()  # create the family object
    menu()  # display the options in the menu
    select_option(family)  # ask the user to pick which one
    display_living_people_in_family(family)
    display_dead_people_in_family(family)
    display_all_clones(family)
    display_financial_records(family)


# run the code
if __name__ == '__main__':
    main()
