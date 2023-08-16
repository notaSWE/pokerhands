from pokerhands import *
from settings import *

class Board:
  def __init__(self):
    self.display_surface = pygame.display.get_surface()

    self.dealer = Dealer()
 
    self.p1 = Player()
    self.p2 = Player()
    self.flop = Flop()

    # Deal cards and, burn one, turn three

    self.dealer.deal_card(self.p1)
    self.dealer.deal_card(self.p2)
    self.dealer.deal_card(self.p1)
    self.dealer.deal_card(self.p2)
    self.dealer.deal_card("muck")
    self.dealer.deal_card(self.flop)
    self.dealer.deal_card(self.flop)
    self.dealer.deal_card(self.flop)

    # Log card data to console

    print(f"P1: {[card_id.id for card_id in self.p1.cards]}")
    print(f"FL: {[card_id.id for card_id in self.flop.cards]}")
    print(f"P2: {[card_id.id for card_id in self.p2.cards]}")

  def render_cards(self):
    # Player 1 cards on left side of screen
    card_x = P1_C1[0] # X coordinate
    self.display_surface.blit(self.p1.cards[0].card_surf, (card_x, self.p2.cards[0].card_y))
    card_x = P1_C2[0] # X coordinate
    self.display_surface.blit(self.p1.cards[1].card_surf, (card_x, self.p2.cards[1].card_y))

    # Player 2 cards on right side of screen
    card_x = WIDTH - self.p2.cards[0].card_surf.get_width() - 80
    self.display_surface.blit(self.p2.cards[0].card_surf, (card_x, self.p2.cards[0].card_y))
    card_x = WIDTH - self.p2.cards[1].card_surf.get_width() - 20
    self.display_surface.blit(self.p2.cards[1].card_surf, (card_x, self.p2.cards[1].card_y))

    # Flop
    card_x = self.p1.cards[0].card_surf.get_width() * 2
    self.display_surface.blit(self.flop.cards[0].card_surf, (card_x, self.flop.cards[0].card_y))
    card_x += self.p1.cards[0].card_surf.get_width() + 60
    self.display_surface.blit(self.flop.cards[1].card_surf, (card_x, self.flop.cards[1].card_y))
    card_x += self.p1.cards[0].card_surf.get_width() + 60
    self.display_surface.blit(self.flop.cards[2].card_surf, (card_x, self.flop.cards[2].card_y))

  def update(self):
    self.render_cards()

class Dealer():
  def __init__(self):
    self.deck = fresh_deck.copy()
    random.shuffle(self.deck)
    self.dealt_cards = []

  def deal_card(self, dest):
    if dest != "muck":
      dest.cards.append(self.deck[-1])
      self.dealt_cards.append(self.deck[-1])
      self.deck.pop(-1)
    else:
      self.dealt_cards.append(self.deck[-1])
      self.deck.pop(-1)
    
    # Print length of deck after card is dealt
    # print(f"{len(self.deck)} cards left in deck; {len(self.dealt_cards)} dealt.")