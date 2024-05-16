################################################################################
# play.py - This script handles the gameplay of blackjack. it will handle
# keeping track of cards and rules. It will push the data to gameboard.py to
# display it
#
# author: Brian Bessler
#
################################################################################

#import json
import random  
import time
from gameboard import GameBoard
import copy #copies array

class Play(object):
    g_board = GameBoard() #handles drawing the game board
    
    #creates a constant card deck the will not be changed
    #each "card" is broken down into ("card_display", suit, card_value_1, card_value_2)
    #the very last card is a blank card that is used only for the dealer when one is face down
    CARD_DECK = [
        ("2 ", g_board.HEARTS, 2, 2), ("2 ", g_board.CLUBS, 2, 2), ("2 ", g_board.SPADES, 2, 2), ("2 ", g_board.DIAMONDS, 2, 2),
        ("3 ", g_board.HEARTS, 3, 3), ("3 ", g_board.CLUBS, 3, 3), ("3 ", g_board.SPADES, 3, 3), ("3 ", g_board.DIAMONDS, 3, 3),
        ("4 ", g_board.HEARTS, 4, 4), ("4 ", g_board.CLUBS, 4, 4), ("4 ", g_board.SPADES, 4, 4), ("4 ", g_board.DIAMONDS, 4, 4),
        ("5 ", g_board.HEARTS, 5, 5), ("5 ", g_board.CLUBS, 5, 5), ("5 ", g_board.SPADES, 5, 5), ("5 ", g_board.DIAMONDS, 5, 5),
        ("6 ", g_board.HEARTS, 6, 6), ("6 ", g_board.CLUBS, 6, 6), ("6 ", g_board.SPADES, 6, 6), ("6 ", g_board.DIAMONDS, 6, 6),
        ("7 ", g_board.HEARTS, 7, 7), ("7 ", g_board.CLUBS, 7, 7), ("7 ", g_board.SPADES, 7, 7), ("7 ", g_board.DIAMONDS, 7, 7),
        ("8 ", g_board.HEARTS, 8, 8), ("8 ", g_board.CLUBS, 8, 8), ("8 ", g_board.SPADES, 8, 8), ("8 ", g_board.DIAMONDS, 8, 8),
        ("9 ", g_board.HEARTS, 9, 9), ("9 ", g_board.CLUBS, 9, 9), ("9 ", g_board.SPADES, 9, 9), ("9 ", g_board.DIAMONDS, 9, 9),
        ("10", g_board.HEARTS, 10,10), ("10", g_board.CLUBS, 10,10), ("10", g_board.SPADES, 10,10), ("10", g_board.DIAMONDS, 10,10),
        ("J ", g_board.HEARTS, 10,10), ("J ", g_board.CLUBS, 10,10), ("J ", g_board.SPADES, 10,10), ("J ", g_board.DIAMONDS, 10,10),
        ("Q ", g_board.HEARTS, 10,10), ("Q ", g_board.CLUBS, 10,10), ("Q ", g_board.SPADES, 10,10), ("Q ", g_board.DIAMONDS, 10,10),
        ("K ", g_board.HEARTS, 10,10), ("K ", g_board.CLUBS, 10,10), ("K ", g_board.SPADES, 10,10), ("K ", g_board.DIAMONDS, 10,10),
        ("A ", g_board.HEARTS, 11, 1), ("A ", g_board.CLUBS, 11, 1), ("A ", g_board.SPADES, 11, 1), ("A ", g_board.DIAMONDS, 11, 1),
        ("  ", "  ", 0, 0)
    ]
    current_deck = [] #creates the current deck. every card dealt will be removed so it can't be dealt again
    dealer_hand = [] #dealer's hand. starts off with a blank card in it, inserted after shuffle
    is_card_up = False #states if the dealer's first card has been flipped yet
    player_hand = [] #players hand
    player_score = 10000 #player score. used for betting
    hit_words = ["h", "H", "hit", "Hit", "HIT"] #words you could type if you want to "hit"
    stand_words = ["s", "S", "stand", "Stand", "STAND"] #words you could type if you want to "stand"
    exit_words = ["e", "E", "exit", "Exit", "EXIT"] #words you could type if you want to "exit"
    to_hit = False #if the player chooses to hit
    to_stand = False #if the player chooses to stand
    user_input = "" #user input
    game_over = False #if the game is over
    bad_input = False #if the user gave bad input
    bust = False #if the player busted
    win_condition = 0 #0 if player won, 1 if dealer won, 2 if tie
    natrual_win = False #if the player, dealer or both got a black jack at deal
    slow = 0.75 #used to slow the dealers turn so it is visible
    
    #the constructor
    def __init__(self): 
        pass

    #main method that will run the game
    def main(self):
        while not self.game_over:
            self.shuffle_deck() #must happen every time to initialize the game
            self.deal_cards() #deals the cards
            self.send_board() #draws the boards
            time.sleep(self.slow)
            d_card_value = self.get_cards_value(self.get_dealer_hand()[1:]) #checks if dealer has blackjack
            p_card_value = self.get_cards_value(self.get_player_hand()) #checks if player has blakjack
            #if they both have blackjack, its a tie and a new game is started
            if (p_card_value == (21,11) or p_card_value == (11,21)) and (d_card_value == (21,11) or d_card_value == (11,21)):
                self.natural_win_reset()
                print("    You both got a black jack! It is a tie")
                input("    hit enter to start a new game")      
            #if only the player has blackjack they win, and a new game is started    
            elif p_card_value == (21,11) or p_card_value == (11,21):
                self.natural_win_reset()
                print("    you got a black jack! you won!")
                input("    hit enter to start a new game")  
            #if only the dealer has blackjack, the player loses and a new game is started
            elif d_card_value == (21,11) or d_card_value == (11,21):
                self.natural_win_reset()
                print("    The dealer got a black jack! you lost!")
                input("    hit enter to start a new game")  
            
            #if there is no natural win or bad input, this will run  
            while not self.bad_input and not self.natural_win:
                self.send_board() #shows the board, with the dealer's first card down
                self.user_input = input("    ")
                #checks if the player wants to hit, stand or exit
                self.to_hit = self.user_input_check(self.hit_words, self.user_input)
                self.to_stand = self.user_input_check(self.stand_words, self.user_input)
                self.game_over = self.user_input_check(self.exit_words, self.user_input)
                
                if self.game_over: #when player exits
                    input("    Hit enter to exit match")
                    break
                elif self.to_hit: #When player hits
                    self.player_hit() #adds a card
                    card_value = self.get_cards_value(self.get_player_hand())
                    #if over 21, the player busts and new game is started
                    if card_value[0] > 21 and card_value[1] > 21:
                        self.bust = True
                        print(f'    your total is {card_value} that means you busted!')
                        input("    hit enter for the new game to start")
                        break
                elif self.to_stand: #when player stands it goes to the dealers turn
                    #saves the results of the dealer's turn
                    win_condition, d_bust = self.dealers_turn()
                    if win_condition == 0 and d_bust: #if player won, but dealer busted
                        print("    The dealer busted so you won!")
                        input("    hit enter to play again")
                        break
                    elif win_condition == 0: #if player won, but dealer didn't bust
                        print("    you scored higher than the dealer, so you won!")
                        input("    hit enter to play again")
                        break
                    elif win_condition == 1: #if dealer won
                        print("    The dealer had more points so you lost!")
                        input("    hit enter to play again")
                        break
                    elif win_condition == 2: #if they tied
                        print("    you both tied!")
                        input("    hit enter to play again")
                        break
                        
                elif not self.to_hit and not self.to_stand: #if the input is wrong, this helps the user try again
                    input("    Input not understood. Press enter to try again")
                    self.g_board.clear()
             
    #dealer's turn happens after the player, the dealer must hit if the total is < 17
    #after the dealer is done hitting, this will return the function check_who_won()
    #if the result is a 0, the player won, 1 the dealer won, 2 it was a draw
    def dealers_turn(self):
        #flip the first card up
        self.card_is_up()
        self.g_board.clear()
        self.send_board()
        to_hit = True #sees if dealer still needs to hit
        dealer_bust = False #if dealer busts, its true
        p_card_value = self.get_cards_value(self.get_player_hand())
        #check if dealer should hit
        while to_hit:
            #find value of dealer's hand, minus the frist blank card
            card_value = self.get_cards_value(self.get_dealer_hand()[1:])
            if card_value[0] > p_card_value[1] or card_value[0] > p_card_value[0] or card_value[1] > p_card_value[1] or card_value[1] > p_card_value[0]:
                time.sleep(self.slow)
                to_hit = False
            if card_value[0] < 17 or card_value[1] < 17: #if 16 or lower, dealer MUST hit
                time.sleep(self.slow)
                self.dealer_hit()
                self.g_board.clear()
                self.send_board()
            #if greater than 21, dealer busts
            elif (card_value[0] > 21 and not card_value[1] < 21) or (card_value[1] > 21 and not card_value[0] < 21): 
                time.sleep(self.slow) 
                dealer_bust = True
                self.g_board.clear()
                self.send_board()
                to_hit = False
            else: #otherwise, dealer can no longer hit
                time.sleep(self.slow)
                to_hit = False
            time.sleep(self.slow/2)
            
        return self.check_who_won(dealer_bust) #returns the result of who won
    
    #used to initalize the game further if one or both got a black on the first deal
    def natural_win_reset(self):
        time.sleep(self.slow)
        self.card_is_up()
        self.g_board.clear()
        self.send_board()
        time.sleep(self.slow)
        self.natural_win = True
    
    #adds a card from the deck to the player's hand
    def player_hit(self):
        self.add_card_player(self.random_card_index())
        self.g_board.clear()
        self.send_board()
    
    #adds a card from the deck to the dealer's hand    
    def dealer_hit(self):
        self.add_card_dealer(self.random_card_index())
        self.g_board.clear()
        self.send_board()
    
    #return 0 if player won, 1 if dealer won, 2 if it was a tie
    #will always return if the dealer busted or not
    def check_who_won(self, d_bust):
        #if dealer busted then player won
        if d_bust: #if dealer busted, player won
            return 0, d_bust
        #get card values for checking who won
        d_val = self.get_cards_value(self.get_dealer_hand()[1:])
        p_val = self.get_cards_value(self.get_player_hand())
        d_val = self.make_score_even(d_val)
        p_val = self.make_score_even(p_val)  
        if d_val == p_val:
            return 2
        elif d_val > p_val: #if dealer has more points, they won
            return 1, d_bust
        elif p_val > d_val: #if player has more points, they won
            return 0, d_bust
        else: #return something went wrong, error
            return 3, d_bust
    
    #this will make the scores that are different from aces even. works best when one 
    #ace value busts, but the other doesnt
    def make_score_even(self, val):
        even_val = val
        if val[0] != val[1]:
            if val[0] > 21 and val[0] > val[1]:
                even_val = (val[1], val[1])
            elif val[1] > 21 and val[1] > val[0]:
                even_val = (val[0], val[0])
            elif val[1] > val[0]:
                even_val = (val[1], val[1])
            elif val[0] > val[1]:
                even_val = (val[0], val[0])
        return even_val
    
    #resets the deck, the player and dealer hands. the dealer is given a blank card in slot one only
    # used for displaying
    def shuffle_deck(self):
        self.current_deck = copy.copy(self.CARD_DECK) #copys the cards array into a new deck
        self.dealer_hand.clear() #clears dealer's hand
        self.add_card_dealer(len(self.get_current_deck())-1) #adds the blank card to the dealer
        self.card_is_down() #the dealer's first card is face down at the beginning
        self.player_hand.clear() #clears the player's hand
        self.natural_win = False
        
    #picks four random cards from the deck. dealer, player, dealer, then player    
    def deal_cards(self):
        self.add_card_dealer(self.random_card_index())
        self.add_card_player(self.random_card_index())
        self.add_card_dealer(self.random_card_index())
        self.add_card_player(self.random_card_index())
    
    #finds a random number from 0 to the current_deck length
    #it will return the card at that index
    def random_card_index(self):
        rand_card_index = random.randrange(0, len(self.get_current_deck()))
        return rand_card_index
    
    def get_current_deck(self):
        return self.current_deck
    
    #if the first card is down, send only the dealers first two cards
    #if the first card is up, send all the cards, except the first blank one
    def get_dealer_hand(self):
        return self.dealer_hand      

    #returns player's hand
    def get_player_hand(self):
        return self.player_hand
    
    #returns player's score
    def get_player_score(self):
        return self.player_score
    
    #can set the player's score
    def set_player_score(self,score):
        self.player_score = score
    
    #can add to the player's score (send a negative number to lower it)
    def add_player_score(self,score):
        new_score = self.get_player_score() + score
        self.set_player_score(new_score)
    
    #pops the card from the deck and ads it to the dealers hand
    def add_card_dealer(self, card_index):
        the_card = self.get_current_deck().pop(card_index)
        self.get_dealer_hand().append(the_card)
    
    #pops the card from the deck and ads it to the players hand
    def add_card_player(self, card_index):
        the_card = self.get_current_deck().pop(card_index)
        self.get_player_hand().append(the_card)
    
    #returns True if the dealer's first card is down    
    def get_is_card_up(self):
        return self.is_card_up
     
    #sets the card to down   
    def card_is_down(self):
        self.is_card_up = False
    
    #sets the card to up
    def card_is_up(self):
        self.is_card_up = True
    
    #sends the current set of cards to the board to be drawn    
    def send_board(self):
        if self.get_is_card_up():
            dc = self.get_dealer_hand()[1:] #dealer's cards without the blank card
        else:
            dc = self.get_dealer_hand()[0:2] # dealer's cards with one flipped down
        dt = self.get_cards_value(dc) #dealer total
        pc = self.get_player_hand() #player cards
        pt = self.get_cards_value(pc) #player total
        ps = self.get_player_score() #player score
        self.g_board.draw_board(dc,dt,pc,pt,ps) #draw_board will draw the results
    
    #returns the total value of the cards sent. if there is at least
    #one ace, then it will return both values
    def get_cards_value(self, cards):
        value_one = 0
        value_two = 0
        has_ace = 0
        for c in cards:
            #if it is an ace, just add the c[3] component to each value
            if c[0] == "A ":
                has_ace += 1 
                value_one += c[3]
                value_two += c[3]
            #if not an ace, then add the values like normal
            else:
                value_one += c[2]
                value_two += c[3]
            
        if has_ace > 0:
            #we add 10 (not 11) to value one, because it already added a 1
            #value two was calculated normally
            return (value_one + 10, value_two)
        else:
            return (value_one, value_two)
    
    #checks the user input against the words sent in the array
    #if any are true, it will return true, otherwise, false
    def user_input_check(self, test_arr, input):
        for test in test_arr:
            if test == input:
                return True
        return False
