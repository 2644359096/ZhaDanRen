import sys
import pygame
import pygame_gui
from pygame.locals import *
from setting import *
from level import Level
from game_core_ui import GameWindow
from game_ui_manager import GameUIManager
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT),DOUBLEBUF)
        pygame.display.set_caption('炸弹人')
        self.clock=pygame.time.Clock()
        self.manager=GameUIManager(self.screen,Level,'./theme/button_theme.json')
        self.manager.load_theme('./theme/label_theme.json')
        self.manager.load_theme('./theme/select_list_theme.json')

        self.manager.state_machine_start()
        # self.manager.init_main_window(roles)
        # self.manager.init_game_window()
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                self.manager.process_events(event)


            dt= self.clock.tick(FPS)/1000


            self.manager.update(dt)

            self.screen.fill(Colors.white)
            self.manager.draw()
            pygame.display.update()
#
#
if __name__ == '__main__':
    game=Game()
    game.run()




