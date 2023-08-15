from collections import namedtuple
import pygame, random, time

CardTuple = namedtuple('Card', ['value', 'suit'])

cardvalues = [2, 3, 4, 5, 6, 7, 8, 9, 10,
  11, # Jack
  12, # Queen
  13, # King
  14] # Ace

cardsuits = ['Clubs', 'Diamonds', 'Hearts', 'Spades']

class Card:
  def __init__(self):
    # Does not take into account the "deck" as a whole; collisions are currently possible
    self.data = CardTuple(value=random.choice(cardvalues), suit=random.choice(cardsuits))
    self.id = self.shorthand()
    self.img = f"graphics/cards/{self.id}.png"
    self.card_img = pygame.image.load(self.img)
    self.card_img = pygame.transform.scale(self.card_img, (self.card_img.get_width() * 4, self.card_img.get_height() * 4))
    self.card_surf = pygame.Surface(self.card_img.get_size())
    self.card_surf.blit(self.card_img, (0, 0))

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

  def shorthand(self):
    card = self.data
    return f"{card.value}{card.suit[0]}"

class Player:
  def __init__(self):
    self.card1 = Card()
    self.card2 = Card()
    
class Flop:
  def __init__(self):
    self.card1 = Card()
    self.card2 = Card()
    self.card3 = Card()