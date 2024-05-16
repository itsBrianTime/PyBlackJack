################################################################################
# gameboard.py - this script will handle all drawing and clearing of the game -
#   - board. It will take in card values and print the board accordingly
#
# author: Brian Bessler
#
################################################################################

#import json
import os
import time
#import sys

class GameBoard(object):

    #globVar = "Global Variable"
    card_height = 6
    HEARTS = "hearts"
    DIAMONDS = "diamonds"
    CLUBS = "clubs"
    SPADES = "spades"

    #the constructor
    def __init__(self): 
        pass
        #these are instance variables
       
    #draws the title and waits for the user to enter    
    def draw_title(self):
        self.clear()
        print(
                f'    ▀█████████▄   ▄█          ▄████████  ▄████████    ▄█   ▄█▄      ▄█    ▄████████  ▄████████    ▄█   ▄█▄\n' 
                f'      ███    ███ ███         ███    ███ ███    ███   ███ ▄███▀     ███   ███    ███ ███    ███   ███ ▄███▀\n' 
                f'      ███    ███ ███         ███    ███ ███    █▀    ███▐██▀       ███   ███    ███ ███    █▀    ███▐██▀  \n' 
                f'     ▄███▄▄▄██▀  ███         ███    ███ ███         ▄█████▀        ███   ███    ███ ███         ▄█████▀   \n' 
                f'    ▀▀███▀▀▀██▄  ███       ▀███████████ ███        ▀▀█████▄        ███ ▀███████████ ███        ▀▀█████▄   \n' 
                f'      ███    ██▄ ███         ███    ███ ███    █▄    ███▐██▄       ███   ███    ███ ███    █▄    ███▐██▄  \n' 
                f'      ███    ███ ███▌    ▄   ███    ███ ███    ███   ███ ▀███▄     ███   ███    ███ ███    ███   ███ ▀███▄\n' 
                f'    ▄█████████▀  █████▄▄██   ███    █▀  ████████▀    ███   ▀█▀ █▄ ▄███   ███    █▀  ████████▀    ███   ▀█▀\n' 
                f'                ▀                                   ▀         ▀▀▀▀▀▀                            ▀         '
            )
        input("                                         Please Hit Enter to start")
      
    #draws the main menu    
    def draw_main_menu(self):
        print(
        f'      ╔══════════════════════════════════╗\n'
         '      ║            Main Menu             ║\n'
         '      ╠══════════════════════════════════╣\n'
         '      ║           Play (p/P)             ║\n'
         '      ║           Exit (e/E)             ║\n'
         '      ╚══════════════════════════════════╝'
        )
    
    #draw_board draws the entire game area. This includes the dealer, player
    # and their cards in between
    def draw_board(self,d_cards, d_total, p_cards, p_total, p_score):
        self.clear() #clear it so the board can be redrawn
        self.draw_dealer(d_total) #prints the dealer with his total card value
        self.draw_cards(d_cards, p_cards) #prints the cards, dealer then player
        self.draw_player(p_total, p_score) #prints the player with their card value and score
    
    #draws the dealer. takes in a card value total 
    def draw_dealer(self, total):
        print(
            f'\n    Dealer - total value: {total}\n'
             '    ════════════════════════════════════════════════════════════════════'            
            )
    
    #draws the player. Takes in the players card value and score
    def draw_player(self, total, score):
        print(
            f'    ════════════════════════════════════════════════════════════════════\n'     
            f'    Player - total value: {total} - Score: {score}\n'   
            f'    (h/H) to hit or (s/S) to stand or (e/E) to exit match:'   
            )    
    
    #draw_cards() will take in a list of the dealers and player's cards
    #using their values, it will print the cards to the screen.
    def draw_cards(self, d_cards, p_cards):
        #creates dealer and player cards in an array
        dealer = self.create_cards(d_cards)
        player = self.create_cards(p_cards) 
        #sends dealer and player arrays to be printed
        self.draw_card_row(dealer)
        self.draw_card_row(player)
    
    #create_cards() takes in an array of card values and then it will
    #send back an array of cards to print
    def create_cards(self, card_arr):
        the_cards = [] #cards to return
        for c in card_arr:
            #makes a new card and appends it to the_cards[]
            new_card = self.make_card(c[0],c[1])
            the_cards.append(new_card)
        return the_cards
    
    #draw_card_row() takes in a printable card array and then loops through
    #and prints each card so that they are to the right of each other
    def draw_card_row(self, card_arr):
        #each card has the same height, this runs through each height level
        for i in range(self.get_card_height()):
            #this will print each card[current height] next to each other
            for card in card_arr:
                print(card[i] + " ",end="")
            #new line for the card height
            print("")
    
    #make_card() will take in a card value in the format "xx"
    #where xx is a card value and a space if it is not 2 digits long
    #Then it will return an array of each piece of the card to be printed
    def make_card(self, cv, suit):
        #the bottom card value is the reverse of the top one, this makes the cards look correct
        bv = cv[::-1]
        #if it is 10, we dont reverse the bottom.
        if cv == "10":
            bv = cv     
        if suit == self.CLUBS:
            card = [    
                        f"    .------.",
                        f"    |{cv}.-. |",
                        f"    | :(): |",
                        f"    | ()() |",
                        f"    | '-'{bv}|",
                        f"    `------'",
            ]
        elif suit == self.DIAMONDS:
            card = [    
                        f"    .------.",
                        f"    |{cv}.-. |",
                        f"    | :/\: |",
                        f"    | :\/: |",
                        f"    | '-'{bv}|",
                        f"    `------'",
            ]
        elif suit == self.HEARTS:
            card = [    
                        f"    .------.",
                        f"    |{cv}.-. |",
                        f"    | (\/) |",
                        f"    | :\/: |",
                        f"    | '-'{bv}|",
                        f"    `------'",
            ]
        elif suit == self.SPADES:
            card = [    
                        f"    .------.",
                        f"    |{cv}.-. |",
                        f"    | :/\: |",
                        f"    | (__) |",
                        f"    | '-'{bv}|",
                        f"    `------'",
            ]
        else:
            card = [
                        f"    .------.",
                        f"    | .--. |",
                        f"    | :  : |",
                        f"    | :  : |",
                        f"    | '--' |",
                        f"    `------'",
            ]
        return card

    #mutator method to get card_height
    def get_card_height(self):
        return self.card_height
    
    #clear() will clear the screen. however, it will not remove anything from a previous run
    def clear(self):
        os.system('cls' if os.name=='nt' else 'clear') 
        
        
        
        
