#things to add
##-second ship
##- two player
## -ships bigger than 1 space
## -more turns.. bigger board?..
## -let user pick amount of ships
from random import randint

#Functions

def create_board():
    """creates board"""
    newboard = []
    for num in range(5):
        newboard.append(["0"] * 5)
    return newboard

def print_board(tboard):
    """prints board"""
    for num in tboard:
        print ' '.join(num)

def rand_row(board1):
    """creates random row number"""
    random_row = randint(1, len(board1) - 1)
    return random_row

def rand_col(board2):
    """creates random column number"""
    rand_column = randint(1, len(board2) - 1)
    return rand_column

def guess_validate(num):
    if num < 1 or num > 5:
        return False
    else:
        return True

def duplicate_validate(row, col):
    if board[row - 1][col - 1] == "*":
        return False
    else:
        return True

print ""
print ""
print "Welcome to Battle Ship. If you can guess where my ship is in four turns, you win!"
print ""
print ""


#Running logic

play_again = 'yes'
while play_again == 'yes':
    #initializes board and coordinates
    board = create_board()
    ship1_row = int(rand_row(board))
    ship1_col = int(rand_col(board))
    print_board(board)
    for turn in range(4): # for loop is the amount of turns they have. In this case 4
        print ""
        print "ship row " + str(ship1_row)
        print "ship row " + str(ship1_col)
        print "You have " + str((range(4)[3] + 1) - turn) + " turns left."
        print "~~~~~~~~~~~~~~"
        while True: #This while loop askes for user input. Validates it's an integer between 1 and 5
            try:    #and makes sure it's a coordinate they already guessed
                guess_row = -3
                while guess_row < 1 or guess_row > 5:
                    try:
                        guess_row = int(raw_input("Guess Row:")) #get input
                        if guess_validate(guess_row) is False: #check to make sure it's in range
                            print "Invalid input"
                        else:
                            break
                    except ValueError:
                        print "Input not valid"
                guess_col = -3
                while guess_col < 1 or guess_col > 5:
                    try:
                        guess_col = int(raw_input("Guess Col:"))
                        #guess_col = 3
                        if guess_validate(guess_col) is False:
                            print "Invalid input"
                        else:
                            break
                    except ValueError:
                        print "Input not valid"
                if duplicate_validate(guess_row, guess_col) is False: #check to make sure it's not already guessed
                    print "You've already guessed this coordinate!"
                else:
                    break
            except ValueError:
                print "Not a valid input."
        print "~~~~~~~~~~~~~~"

        if guess_row == ship1_row and guess_col == ship1_col:
            print "It's a hit You win!"
            board[ship1_row - 1][ship1_col - 1] = "X"
            print_board(board)
            #ask user if they want to play again
            response = raw_input("Would you like to play again?")
            while response.lower() not in {'y', 'n', 'yes', 'no'}:  # Fill in the condition (before the colon)
                response = raw_input("Please enter yes or no: ")
            playagain = response
            break
        else: #continue game
            if turn != 3:
                print "Miss!"
                print "~~~~~~~~~~~~~~"
                board[guess_row - 1][guess_col - 1] = "*"
                print_board(board)
                print " this is turn", turn
                print "~~~~~~~~~~~~~~ end of continue"
            else: #end game
                print "~~~~~~~~~~~~~~ start of end else"
                print "Game over"
                print "My ship was at row %s, column %s!" % (ship1_col, ship1_row)
                board[ship1_row - 1][ship1_col - 1] = "X"
                print "~~~~~~~~~~~~~~"
                print_board(board)
                response = raw_input("Would you like to play again?")
                playagain = response
print "Thanks for playing"
