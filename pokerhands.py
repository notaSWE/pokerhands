from collections import namedtuple
from settings import *
import pygame, random, time

CardTuple = namedtuple('Card', ['value', 'suit'])

fresh_deck = []

cardvalues = [2, 3, 4, 5, 6, 7, 8, 9, 10,
  11, # Jack
  12, # Queen
  13, # King
  14] # Ace

cardsuits = ['C', 'D', 'H', 'S']

class Card:
  def __init__(self, input_value, input_suit):
    self.data = CardTuple(value=input_value, suit=input_suit)
    self.id = f"{self.data.value}{self.data.suit}"
    self.img = f"graphics/cards/{self.id}.png"
    self.card_img = pygame.image.load(self.img)
    self.card_img = pygame.transform.scale(self.card_img, (self.card_img.get_width() * 4, self.card_img.get_height() * 4))
    self.card_surf = pygame.Surface(self.card_img.get_size())
    self.card_surf.blit(self.card_img, (0, 0))
    self.card_y = (P1_C1[1] - self.card_surf.get_height() // 2) + random.randint(-20, 20)

class Player:
  def __init__(self):
    self.cards = []
    
class Flop:
  def __init__(self):
    self.cards = []

for cv in cardvalues:
  for cs in cardsuits:
    fresh_deck.append(Card(cv, cs))