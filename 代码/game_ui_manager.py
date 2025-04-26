import pygame
from pygame_gui import UIManager
from pygame_gui.core import UIContainer
from pygame.locals import *
from .setting import *
from .state import *





class GameUIManager(object):
    def __init__(self, display_surface, game, theme_path=None ):
        self.display_surface = display_surface
        self.display_rect=self.display_surface.get_rect()
        self.manager = UIManager(self.display_rect.size, theme_path)
        self.game = game
        self.ui_state_machine=StateMachine()

    def load_theme(self,theme_path):
        self.manager.get_theme().load_theme(theme_path)


    def state_machine_start(self):
        ui_state_configs = {
            'start': (StartUIState, (self.display_surface, self.manager, pygame.image.load('./游戏素材/ui/开始界面/标题/标题.png'),)),
            'main': (MainUIState, (self.display_surface, self.manager, ['蓝', '绿', '草', '紫'])),
            'game':(GameUIState,(self.display_surface,self.manager,self.game))
        }

        self.ui_state_machine.add_states(ui_state_configs)
        self.ui_state_machine.set_state('start')
    def process_events(self, event):
        self.manager.process_events(event)
        self.ui_state_machine.process_event(event)
    def update(self, dt):
        self.manager.update(dt)
        self.ui_state_machine.update(dt)

    def draw(self):
        self.manager.draw_ui(self.display_surface)
