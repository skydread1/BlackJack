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

	def remove_card(self,card):
		self.cards.remove(card)

class Stack():

	def __init__(self,name,balance):
		self.name =name
		self.balance = balance

	def __str__(self):
		return f"Current stack of {self.name} is worth ${self.balance}"

	def debit(self, amount):
		if self.balance < amount:
			print(f"you only have ${self.balance} in your stack...\nThus you can't bet ${amount} ")
		else:
			self.balance = self.balance - amount;
			print(f"you bet ${amount}")

	def credit(self, amount):
		self.balance = self.balance + amount;
		print(f"you won ${amount}")


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
		return description	

	def hit(self,card):
		#add the card to the hand
		self.cards.append(card)
		#update the value of the hand
		self.value_hand = self.value_hand + values[card.value]
		print(f"{self.name} hit {str(card)}")

def random_card(deck):

	#check if the deck is empty
	if len(deck.cards) == 0:
		#we take a new deck
		deck.new_deck()

	#we pick randomly a card in the deck
	random_card = random.choice(deck.cards)

	#we remove this car from the deck
	deck.remove_card(random_card)

	#we return the card
	return random_card

def check_burst(hand):
	if hand.value_hand > 21:
		print(f"{hand.name} BURST !")
		return True
	return False

def check_blackjack(hand):
	if hand.value_hand == 21:
		print(f"{hand.name} has BLACKJACK !")
		return True
	return False

#the dealer has to draw until he reaches at least 17 or Burst, we return the value or burst
def dealer_move(hand_dealer):
	while hand_dealer.value_hand < 17:
		hand_dealer.hit(random_card(deck))
		if check_burst(hand_dealer):
			return "burst"

	return hand_dealer.value_hand

def display_current_board(hand_dealer,hand_player, stack, current_bet):
	print('\n\n\n')
	print('--------------------------')
	print(str(hand_dealer))
	print('--------------------------\n')
	print(str(stack))
	print(f"Current bet: ${current_bet}")
	print('--------------------------\n')
	print(str(hand_player))
	print('--------------------------')
	print('\n\n\n')




#SET UP
#setup deck
deck = Deck()

#setup name and stack of player
player_name = input("what is your name ? ")

while True:
	try:
		player_initial_stack = int(input("How big is your stack ? "))
	except TypeError:
		print("Please be sure to enter a number: ")
		continue
	else:
		stack = Stack(player_name,player_initial_stack)
		break
#GAMBLING SESSION
replay_on = True
while replay_on:

	#HAND (in the sense of round) 
	#betting
	while True:
		try:
			bet = int(input("Your bet: "))
			if bet > stack.balance:
				print(f"you only have ${stack.balance} in your stack...\nThus you can't bet ${bet} ")
				continue
		except TypeError:
			print("Please be sure to enter a number: ")
			continue
		else:
			stack.debit(bet)
			break

	#initialize hands
	hand_dealer = Hand('Dealer', [random_card(deck)])
	hand_player = Hand(player_name, [random_card(deck),random_card(deck)])

	#display initial board
	display_current_board(hand_dealer,hand_player,stack,bet)

	#hit or stay and result
	round_on = True
	while(round_on):
		#player decision
		decision = ''
		while decision != 'h' and decision != 's':
			decision = input("Hit or Stay (h/s)")

		if decision == 'h':
			#hit the player
			hand_player.hit(random_card(deck))
			#check if burst
			if check_burst(hand_player):
				print(f"You just lost ${bet}")
				bet = 0
				round_on = False

		else:
			#the player stays so the dealer can now proceed
			dealer_result = dealer_move(hand_dealer)
			#the dealer burst or the player is closer form 21 than the dealer
			if dealer_result == "burst":
				stack.credit(bet*2) 
				bet = 0
			elif hand_player.value_hand > hand_dealer.value_hand:
				#test if blackjack
				if check_blackjack:
					stack.credit(bet*3)
				else:
					stack.credit(bet*2) 
					print("You beat the Dealer")
					bet = 0
			else:
				print(f"The Dealer wins")
				print(f"You just lost ${bet}")
			round_on = False
		#display updated board
		display_current_board(hand_dealer,hand_player,stack,bet)

	#ask the player if he wanna play another hand
	another_one = ''
	while another_one != 'y' and another_one != 'n':
		another_one = input("Do you wanna play another hand ? (y/n)")
	if another_one == 'n':
		break
print(f"Thank you {player_name} for playing with us")
