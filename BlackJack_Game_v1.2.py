import colorama #for colored text
import random #to shuffle the cards
import time
import os
import sys
import getpass
#'blackjack' is the password
from colorama import Fore, Style, Back

password = getpass.getpass(prompt = "Enter the password:")

if password == 'blackjack':
    print(Back.WHITE + Fore.GREEN + Style.BRIGHT + 'Password Accepted' + Style.RESET_ALL + "\n")
else:
    print(Back.WHITE + Fore.RED + Style.BRIGHT + 'Incorrect Password' + Style.RESET_ALL + "\n")
    sys.exit()

print('\n' + Back.WHITE + Fore.BLUE + Style.BRIGHT + 'THIS GAME HAS BEEN DEVELOPED BY ABHINAV GUPTA' + Style.RESET_ALL + "\n")
time.sleep(1) #used to delay
print(Back.WHITE + Fore.RED + Style.BRIGHT + 'NOTE: IF THE DEALER/PLAYER GETS AN ACE CARD IN THE FIRST SET, IT WILL BE TAKEN AS 11' + Style.RESET_ALL + '\n\n\n')
time.sleep(1)

while True:

    suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
    ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
    values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
             'Queen':10, 'King':10, 'Ace':11}
    check = 0
    
    playing = True
    
    class Card:
        
        def __init__(self,suit,rank):
            self.suit = suit
            self.rank = rank
        
        def __str__(self):
            return self.rank + " of " + self.suit
    
    class Deck():
        
        def __init__(self):
            self.deck = []  # start with an empty list
            for suit in suits:
                for rank in ranks:
                    self.deck.append(str(Card(suit,rank)))
                    
                    
        
        def __str__(self):
            deck_comp = ''
            for card in self.deck:
                deck_comp += '\n' + card #or card.__str__() BUT WHY??!! To change from main type to str type??
            return 'The Deck Has: \n' + deck_comp
        
        def shuffle(self):
            random.shuffle(self.deck) #shuffling the contents in the list
            
        def deal(self):
            single_card = self.deck.pop()
            print('\n')
            return single_card
    
    class Hand:
        def __init__(self):
            self.cards = []  # start with an empty list as we did in the Deck class
            self.value = 0   # start with zero value
            #self.aces = 0    # add an attribute to keep track of aces
            self.flag = 0
            
        def add_card(self,card):
            #self.acecheck = False
            card = card.title()
            if (card.split())[0] == 'Ace':
                
                #self.value += Hand.adjust_for_ace(self)
                values['Ace'] = Hand.adjust_for_ace(self)
                #self.acecheck = True
            self.cards.append(card)
            #if self.acecheck == False:
            self.value += values[(card.split())[0]]

        def add_card_dealer(self,card):
            self.acecheck = False
            card = card.title()
            if (card.split())[0] == 'Ace':
                if self.value + 11 > 21:
                    self.value += 1
                    print(Fore.CYAN + 'Dealer has taken Ace as 1' + Fore.RESET)
                else:
                    self.value += 11
                    print(Fore.CYAN + 'Dealer has taken Ace as 11' + Fore.RESET)
                self.acecheck = True
            self.cards.append(card)
            if self.acecheck == False:
                self.value += values[(card.split())[0]]
            
        def add_card_first_set(self,card):
            card = card.title()
            self.cards.append(card)
            if card[:3] == 'Ace':
                self.value += 11
            else:
                self.value += values[(card.split())[0]]
            
        def adjust_for_ace(self):
            while True:
                try:            
                    self.flag = int(input('Do you wish to take the Ace as 11 or 1?\n'))
                except:
                    print(Style.BRIGHT + Fore.RED + 'Invalid Input!' + Style.RESET_ALL)
                else:
                    if self.flag != 1 and self.flag != 11:
                        print(Style.BRIGHT + Fore.RED + 'Enter either 1 or 11!' + Style.RESET_ALL)
                    else:
                        print(Style.BRIGHT + Fore.GREEN + 'Ace has now been taken as {}'.format(self.flag) + Style.RESET_ALL)
                       
                        break;
            return self.flag
        
    
    class Chips:
        
        def __init__(self,total = 100):
            self.total = total  # This can be set to a default value or supplied by a user input
            self.bet = 0
            
        def win_bet(self):
            self.total += self.bet
        
        def lose_bet(self):
            self.total -= self.bet
    
    def take_bet(chips):
        
        while True:
            try:
                chips.bet = int(input('\nEnter the number of chips you would like to bet:\n'))
            except:
                print(Style.BRIGHT + Fore.RED + 'Invalid Input!' + Style.RESET_ALL)
            else:
                if chips.bet > chips.total and chips.bet > 0:
                    print(Style.BRIGHT + Fore.RED + 'Your bet exceeds the total number of chips!' + Style.RESET_ALL)
                elif chips.bet < 0:
                    print(Style.BRIGHT + Fore.RED + 'Your bet is invalid!' + Style.RESET_ALL)
                elif chips.bet == 0:
                    print(Style.BRIGHT + Fore.RED + 'Your bet is invalid!' + Style.RESET_ALL)
                else:
                    print(Style.BRIGHT + Fore.GREEN + 'Your bet has been accepted\n' + Style.RESET_ALL)
                    break
    
    def hit(deck,hand):
        c = deck.deal()
        time.sleep(1)
        print('Your card is: ' + Fore.MAGENTA + c + Fore.RESET)
        hand.add_card(c)
        print('Your new total value: ' + Fore.MAGENTA + str(hand.value) + Fore.RESET)
        
    def dealer_hit(deck,hand):
        c = deck.deal()
        print("The dealer's card is: " + Fore.CYAN + c + Fore.RESET)
        hand.add_card_dealer(c)
        print("The dealer's new total value: " + Fore.CYAN + str(hand.value) + Fore.RESET)

    
    def hit_or_stand(deck,hand):
        global playing  # to control an upcoming while loop
        while True:
            ans = input('Do you wish to hit or stand?\n')
            ans = ans.lower()
            if ans == 'hit':
                hit(deck,hand)
                if hand.value > 21 or hand.value == 21:
                    playing = False
                    break
            elif ans == 'stand':
                playing = False
                break
            else:
                print(Style.BRIGHT + Fore.RED + 'Invalid Input! Enter hit or stand.' + Style.RESET_ALL)
    
    def show_some(player,dealer):
        
        print(Fore.MAGENTA + "\nPLAYER'S HAND\n")
        for ca in player.cards:         
            print(ca)           
        print("Player's Total Value: {}".format(player.value))
        print('\n')       
        print(Fore.CYAN + "DEALER'S HAND\n")       
        print(dealer.cards[0] + Fore.RESET)
     
    #def show_some_first_set(player,dealer):
        #print(Fore.MAGENTA + "\nPLAYER'S HAND\n")
        #for ca in player.cards:
            #print(ca)
        #print('\n')

        #print(Fore.CYAN+ "DEALER'S HAND\n")
        #print(dealer.cards[0] + Fore.RESET)
        
    def show_all(player,dealer):
        
        print(Fore.MAGENTA + "\nPLAYER'S HAND\n")
        for ca in player.cards:         
            print(ca)        
        print(f"Player's Total Value: {player.value}\n")
        
        print(Fore.CYAN + "DEALER'S HAND\n")
        for ca in dealer.cards:         
            print (ca)        
        print(f"Dealer's Total Value: {dealer.value}\n" + Fore.RESET)
            
    def player_busts(player,dealer,chips):
        print(Style.BRIGHT + Fore.GREEN + '\nPlayer is BUSTED!' + Style.RESET_ALL)
        chips.lose_bet()
    
    def player_wins(player,dealer,chips):
        print(Style.BRIGHT + Fore.GREEN + '\nPlayer has WON!' + Style.RESET_ALL)
        chips.win_bet()
        
    def dealer_busts(player,dealer,chips):
        print(Style.BRIGHT + Fore.GREEN + '\nDealer is BUSTED!' + Style.RESET_ALL)
        
        
    def dealer_wins(player,dealer,chips):
        print(Style.BRIGHT + Fore.GREEN + '\nDealer has WON!' + Style.RESET_ALL)
        
        
    def push(player,dealer):
        print(Style.BRIGHT + Fore.GREEN + '\nDealer and Player tie!' + Style.RESET_ALL + '\n')


    def restart():
        while True:
            a = input('Do you wish to play again? yes/no\n')
            a = a.lower()
            if a == 'yes':
                print('\n')
                return 0
            elif a == 'no':
                return 1
            else:
                print(Style.BRIGHT + Fore.RED + 'Invalid Input!' + Style.RESET_ALL)

    
    # Print an opening statement
    print(Back.WHITE + Style.BRIGHT + Fore.BLUE + 'WELCOME TO BLACKJACK VERSION 1.2 ' + '♠️ ♥️ ♣️ ♦️ ' + Style.RESET_ALL + '\n')
    # Create & shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()
    
    while True:
        try:
            total_chips = int(input('Enter the total number of chips:\n'))
        except:
            print(Style.BRIGHT + Fore.RED + 'Invalid Input!' + Style.RESET_ALL)
        else:
            if total_chips <= 0:
                print(Style.BRIGHT + Fore.RED + 'Invalid Input!' + Style.RESET_ALL)
            else:
                break

    player_chips = Chips(total_chips)
    take_bet(player_chips)
    
    player_hand = Hand()
    player_hand.add_card_first_set(deck.deal())
    player_hand.add_card_first_set(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card_first_set(deck.deal())
    dealer_hand.add_card_first_set(deck.deal())
    show_some(player_hand,dealer_hand)

    if player_hand.value == 21:
        time.sleep(2)
        print('\n' + Back.WHITE + Style.BRIGHT + Fore.BLACK + 'BLACK' + Style.RESET_ALL + Back.WHITE + Style.BRIGHT + Fore.RED + 'JACK' + Style.RESET_ALL)
        player_wins(player_hand,dealer_hand,player_chips)
        check = restart()
        if check == 1:
            break
        else:
            continue
    
    print(Fore.MAGENTA + "\nPLAYER'S TURN\n" + Fore.RESET)
    while playing:  # recall this variable from our hit_or_stand function        
        # Prompt for Player to Hit or Stand
        hit_or_stand(deck,player_hand)
        time.sleep(1.5)
        # Show cards (but keep one dealer card hidden)
        show_some(player_hand,dealer_hand)
        time.sleep(7)
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            player_busts(player_hand,dealer_hand,player_chips)
            break
            

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    
    if player_hand.value<21:
        print(Fore.CYAN + "\nDEALER'S TURN\n" + Fore.RESET)
        # Show all cards
        time.sleep(3)
        print('SETS OF CARDS BEFORE DEALER MAY HIT:\n')
        show_all(player_hand,dealer_hand)
        time.sleep(10)
        while True:
            if dealer_hand.value < 17:
                dealer_hit(deck,dealer_hand)
                time.sleep(5)
            else:
                break
        print('\nFINAL SETS OF CARDS:\n')
        show_all(player_hand,dealer_hand)
        time.sleep(10)
                
    # Run different winning scenarios
    if player_hand.value == 21:
        print('\n' + Back.WHITE + Style.BRIGHT + Fore.BLACK + 'BLACK' + Style.RESET_ALL + Back.WHITE + Style.BRIGHT + Fore.RED + 'JACK' + Style.RESET_ALL)
        player_wins(player_hand,dealer_hand,player_chips)
        print()
    elif dealer_hand.value > 21:
        dealer_busts(player_hand,dealer_hand,player_chips)
        player_wins(player_hand,dealer_hand,player_chips)
        print()
    elif player_hand.value > dealer_hand.value and player_hand.value <= 21:
        player_wins(player_hand,dealer_hand,player_chips)
        print()

    elif player_hand.value < dealer_hand.value:
        player_busts(player_hand,dealer_hand,player_chips)
        dealer_wins(player_hand,dealer_hand,player_chips)
        print()

    elif player_hand.value ==  dealer_hand.value:
        push(player_hand,dealer_hand)
            
    
    # Inform Player of their chips total 
    print(f'The total number of chips that you have: {player_chips.total}')
    
    # Ask to play again
    time.sleep(1)
    check = restart()
    if check == 1:
        break
    os.system('clear') #used to clear the previous output
os.system('clear')
