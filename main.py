################################################################################
# main.py - This handles the game loop. it will allow the user to enter and exit
# the game based on their input   
#
# author: Brian Bessler
#
################################################################################

#import json
import sys
from gameboard import GameBoard
from play import Play

#instance of gameboard() to draw everything needed
g_board = GameBoard()
#strings acceptable to be typed when deciding to play or exit
exit_words = ["e", "E", "exit", "Exit", "EXIT"] 
play_words = ["p", "P", "play", "Play", "PLAY"]

#checks the user input against the words sent in the array
#if any are true, it will return true, otherwise, false
def user_input_check(test_arr, input):
    for test in test_arr:
        if test == input:
            return True
    return False

#clears the screen and exits the game
def exit_game():
    g_board.clear()
    sys.exit()

#This handles the main parts of the program
if __name__ == '__main__':    
    g_board.draw_title()        
    to_exit = False #used to check if the users wants to exit
    to_play = False #used to check if the user chose to play
    user_input = ''
    
    while not to_exit: #while the player chose not to exit
        g_board.clear()
        g_board.draw_main_menu()
        user_input = input("      Would you like to play or exit?: ")
        #checks the user input against the exit and play words
        to_exit = user_input_check(exit_words, user_input)
        to_play = user_input_check(play_words, user_input)
        if to_play: #if play word typed
            blackjack = Play() 
            blackjack.main() #play handles the gameplay
        if to_exit: #if exit word typed
            exit_game()
        if not to_play and not to_exit: #if the input is wrong, this helps the user try again
            input("      Input not understood. Press enter to try again")
            g_board.clear()
    
    
    
