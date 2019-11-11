class Card():

	def __init__(self,value,suit):
		self.value = value
		self.suit = suit
		self.name = self.value + ' of ' + self.suit

	def __str__(self):
		return f"{self.name}"

class Deck():

	# class object attribute
	suitList = ['clubs','diamonds','hearts','spades']
	valueList = ['2','3','4','5','6','7','8','9','10','J','Q','K','Ace']

	def __init__(self):
		self.cards = []
		for suit in Deck.suitList:
			for value in Deck.valueList:
				card = Card(value,suit)
				self.cards.append(card)

	def __str__(self):
		description = "The deck is composed of:\n"
		for card in self.cards:
			description = description + str(card) + '\n'
		return description


class Stack():

	def __init__(self,balance):
		self.balance = balance

	def __str__(self):
		return f"Your current stack is worth ${self.balance}"

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

	def __str__(self):
		description = "Hand of " + self.name + ":\n"
		for card in self.cards:
			description = description + str(card) + '\n'
		return description	

	def hit(self,card):
		self.cards.append(card)
		print(f"you hit {str(card)}")


#test_card = Card('AS','clubs')
#print(str(test_card))
test_deck = Deck()
#print(str(test_deck))
stack = Stack(100)
# print(str(stack))
# stack.debit(50)
# print(str(stack))
# stack.credit(100)
# print(str(stack))
# stack.debit(1000)
# print(str(stack))
# stack.debit(3)
# print(str(stack))
hand_player = Hand('lolo', [Card('AS','clubs'),Card('3','diamonds')])
print(str(hand_player))
hand_player.hit(Card('5','clubs'))
print(str(hand_player))
