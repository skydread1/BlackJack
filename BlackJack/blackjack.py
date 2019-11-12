import random

# global variables
suits = ('clubs','diamonds','hearts','spades')
ranks = ('2','3','4','5','6','7','8','9','10','J','Q','K','Ace')
values = {'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':10,'Q':10,'K':10,'Ace':11}

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

	def __str__(self):
		return f"Current stack of {self.name} is worth ${self.balance}"

	def debit(self):
		self.balance = self.balance - self.bet;
			

	def credit(self):
		self.balance = self.balance + self.bet*(2 + self.blackjack_bonus);


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


def check_burst(hand):
	if hand.value_hand > 21:
		return True
	return False

def check_blackjack(hand):
	if hand.value_hand == 21:
		return True
	return False

#the dealer has to draw until he reaches at least 17 or Burst, we return the value or burst
def dealer_move(hand_dealer):
	while hand_dealer.value_hand < 17:
		hand_dealer.hit(deck.deal())
		if check_burst(hand_dealer):
			return "burst"

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


def display_current_board(hand_dealer,hand_player, stack):
	print('\n\n\n')
	print('--------------------------')
	print(str(hand_dealer))
	print('--------------------------\n')
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
			#check if burst
			if check_burst(hand_player):
				print(f"{hand_player.name} BURST")
				print(f"{hand_player.name} just lost ${stack.bet}")
				stack.bet = 0
				round_on = False

		else:
			#the player stays so the dealer can now proceed
			dealer_result = dealer_move(hand_dealer)
			#the dealer burst
			if dealer_result == "burst":
				print("Dealer BURST")
				if check_blackjack(hand_player):
					stack.blackjack_bonus = 1
					stack.credit()
					print("BLACKJACK")
					print(f"{hand_player.name} just won ${stack.bet*3}")
				else:
					stack.credit() 
					print(f"{hand_player.name} just won ${stack.bet*2}")
					stack.bet = 0
			#the player beats the dealer (no one bursted)
			elif hand_player.value_hand > hand_dealer.value_hand:
				print(f"{hand_player.name} beates the Dealer")
				#test if blackjack
				if check_blackjack(hand_player):
					stack.blackjack_bonus = 1
					stack.credit()
					print("BLACKJACK")
					print(f"{hand_player.name} just won ${stack.bet*3}")
				else:
					stack.credit() 
					print(f"{hand_player.name} just won ${stack.bet*2}")
					stack.bet = 0

			#the dealer beats the player (no one bursted)
			else:
				print(f"The Dealer beats {hand_player.name}")
				print(f"You just lost ${stack.bet}")

			#clear the board
			stack.bet = 0
			stack.blackjack_bonus = 0
			round_on = False

		#display updated board
		display_current_board(hand_dealer,hand_player,stack)

	#ask the player if he wanna play another hand
	another_one = ''
	while another_one != 'y' and another_one != 'n':
		another_one = input("Do you wanna play another hand ? (y/n)")
	if another_one == 'n':
		break
print(f"Thank you {player_name} for playing with us")
