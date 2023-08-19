from hand import *
from pokerhands import *
from settings import *
import ctypes, pygame, sys

# Maintain resolution regardless of Windows scaling settings
ctypes.windll.user32.SetProcessDPIAware()

class Game:
  def __init__(self):

    # General setup
    pygame.init()
    self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE_STRING)
    self.clock = pygame.time.Clock()
    self.hand = Hand()

  def run(self):

    self.start_time = pygame.time.get_ticks()

    while True:
      # Handle quit operation
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
          if event.button == 1:  # Left mouse button
            mouse_down = True

        if event.type == pygame.MOUSEBUTTONUP:
          if event.button == 1:  # Left mouse button
            if mouse_down:
              mouse_down = False
              self.hand = Hand()

      # Time variables
      self.delta_time = (pygame.time.get_ticks() - self.start_time) / 1000
      self.start_time = pygame.time.get_ticks()
      pygame.display.update()
      self.screen.fill(BG_COLOR)

      self.hand.update()
      self.clock.tick(FPS)

if __name__ == '__main__':
  game = Game()
  game.run()