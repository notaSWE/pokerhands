from pokerhands import *
from settings import *
import itertools

# This is more like a 'hand' and should probably be renamed
class Board:
  def __init__(self):
    self.display_surface = pygame.display.get_surface()
    self.cards_to_deal = []
    self.winner = None
    self.font = font = pygame.font.Font(GAME_FONT, 46)
    self.win_rotation_angle = random.uniform(-10, 10)
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
    eval_cards = [card_id.id for card_id in self.p1.cards] + [card_id.id for card_id in self.flop.cards] + [card_id.id for card_id in self.flop.cards] + [card_id.id for card_id in self.p2.cards]
    eval_cards = [(value_dict[x[0]], x[1]) for x in eval_cards]

    # Find winner
    if self.dealer.eval_hand(eval_cards[:5]) > self.dealer.eval_hand(eval_cards[5:]):
      print(f"P1 WIN: {self.dealer.eval_hand(eval_cards[:5])}")
      self.winner = "Player 1"
    elif self.dealer.eval_hand(eval_cards[:5]) < self.dealer.eval_hand(eval_cards[5:]):
      print(f"P2 WIN: {self.dealer.eval_hand(eval_cards[5:])}")
      self.winner = "Player 2"
    else:
      print("SPLIT")
      self.winner = "Tie"

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
    card_x += self.p1.cards[0].card_surf.get_width() + 40
    self.display_surface.blit(self.flop.cards[1].card_surf, (card_x, self.flop.cards[1].card_y))
    card_x += self.p1.cards[0].card_surf.get_width() + 40
    self.display_surface.blit(self.flop.cards[2].card_surf, (card_x, self.flop.cards[2].card_y))

  def render_winner(self):
    if self.winner != None:
      # Set the text and color based on the winner
      if self.winner == "Player 1":
          text = "Player 1 Wins!"
          text_color = (135, 206, 235) # Blue
          coordinates = (20, 200)
      elif self.winner == "Player 2":
          text = "Player 2 Wins!"
          text_color = (115, 235, 0) # Green
          coordinates = (1580, 200)
      elif self.winner == "Tie":
          text = "Split Pot!"
          text_color = (255, 185, 250) # Pink
          coordinates = (850, 200)
      text_surface = self.font.render(text, True, text_color)
      text_rect = text_surface.get_rect()
      text_rect.topleft = coordinates
      rotated_surface = pygame.transform.rotate(text_surface, self.win_rotation_angle)
      rotated_rect = rotated_surface.get_rect(center=text_rect.center)
      self.display_surface.blit(rotated_surface, rotated_rect)

  def update(self):
    self.render_cards()
    self.render_winner()

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

  def eval_hand(self, hand):
    # Return ranking followed by tie-break information.
    # 8. Straight Flush
    # 7. Four of a Kind
    # 6. Full House
    # 5. Flush
    # 4. Straight
    # 3. Three of a Kind
    # 2. Two pair
    # 1. One pair
    # 0. High card

    values = sorted([c[0] for c in hand], reverse=True)
    suits = [c[1] for c in hand]
    straight = (values == list(range(values[0], values[0]-5, -1))
          or values == [14, 5, 4, 3, 2])
    flush = all(s == suits[0] for s in suits)

    if straight and flush: return 8, values[1]
    if flush: return 5, values
    if straight: return 4, values[1]

    trips = []
    pairs = []
    for v, group in itertools.groupby(values):
      count = sum(1 for _ in group)
      if count == 4: return 7, v, values
      elif count == 3: trips.append(v)
      elif count == 2: pairs.append(v)

    if trips: return (6 if pairs else 3), trips, pairs, values
    return len(pairs), pairs, values