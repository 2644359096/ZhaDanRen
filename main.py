import sys
import pygame
from pygame.locals import *
from 代码.setting import *
from 代码.level import Level
from 代码.game_core_ui import GameWindow
from 代码.game_ui_manager import GameUIManager
import os

# 确保当前工作目录为项目根目录

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(PROJECT_ROOT, "代码"))
os.chdir(PROJECT_ROOT)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT),DOUBLEBUF)
        pygame.display.set_caption('炸弹人')
        self.clock=pygame.time.Clock()
        self.manager=GameUIManager(self.screen,Level,'./代码/theme/button_theme.json')
        self.manager.load_theme('./代码/theme/label_theme.json')
        self.manager.load_theme('./代码/theme/select_list_theme.json')

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




