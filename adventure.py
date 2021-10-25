"""
 adventure.py

 Programmeren 2
 Luna Ellinger

 - Contains the class Adventure and the game main loop.
 - The Adventure class contains items required for playing the Adveture game.
"""

from loader import load_room_graph


class Adventure():

    def __init__(self, filename):
        """
        Initializes the Adventure game by defining the current room object
        and creating an empty list for the player inventory.
        Takes the filename (str) of the game as parameter that was specified at
        the command line.
        Returns nothing.

        """

        self._current_room = load_room_graph(filename)
        self.player_inventory = []

    def synonyms(self, command):
        """
        Determines whether given command is a synonym. If so, returns
        the full word of the synonym (str).
        Takes command (str) as parameter.
        """

        # open synonym file
        with open("data/Synonyms.dat", "r") as synonyms_file:
            count_synonyms = 9

            # for loop over lines in file
            for line in range(count_synonyms):
                line = synonyms_file.readline()

                # strip and split line on "=" sign (eg Q=QUIT)
                line = line.rstrip().split("=")
                synonym = line[0]
                full_word = line[1]

                if command == synonym:
                    return full_word

    def room_description(self):
        """
        Returns the description (str) of the current room, be it short or long.
        Takes no parameters

        """

        return self._current_room.description()

    def move(self, direction, index):
        """
        'Moves' player to a different room by changing "current" room,
        if possible. If this is possible, returns boolean value 'True',
        else 'False'.
        Takes two parameters, the direction and list index of destination room.
        """

        if self._current_room.has_connection(direction) is True:
            self._current_room = self._current_room.get_connection(direction, index)
            return True

        return False

    def list_room_inventory(self):
        """
        Places all the items of the room inventory in a list and returns this
        list.
        Takes no parameters.
        """
        room_inventory = self._current_room.room_inventory

        items = [item.item_description() for item in room_inventory]
        return items

    def list_player_inventory(self):
        """
        Places all the items of the room inventory in a list and returns this
        list.
        Takes no parameters.
        """

        items = [item.item_description() for item in self.player_inventory]
        return items

    def condition(self, direction):
        """
        Determines to which room the player should go when room for given
        direction is conditional.
        Returns the list index (int) of the destination room.
        Takes 'direction' (str) as parameter.
        """

        # set index to default value (end of list)
        index = -1

        condition_items = self._current_room.condition_items

        # loop over conditional items of room for given direction
        for item_room in condition_items[direction]:

            # loop over player inventory
            for item_player in range(len(self.player_inventory)):

                # when item is found in the player inventory, overwrite index
                # with the item index in the conditional_items list
                if item_room == self.player_inventory[item_player].item_name:
                    index = condition_items[direction].index(item_room)
        return index

    def take(self, item_input):
        """
        Simulates 'taking' an item by determinening whether the given command
        is an item in the nventory of the room. If so, appends item to player
        inventory and removes item from room inventory.
        Returns no values.
        Takes given item (str) as parameter.
        """

        # loop over room inventory
        for item in self._current_room.room_inventory:
            if item_input == item.item_name:

                # append object to player inventory (ie take item)
                self.player_inventory.append(item)

                # remove item from room inventory
                self._current_room.room_inventory.remove(item)

    def drop(self, item_input):
        """
        Simulates 'dropping' an item by determinening whether the given
        command is an item in the inventory of the player. If so, appends
        item to room inventory and removes item from room inventory.
        Returns no values.
        Takes the given item (str) as parameter.
        """

        # loop over player inventory
        for item in self.player_inventory:
            if item_input == item.item_name:

                # append item to room inventory list (ie drop item in room)
                self._current_room.room_inventory.append(item)

                # pop item from player inventor
                self.player_inventory.remove(item)

    def room_connection(self, direction):
        """
        Determines whether room has a connection for given direction.
        If so, returns boolean value 'True', else 'False'.
        Takes one parameter 'direction' (str).
        """
        if self._current_room.has_connection(direction) is True:
            return True
        return False

    def check_conditional_room(self, direction):
        """
        Determines whether room is conditional for given direction.
        If so returns boolean value 'True', else 'False.
        Takes one parameter 'direction' (str).

        """

        if len(self._current_room.connections[direction]) > 1:
            return True
        return False

    def room_has_inventory(self):
        """
        Determines whether room inventory contains items. If so returns
        the boolean value 'True', else 'False.
        Takes no parameters.
        """

        if len(self._current_room.room_inventory) > 0:
            return True
        return False

    def description_large(self):
        """
        Returns the large description of the current room (str).
        Takes no parameters.
        """

        return adventure._current_room.descrip_large

    def item_drop_check(self, item_input):
        """
        Takes an item name (str) as parameter and determines whether
        the item object to which the item name belongs is in
        the player inventory. If so, returns the True, else False.
        """

        for item in self.player_inventory:
            if item.item_name == item_input:
                return True

        return False

    def item_take_check(self, item_input):
        """
        Takes an item name (str) as parameter and determines whether
        the item object to which the item name belongs is in
        the current room inventory. If so, returns the True, else False.
        """

        for item in self._current_room.room_inventory:
            if item.item_name == item_input:
                return True
        return False

    def instructions(self):
        """
        Takes no paramaters other than self and returns the user instructions
        of the game (str).
        """
        return("You can move by typing directions such as EAST/WEST/IN/OUT"
               "\nQUIT quits the game."
               "\nHELP prints instructions for the game."
               "\nLOOK lists the complete description of the room and its contents."
               "\nINVENTORY lists all items in your inventory.")


if __name__ == "__main__":

    from sys import argv

    # check command line arguments
    if len(argv) not in [1, 2]:
        print("Usage: python3 adventure.py [name]")
        exit(1)

    # load the requested game or else Tiny
    print("Loading...")
    if len(argv) == 2:
        game_name = argv[1]
    elif len(argv) == 1:
        game_name = "Tiny"
    filename = f"data/{game_name}Adv.dat"

    # create game
    adventure = Adventure(filename)

    # welcome user
    print("Welcome to Adventure.\n")

    # print very first room description
    print(adventure.room_description())

    # prompt the user for commands until they type QUIT
    while True:

        # prompt, converting all input to upper case
        command = input("> ").upper()

        # create list of command
        command_split = command.split()

        # Set index to last element in list (will be used later to index
        # into correct room when room is conditional)
        room_index = -1

        # check whether command is two strings
        if len(command_split) == 2:

            # check whether first string of command is 'take'
            if command_split[0] == "TAKE":

                # check whether given item input is an item in the room
                if adventure.item_take_check(command_split[1]) is True:
                    print(f"{command_split[1]} taken")

                    # perform the actual 'take' of the item
                    adventure.take(command_split[1])
                else:
                    print("No such item.")

            # check whether first string of command is 'drop'
            elif command_split[0] == "DROP":

                # check whether given item input is an item in
                # the player inventory
                if adventure.item_drop_check(command_split[1]) is True:
                    print(f"{command_split[1]} dropped")

                    # perform the actual 'drop' of the item
                    adventure.drop(command_split[1])
                else:
                    print("No such item.")
            else:
                print("Invalid command.")

        # check whether command is one string
        elif len(command_split) == 1:

            # retrieves full word of synonym if command is synonym
            if len(command) == 1:
                command = adventure.synonyms(command)

            # CHECK ALL HELPER COMMANDS
            # print instruction if command is "HELP"
            if command == "HELP":
                print(adventure.instructions())

            # print large room description and room items if command is "LOOK"
            elif command == "LOOK":
                print(adventure._current_room.descrip_large)
                if adventure.room_has_inventory:
                    print(*adventure.list_room_inventory(), sep="\n")

            # print items in player inventory if command is "INVENTORY"
            elif command == "INVENTORY":
                if len(adventure.player_inventory) == 0:
                    print("Your inventory is empty")
                else:
                    print(*adventure.list_player_inventory(), sep="\n")

            # quit the game if command is "QUIT"
            elif command == "QUIT":
                break

            # check whether command is a valid move
            elif adventure.room_connection(command) is True:

                # check whether room is conditional for given direction
                if adventure.check_conditional_room(command) is True:
                    room_index = adventure.condition(command)

                # perform the move or other command
                if adventure.move(command, room_index) is True:

                    while adventure.room_connection("FORCED") is True:

                        # if check is true, room is conditional for given
                        # direction. Move is performed until check is false.
                        if adventure.check_conditional_room("FORCED") is True:
                            room_index = adventure.condition("FORCED")
                            adventure.move("FORCED", room_index)

                        else:
                            print(adventure.room_description())
                            adventure.move("FORCED", room_index)

                    print(adventure.room_description())

                    # prints room inventory (if there is any)
                    if adventure.room_has_inventory:
                        print(*adventure.list_room_inventory(), sep="\n")
            else:
                print("Invalid command.")
        else:
            print("Invalid command.")
