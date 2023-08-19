import itertools, os, pygame, random
from cards import *
from settings import *

# Audio
pygame.mixer.init()
audio_files = os.listdir(GAME_AUDIO_DIR)
wav_files = [file for file in audio_files if file.endswith('.wav')]
num_channels = len(wav_files)
pygame.mixer.set_num_channels(num_channels)
channels = [pygame.mixer.Channel(i) for i in range(num_channels)]

# This is more like a 'hand' and should probably be renamed
class Hand:
  def __init__(self):
    self.display_surface = pygame.display.get_surface()
    self.winner = None
    self.font = pygame.font.Font(GAME_FONT, 120)
    self.win_rotation_angle = random.uniform(-10, 10)
    self.p1 = Player()
    self.p2 = Player()
    self.flop = Flop()
    self.player_list = [self.p1, self.p2]
    self.dealer = Dealer(self.player_list, self.flop)

  def render_cards(self):
    # Draw cards at current positions
    for player in self.player_list:
      for card in player.cards:
        self.display_surface.blit(card.card_surf, card.start_position)
    for card in self.flop.cards:
      self.display_surface.blit(card.card_surf, card.position)

  def render_winner(self):
    if self.dealer.determined_winner is not None:
      # Set the text and color based on the winner
      if self.dealer.determined_winner == "Player 1":
        text = "Player 1 Wins!"
        text_color = (115, 235, 0) # Blue
      elif self.dealer.determined_winner == "Player 2":
        text = "Player 2 Wins!"
        text_color = (135, 206, 235) # Green
      elif self.dealer.determined_winner == "Tie":
        text = "Split Pot!"
        text_color = (255, 192, 203) # Pink

      coordinates = (520, 100)
      # Winner text
      text_surface = self.font.render(text, True, text_color)
      text_rect = text_surface.get_rect()
      text_rect.topleft = coordinates
      rotated_surface = pygame.transform.rotate(text_surface, self.win_rotation_angle)
      rotated_rect = rotated_surface.get_rect(center=text_rect.center)
      self.display_surface.blit(rotated_surface, rotated_rect)

  def update(self):
    self.dealer.update()
    self.render_cards()
    self.render_winner()

class Dealer():
  def __init__(self, players, flop):
    self.determined_winner = None
    self.players_list = players
    self.num_players = len(players)
    self.current_player_index = 0
    self.current_flop_index = 0
    self.printed_flop = False
    self.deck = self.generate_deck()
    random.shuffle(self.deck)
    self.animating_card = None
    self.can_deal = True
    self.can_deal_flop = False
    self.last_dealt_card_time = None
    self.last_dealt_flop_time = None
    self.dealt_cards = 0
    self.flop = flop
    self.audio_channel = 0

  def card_audio(self):
    random_wav = random.choice(wav_files)
    wav_file_path = os.path.join(GAME_AUDIO_DIR, random_wav)
    sound = pygame.mixer.Sound(wav_file_path)
    channels[self.audio_channel].play(sound)
    self.audio_channel += 1

  def generate_deck(self):
    fresh_deck = []
    for cv in cardvalues:
      for cs in cardsuits:
        fresh_deck.append(Card(cv, cs))
    return fresh_deck

  def cooldowns(self):
    # Need to use delta time
    current_time = pygame.time.get_ticks()
    if self.last_dealt_card_time and current_time - 200 > self.last_dealt_card_time:
      self.can_deal = True

    if self.last_dealt_flop_time and \
            current_time - random.randint(120, 200) > self.last_dealt_flop_time:
      self.can_deal_flop = True

  def animate_hole_card(self, card):
    current_time = pygame.time.get_ticks()
    elapsed_time = current_time - self.last_dealt_card_time

    current_card = card
    animation_duration = 200

    if elapsed_time < animation_duration:
      # Calculate the increment for each frame to move the card and update position
      x_orig, y_orig = current_card.orig_position
      x_final, y_final = current_card.position
      elapsed_ratio = elapsed_time / animation_duration
      x_change = x_orig + (x_final - x_orig) * elapsed_ratio
      y_change = y_orig + (y_final - y_orig) * elapsed_ratio
      current_card.start_position = (x_change, y_change)
    else:
      card.animation_complete = True

  def deal_hole_cards(self):
    if self.can_deal:
      # Deal card to current player's hand
      current_player = self.players_list[self.current_player_index]
      current_player.cards.append(self.deck[-1])

      # Card one of two; sets positions for both players
      if self.current_player_index == 0:
        if len(current_player.cards) == 1:
          current_player.cards[0].position = (P1_C1[0], current_player.cards[0].card_y)
        elif len(current_player.cards) == 2:
          current_player.cards[1].position = (P1_C2[0], current_player.cards[1].card_y)
        self.animating_card = current_player.cards[-1]
      # Card two of two
      elif self.current_player_index == 1:
        if len(current_player.cards) == 1:
          current_player.cards[0].position = ((P2_C1[0] - current_player.cards[0].card_surf.get_width() - 80), current_player.cards[0].card_y)
        elif len(current_player.cards) == 2:
          current_player.cards[1].position = ((P2_C2[0] - current_player.cards[1].card_surf.get_width() - 20), current_player.cards[1].card_y)
        self.animating_card = current_player.cards[-1]

      if self.animating_card:
        self.last_dealt_card_time = pygame.time.get_ticks()
        self.animate_hole_card(self.animating_card)

      # Play audio
      self.card_audio()

      # Remove dealt card from deck; change player index; prompt card dealing cooldown
      self.deck.pop(-1)
      self.current_player_index = (self.current_player_index + 1) % self.num_players
      self.can_deal = False

  def deal_flop(self):
    # Set flop card locations
    flop_x = self.players_list[0].cards[0].card_surf.get_width()
    if self.current_flop_index == 0:
      flop_x = self.players_list[0].cards[0].card_surf.get_width() * 2
    elif self.current_flop_index == 1:
      flop_x = self.players_list[0].cards[0].card_surf.get_width() * 2 + (self.players_list[0].cards[0].card_surf.get_width() + 20)
    elif self.current_flop_index == 2:
      flop_x = self.players_list[0].cards[0].card_surf.get_width() * 2 + (self.players_list[0].cards[0].card_surf.get_width() * 2 + 40)

    # Three flop cards in above set locations; remove from deck; flop cooldown
    if self.can_deal and self.can_deal_flop and self.dealt_cards - (self.num_players * 2) < 3:
      self.card_audio()
      self.flop.cards.append(self.deck[-1])
      self.flop.cards[self.current_flop_index].position = (flop_x, self.flop.cards[self.current_flop_index].card_y)
      self.deck.pop(-1)
      self.last_dealt_flop_time = pygame.time.get_ticks()
      self.can_deal_flop = False
      self.current_flop_index += 1

    # Print length of deck after card is dealt for troubleshooting
    # print(f"{len(self.deck)} cards left in deck; {self.update_dealt_card_count()} dealt.")

  # Hand-ranking algorithm reference in README.md
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
    straight = (values == list(range(values[0], values[0]-5, -1)) or values == [14, 5, 4, 3, 2])
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

  def eval_winner(self, hand_to_eval):
    eval_cards = [(value_dict[x[0]], x[1]) for x in hand_to_eval]
    if self.eval_hand(eval_cards[:5]) > self.eval_hand(eval_cards[5:]):
      print(f"P1 WIN: {self.eval_hand(eval_cards[:5])}")
      return "Player 1"
    elif self.eval_hand(eval_cards[:5]) < self.eval_hand(eval_cards[5:]):
      print(f"P2 WIN: {self.eval_hand(eval_cards[5:])}")
      return "Player 2"
    else:
      print("SPLIT")
      return "Tie"

  # Print to console
  def print_hands(self):
    for i in range(len(self.players_list)):
      print(f"P{i+1}: {[card.id for card in self.players_list[i].cards]}")
    print(f"FL: {[card.id for card in self.flop.cards]}")

  # Getter for number of dealt cards
  def update_dealt_card_count(self):
    total_card_count = 0
    for player in self.players_list:
      total_card_count += len(player.cards)
    total_card_count += len(self.flop.cards)
    return total_card_count

  def update(self):
    self.dealt_cards = self.update_dealt_card_count()
    self.cooldowns()

    if self.dealt_cards < (self.num_players * 2):
      self.deal_hole_cards()

    if self.animating_card:
      self.animate_hole_card(self.animating_card)

    # Deal flop after hole cards are dealt and animations are done
    if self.dealt_cards == (self.num_players * 2) and (not self.animating_card or self.animating_card.animation_complete):
      self.can_deal_flop = True
      self.deal_flop()
    # Slightly redundant
    if self.dealt_cards < (self.num_players * 2) + 3 and self.can_deal_flop:
      self.deal_flop()
    # Print hand data to console
    if not self.printed_flop and self.dealt_cards == (self.num_players * 2) + 3:
      self.print_hands()
      self.printed_flop = True

    if self.dealt_cards == ((self.num_players * 2) + 3) and self.determined_winner is None:
      eval_cards = [card_id.id for card_id in self.players_list[0].cards] + [card_id.id for card_id in self.flop.cards] + [card_id.id for card_id in self.flop.cards] + [card_id.id for card_id in self.players_list[1].cards]
      self.determined_winner = self.eval_winner(eval_cards)
