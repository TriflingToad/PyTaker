from textwrap import dedent
import time

class PyTaker:
    # fonts from https://texteditor.com/multiline-text-art/
    def __init__(self):

        self.wall = '⬛'
        self.air = '⬜'
        self.player = '🐸'
        self.enemy = '💔'
        self.stone = '🪨'
        self.goal = '🩷'
        # dedent removes tabs for readability
        # strip removes ending and leading newlines for readability
        self.board_txt = dedent("""
        ⬛⬛⬛⬛⬛⬛⬛⬛⬛
        ⬛⬛⬛⬛⬛⬜🐸⬛⬛
        ⬛⬛⬜⬜💔⬜⬜⬛⬛
        ⬛⬛⬜💔⬜💔⬛⬛⬛
        ⬛⬜⬜⬛⬛⬛⬛⬛⬛
        ⬛⬜🪨⬜⬜🪨⬜⬛⬛
        ⬛⬜🪨⬜🪨⬜⬜🩷⬛
        ⬛⬛⬛⬛⬛⬛⬛⬛⬛
        """).strip()

        # removes newlines for readability
        self.board = list(self.board_txt.replace("\n", ""))

        # information about level
        self.moves = 23
        self.won = False
        self.player_location = (7, 2)
        self.level_dimensions = self.get_dimensions(self.board_txt)

    def get_dimensions(self, level_txt):
        level_split = level_txt.split("\n")
        board_width = len(level_split[0])
        board_height = len(level_split) + 1  # +1 because last line doesn't have a \n character
        xy_tuple = board_width, board_height
        # print(xy_tuple)
        return xy_tuple  # tuple

    def replace_char(self, x, y, char):
        # replaces a charicter given the x and y. Top left is 1,1 bottom right is 5,5 (assuming 5x5)
        location_to_replace = ((y - 1) * self.level_dimensions[1]) + (x - 1)
        # print(location_to_replace)
        self.board[location_to_replace] = char

    def get_raw(self, x, y):
        # replaces a charicter given the x and y. Top left is 1,1 bottom right is 5,5 (assuming 5x5)
        return ((y - 1) * self.level_dimensions[1]) + (x - 1)

    def print_board(self):
        print_string = ""
        for i in range(len(self.board)):
            print_string += self.board[i]
            if (i+1) % self.level_dimensions[1] == 0:
                print_string += "\n"
        print(print_string, end="")
        print(f"{self.moves} moves left. R to restart")

    def reset(self):
        self.moves = 21
        self.won = False
        self.board = list(self.board_txt.replace("\n", ""))
        self.player_location = (7, 3)
        self.level_dimensions = self.get_dimensions(self.board_txt)


    def move(self, u_input):
        self.moves -= 1

        if self.moves < 1:
            print("You ran out of moves.")
            input("enter to restart")
            print(dedent("""
            ░▄▀▄░█░█░▀█▀░░░▄▀▄▒█▀░░░█▄░▄█░▄▀▄░█░█░██▀░▄▀▀
            ░▀▄▀░▀▄█░░█░░░░▀▄▀░█▀░░░█░▀░█░▀▄▀░▀▄▀░█▄▄░▄██
            """))
            time.sleep(2)
            self.reset()
            return

        pl = self.player_location
        match u_input.lower():
            case "w":
                loc_tile_ahead = (pl[0], pl[1] - 1)
                loc_tile_behind = (pl[0], pl[1] + 1)
                loc_tile_2head = (pl[0], pl[1] - 2)
            case "a":
                loc_tile_ahead = (pl[0] - 1, pl[1])
                loc_tile_behind = (pl[0] + 1, pl[1])
                loc_tile_2head = (pl[0] - 2, pl[1])
            case "s":
                loc_tile_ahead = (pl[0], pl[1] + 1)
                loc_tile_behind = (pl[0], pl[1] - 1)
                loc_tile_2head = (pl[0], pl[1] + 2)
            case "d":
                loc_tile_ahead = (pl[0] + 1, pl[1])
                loc_tile_behind = (pl[0] - 1, pl[1])
                loc_tile_2head = (pl[0] + 2, pl[1])
            case "r": # reset
                self.reset()
                return
            case _:
                loc_tile_ahead = pl
                print("Sorry didn't understand.")
                self.moves += 1
                return

        # gets the sprites of the tile ahead, and 2 ahead.
        tile_moving_to = self.board[self.get_raw(*loc_tile_ahead)]
        tile_scooting_to = self.board[self.get_raw(*loc_tile_2head)]

        # checks for out of bounds and... also out of bounds, but worse
        valid_move = False
        oob = 1 <= loc_tile_ahead[0] <= self.level_dimensions[0] and 1 <= loc_tile_ahead[1] <= self.level_dimensions[1]
        hit_wall = (tile_moving_to != self.wall)
        if oob and hit_wall: # want these to be True
            print(f"moving to: {tile_moving_to}")
            valid_move = True
        else:
            print("ILLEGAL MOVE")
            if not hit_wall:
                print("You tried to move to a black tile")
            elif not oob:
                print("You tried to move out of the entire map. How'd ya manage that?")
            nl = pl

        #Check if player has reached the goal
        self.won = tile_moving_to == self.goal

        #SCOOTING
        scooting = False
        if tile_moving_to == self.enemy or tile_moving_to == self.stone:
            scooting = True

            print(f"scooting: {tile_moving_to} into {tile_scooting_to}")

            enemy_killed = False
            if tile_moving_to == self.enemy and (tile_scooting_to == self.wall or tile_scooting_to == self.stone):
                print("You killed an enemy!")
                enemy_killed = True
            elif tile_scooting_to == self.wall or (tile_moving_to == self.stone and tile_scooting_to == self.stone):
                print("You tried scooting something into a wall.")
                valid_move = False

        if valid_move:
            if scooting and not enemy_killed:
                self.replace_char(*loc_tile_2head, tile_moving_to)  # move the one infront of player 1 forward
            self.replace_char(*loc_tile_ahead, self.player) # make tile where player wants to go, player
            self.replace_char(*self.player_location, self.air) # make tile where player WAS white
            self.player_location = loc_tile_ahead

            if self.won:
                self.win()
        else:
            self.moves += 1

    def start(self):
        print("\n" * 50)  # Move screen to bottom of scrollbar

        print("loading", end="")
        for i in range(10):
            time.sleep(0.5)
            print(".", end="")
        print("\n\n --==+TriflingToad Presents+==--")
        time.sleep(2)
        print(dedent("""\n
                \t░▒█▀▀█░█░░█░▀▀█▀▀░█▀▀▄░█░▄░█▀▀░█▀▀▄
                \t░▒█▄▄█░█▄▄█░░▒█░░░█▄▄█░█▀▄░█▀▀░█▄▄▀
                \t░▒█░░░░▄▄▄▀░░▒█░░░▀░░▀░▀░▀░▀▀▀░▀░▀▀
                \t    Helltaker, but in python!
                \n"""))

        for i in range(5):
            time.sleep(0.5)
            print(".", end="")
        print("\n")

        print("Hi. Thanks for playing. This is my attempt at making a python text version of the videogame Helltaker, a short but difficult puzzle game.")
        time.sleep(3)
        print("Though I only made the first level I figured it would be nice to give a guide. Here are the items:")
        time.sleep(4)
        print(f"\t1: This, {self.wall} is a wall. You can't pass through them.")
        time.sleep(1)
        print(f"\t2: This, {self.air} is air. You CAN walk through it.")
        time.sleep(1)
        print(f"\t3: This is you, {self.player}. In the OG game you are a buff guy, but since it's my version I made it a frog.")
        time.sleep(1)
        print(f"\t4: This is an enemy, {self.enemy}. They don't want to hurt you and won't move, but if they get in your way you can crush them against a wall.")
        time.sleep(1)
        print(f"\t5: This, {self.stone} is a stone. They act like enemies but you can't crush them.")
        time.sleep(1)
        print(f"\t6: The goal of the game is to reach this, {self.goal}. It is a 'sharply dressed demon girl' as the OG developer puts it.")

        time.sleep(2)
        print("\nTip: set your width pretty large, and use an IDE to run this if possible.")
        time.sleep(2)
        print("For credits, here's a link to the OG game: https://store.steampowered.com/app/1289310/Helltaker/")
        time.sleep(2)
        print("\tGood Luck!\n  ~TriflingToad\n\n")
        time.sleep(4)


        # Main Loop
        while not self.won:
            self.print_board()
            self.move(input("\n WASD to move: "))

    def win(self):
        print("\n\n")
        time.sleep(1)
        print("Looking in the corner you see a woman sorting through papers. ")
        time.sleep(2)
        print("You get closer and see that she is dressed in a professional looking black suit with a blood red undercoat.")
        time.sleep(2)
        print("This matches well with her red skin and her tail with a sharp point at the end.")
        time.sleep(2)
        print("She looks exhausted, with bags under her eyes and glasses nearly falling off, she yawns before speaking:")
        time.sleep(4)

        print("\n\t\"Name's Pandemonica, Hell's Customer Service. How may I serve you?\"")
        time.sleep(3)
        print("\n1: We can figure something out at my place.")
        time.sleep(0.5)
        print("2: Maybe can I serve YOU instead?")
        time.sleep(0.5)
        u_input = input("What do you respond with? 1 or 2: ")


        if u_input == "1":
            time.sleep(2)
            print("\nShe lets out a sharp and intence chuckle.")
            time.sleep(2)
            print("\n\t\"You thought you were leaving hell alive? How delusional.\"")
            time.sleep(2)
            print("\nShe took your face in her hands and snapped your neck with professional gentleness.")
            time.sleep(2)
            input("\nenter to continue...")
            time.sleep(1)
            print(dedent("""
            ▀██▀▀█▄               ▀██     ▀██▀▀▀▀█               ▀██   ██                   
             ██   ██   ▄▄▄▄     ▄▄ ██      ██  ▄    ▄▄ ▄▄▄     ▄▄ ██  ▄▄▄  ▄▄ ▄▄▄     ▄▄▄ ▄ 
             ██▀▀▀█▄  ▀▀ ▄██  ▄▀  ▀██      ██▀▀█     ██  ██  ▄▀  ▀██   ██   ██  ██   ██ ██  
             ██    ██ ▄█▀ ██  █▄   ██      ██        ██  ██  █▄   ██   ██   ██  ██    █▀▀   
            ▄██▄▄▄█▀  ▀█▄▄▀█▀ ▀█▄▄▀██▄    ▄██▄▄▄▄▄█ ▄██▄ ██▄ ▀█▄▄▀██▄ ▄██▄ ▄██▄ ██▄  ▀████▄ 
                                                                                    ▄█▄▄▄▄▀ 
            """))
            time.sleep(1)
            print("                            (try again)\n\n")
            time.sleep(2)
            self.reset()
            return
        elif u_input == "2":
            time.sleep(2)
            print("\nShe stops shuffling her papers around. Looking you not quite in the eye she gratefully says,")
            time.sleep(3)
            print("\n\t\"Sweet of you to offer. I could really use some coffee. I'm not myself without it.\"")
            time.sleep(2)
            input("\nenter to continue...")
            time.sleep(1)
            print(dedent("""
             ▄█▀▀▀▄█                                         
             ██▄▄  ▀  ▄▄▄ ▄▄▄    ▄▄▄▄    ▄▄▄▄   ▄▄▄▄   ▄▄▄▄  
              ▀▀███▄   ██  ██  ▄█   ▀▀ ▄█▄▄▄██ ██▄ ▀  ██▄ ▀  
            ▄     ▀██  ██  ██  ██      ██      ▄ ▀█▄▄ ▄ ▀█▄▄ 
            █▀▄▄▄▄█▀   ▀█▄▄▀█▄  ▀█▄▄▄▀  ▀█▄▄▄▀ █▀▄▄█▀ █▀▄▄█▀ 
            """))
            time.sleep(1)
            print("             Thanks for playing.")
            return


    def print_board_ascii(board):
        # UNUSED
        # This is when I thought I was going to make minesweeper.
        # It prints a 5x5 board (a 25 char long string) with a pattern.
        # example for 2x2:
        #  +-+-+
        #  |1|2|
        #  +-+-+
        #  |3|4|
        #  +-+-+

        def print_line(starting_val):
            # prints 5 items in the array using | every other (and the start)
            line = ["|"]  # start with a |
            length = 5
            for i in range(length):
                line.append(board[starting_val + i])  # match from the actual board
                if i < length - 1:  # add a | every other
                    line.append("|")
            line.append("|")  # add a | at the end
            return "".join(line)

        inbetween = "+-+-+-+-+-+"
        for i in range(0, 25, 5):
            print(inbetween)
            print(print_line(i))
        print(inbetween)


pt = PyTaker()
pt.start()