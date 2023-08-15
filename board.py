from pokerhands import *
from settings import *

class Board:
  def __init__(self):
    self.display_surface = pygame.display.get_surface()

    self.p1 = Player()
    self.p2 = Player()
    self.flop = Flop()

    # Log card data to console
    print(f"P1: {self.p1.card1.id}, {self.p1.card2.id}")
    print(f"FL: {self.flop.card1.id}, {self.flop.card2.id}, {self.flop.card3.id}")
    print(f"P2: {self.p2.card1.id}, {self.p2.card2.id}")

  def draw_cards(self):
    # Player 1 cards on left side of screen
    card_x = P1_C1[0]  # X coordinate
    card_y = P1_C1[1] - self.p1.card1.card_surf.get_height() // 2  # Y coordinate adjusted by half of the card's height
    self.display_surface.blit(self.p1.card1.card_surf, (card_x, card_y))
    card_x = P1_C2[0]  # X coordinate
    card_y = P1_C2[1] - self.p1.card2.card_surf.get_height() // 2  # Y coordinate adjusted by half of the card's height
    self.display_surface.blit(self.p1.card2.card_surf, (card_x, card_y))

    # Player 2 cards on right side of screen
    card_x = WIDTH - self.p2.card1.card_surf.get_width() - 80
    card_y = P2_C1[1] - self.p2.card1.card_surf.get_height() // 2  # Y coordinate adjusted by half of the card's height
    self.display_surface.blit(self.p2.card1.card_surf, (card_x, card_y))
    card_x = WIDTH - self.p2.card1.card_surf.get_width() - 20
    card_y = P2_C2[1] - self.p2.card2.card_surf.get_height() // 2  # Y coordinate adjusted by half of the card's height
    self.display_surface.blit(self.p2.card2.card_surf, (card_x, card_y))

    # Flop
    card_x = self.p1.card1.card_surf.get_width() * 2
    self.display_surface.blit(self.flop.card1.card_surf, (card_x, card_y))
    card_x += self.p1.card1.card_surf.get_width() + 60
    self.display_surface.blit(self.flop.card2.card_surf, (card_x, card_y))
    card_x += self.p1.card1.card_surf.get_width() + 60
    self.display_surface.blit(self.flop.card3.card_surf, (card_x, card_y))

  def update(self):
    self.draw_cards()
