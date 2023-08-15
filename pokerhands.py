from collections import namedtuple
import random, time

CardTuple = namedtuple('Card', ['value', 'suit'])

cardvalues = [2, 3, 4, 5, 6, 7, 8, 9, 10,
  11, # Jack
  12, # Queen
  13, # King
  14] # Ace

cardsuits = ['Clubs', 'Diamonds', 'Hearts', 'Spades']

class Card:
  def __init__(self):
    self.data = CardTuple(value=random.choice(cardvalues), suit=random.choice(cardsuits))

  def info(self, card):
    card = card.data
    if card.value > 10:
      if card.value == 11:
        return f"Jack of {card.suit}"
      elif card.value == 12:
        return f"Queen of {card.suit}"
      elif card.value == 13:
        return f"King of {card.suit}"
      elif card.value == 14:
        return f"Ace of {card.suit}"
    else:
      return f"{card.value} of {card.suit}"

class Player:
  def __init__(self):
    self.card1 = Card()
    self.card2 = Card()
    
class Flop:
  def __init__(self):
    self.card1 = Card()
    self.card2 = Card()
    self.card3 = Card()

p1 = Player()
p2 = Player()
flop = Flop()

print(f"Flop: {flop.card1.info(flop.card1)}, {flop.card2.info(flop.card2)}, {flop.card3.info(flop.card3)}\n")
time.sleep(1)
print(f"Player1 hand: {p1.card1.info(p1.card1)}, {p1.card1.info(p1.card2)}\n")
time.sleep(1)
print(f"Player2 hand: {p2.card1.info(p2.card1)}, {p2.card1.info(p2.card2)}")
