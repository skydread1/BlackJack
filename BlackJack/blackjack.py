import random

# global variables
suits = ('clubs','diamonds','hearts','spades')
ranks = ('2','3','4','5','6','7','8','9','10','J','Q','K','Ace')
values = {'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':10,'Q':10,'K':10,'Ace':11}

#message ot display (ex, delaer Busts, player wins etc
message = ''

class Card():

	def __init__(self,value,suit):
		self.value = value
		self.suit = suit
		self.name = self.value + ' of ' + self.suit

	def __str__(self):
		return f"{self.name}"

class Deck():

	def __init__(self):
		self.cards = []
		self.new_deck()
		self.shuffle()

	def new_deck(self):
		for suit in suits:
			for value in ranks:
				card = Card(value,suit)
				self.cards.append(card)

	def __str__(self):
		description = "The deck is composed of:\n"
		for card in self.cards:
			description = description + str(card) + '\n'
		return description

	def shuffle(self):
		random.shuffle(self.cards)

	def deal(self):
		if len(self.cards) == 0:
			self.new_deck()
			self.shuffle()
		card = self.cards.pop()
		return card

class Stack():

	def __init__(self,name):
		self.name =name
		self.balance = 0
		self.bet = 0
		#if blackjack, winned win 3 times his bet instead of 2
		self.blackjack_bonus = 0
		self.push = 0

	def __str__(self):
		return f"Current stack of {self.name} is worth ${self.balance}"

	def debit(self):
		self.balance = self.balance - self.bet;
			

	def credit(self):
		self.balance = self.balance + self.bet*(2 + self.blackjack_bonus-self.push);


class Hand():

	def __init__(self,name,cards):
		self.name = name
		self.cards = cards
		self.value_hand = 0
		#determine value of the hands
		for card in cards:
			self.value_hand = self.value_hand + values[card.value]

	def __str__(self):
		description = "Hand of " + self.name + ":\n"
		for card in self.cards:
			description = description + str(card) + '\n'
		description = description + "Value of the hand: " + str(self.value_hand)+ "\n"
		return description	

	def hit(self,card):
		#add the card to the hand
		self.cards.append(card)
		#update the value of the hand
		#particular case for the Ace than can be 11 or 1
		if card.value == "Ace" and (self.value_hand + 11) > 21:
			self.value_hand = self.value_hand + 1
		else:
			self.value_hand = self.value_hand + values[card.value]
			print(f"{self.name} hit {str(card)}")


def check_BUST(hand):
	if hand.value_hand > 21:
		return True
	return False

def check_blackjack(hand):
	if hand.value_hand == 21:
		return True
	return False

def check_push(hand_dealer,hand_player):
	if hand_player.value_hand == hand_dealer.value_hand:
		return True
	return False

#the dealer has to draw until he reaches at least 17 or BUST, we return the value or BUST
def dealer_move(hand_dealer):
	while hand_dealer.value_hand < 17:
		hand_dealer.hit(deck.deal())
		if check_BUST(hand_dealer):
			return "BUST"

	return hand_dealer.value_hand

def set_stack(stack):
	while True:
		try:
			stack.balance = int(input("How big is your stack ? "))
		except TypeError:
			print("Please be sure to enter a number: ")
			continue
		else:
			break

def take_bet(stack):
	while True:
		try:
			stack.bet = int(input("Your bet: "))
		except TypeError:
			print("Please be sure to enter a number: ")
			continue
		else:
			if stack.bet > stack.balance:
				print(f"you only have ${stack.balance} in your stack...\nThus you can't bet ${stack.bet} ")
			else:
				stack.debit()
				break

def win_bet(hand_dealer,hand_player,stack):
	global message
	if check_blackjack(hand_player):
		stack.blackjack_bonus = 1
		message = message + "BLACKJACK\n"
		message = message + f"{hand_player.name} just won ${stack.bet*3}\n"
	elif check_push(hand_dealer,hand_player):
		stack.push = 1
		message = message + "PUSH\n"
		message = message + f"{hand_player.name} is refunded ${stack.bet}\n"
	else:
		message = message + f"{hand_player.name} just won ${stack.bet*2}\n"

	stack.credit()

def player_busts(hand_player,stack):
	global message
	message = message + f"{hand_player.name} BUSTS\n"
	message = message + f"{hand_player.name} just lost ${stack.bet}\n"
	stack.bet = 0

def dealer_busts(hand_dealer, hand_player,stack):
	global message
	message = message + "Dealer BUSTS\n"
	win_bet(hand_dealer,hand_player,stack)
	stack.bet = 0

def player_wins(hand_player,stack):
	global message
	message = message + f"{hand_player.name} beats the Dealer\n"
	win_bet(hand_dealer,hand_player,stack)
	stack.bet = 0

def dealer_wins(hand_player,stack):
	global message
	message = message + f"The Dealer beats {hand_player.name}\n"
	message = message + f"You just lost ${stack.bet}\n"
	stack.bet = 0

def push(hand_dealer, hand_player,stack):
	global message
	message = message + "PUSH"
	message = message + f"You are refunded ${stack.bet}\n"
	win_bet(hand_dealer,hand_player,stack)
	stack.bet = 0

def bankrupt(stack):
	print("It appears that you don't have any more chips")
	top_up = ''
	while top_up != 'y' and top_up != 'n':
		try:
			top_up = input("Wanna top up ? (y/n)")
		except:
			print("Please be sure to enter a y or n: ")
			continue
		else:
			break

	if top_up == 'y':
		set_stack(stack)

	return top_up

def play_again():
	another_one = ''
	while another_one != 'y' and another_one != 'n' and top_up != 'y':
		try:
			another_one = input("Do you wanna play another hand ? (y/n)")
		except:
			print("Please be sure to enter a y or n: ")
			continue
		else:
			break

	return another_one

def display_current_board(hand_dealer,hand_player, stack):
	global message
	print('\n\n\n')
	print('--------------------------')
	print(str(hand_dealer))
	print('--------------------------\n')
	print(message + '\n')
	print(str(stack))
	print(f"Current bet: ${stack.bet}")
	print('--------------------------\n')
	print(str(hand_player))
	print('--------------------------')
	print('\n\n\n')




#SET UP
#setup deck
deck = Deck()

#setup name and stack of player
player_name = input("what is your name ? ")
stack = Stack(player_name)
set_stack(stack)

#GAMBLING SESSION
replay_on = True
while replay_on:

	#HAND (in the sense of round) 
	#betting
	take_bet(stack)

	#initialize hands
	hand_dealer = Hand('Dealer', [deck.deal()])
	hand_player = Hand(player_name, [deck.deal(),deck.deal()])

	#display initial board
	display_current_board(hand_dealer,hand_player,stack)

	#hit or stay and result
	round_on = True
	while(round_on):
		#player decision
		decision = ''
		while decision != 'h' and decision != 's':
			decision = input("Hit or Stay (h/s)")

		if decision == 'h':
			#hit the player
			hand_player.hit(deck.deal())
			#check if BUST
			if check_BUST(hand_player):
				player_busts(hand_player,stack)
				round_on = False

		else:
			#the player stays so the dealer can now proceed
			dealer_result = dealer_move(hand_dealer)
			#the dealer BUST
			if dealer_result == "BUST":
				dealer_busts(hand_dealer, hand_player,stack)

			#player and dealer have same score
			elif check_push(hand_dealer,hand_player):
				push(hand_dealer, hand_player,stack)

			#the player beats the dealer (no one BUSTed)
			elif hand_player.value_hand > hand_dealer.value_hand:
				player_wins(hand_player,stack)

			#the dealer beats the player (no one BUSTed)
			else:
				dealer_wins(hand_player,stack)

			#reset values
			stack.bet = 0
			stack.blackjack_bonus = 0
			round_on = False

		#display updated board
		display_current_board(hand_dealer,hand_player,stack)

		#clear the board
		message = ''

	#ask the player if he wanna play another hand
	another_one = ''
	top_up = 'n'
	#the player has no more chips
	if stack.balance == 0:
		#ask him if he wanna top up
		top_up = bankrupt(stack)
		if top_up == 'n':
			replay_on = False
	else:		
		another_one = play_again()
		if another_one == 'n':
			replay_on = False

print(f"Thank you {player_name} for playing with us")
