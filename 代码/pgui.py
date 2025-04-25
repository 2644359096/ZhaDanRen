import pygame
import pygame_gui

from pygame_gui.ui_manager import UIManager
from pygame_gui.elements.ui_window import UIWindow
from pygame_gui.elements.ui_image import UIImage
from level import Level
from gamemaps import PixleMap, GameMaps
from setting import *

PONG_WINDOW_SELECTED = pygame.event.custom_type()


class PongWindow(UIWindow):
    def __init__(self, position,size, ui_manager):
        super().__init__(pygame.Rect(position, size), ui_manager)

        game_surface_size = self.get_container().get_size()
        self.game_surface_element = UIImage(pygame.Rect((0, 0),
                                                        game_surface_size),
                                            pygame.Surface(game_surface_size).convert(),
                                            manager=ui_manager,
                                            container=self,
                                            parent_element=self)

        self.bombman_game=Level()

    def rebuild(self):
        self.enable_title_bar = False
        self.enable_close_button = False
        self.title_bar_height=0
        super().rebuild()

    def process_event(self, event):
        handled = super().process_event(event)
        if (event.type == pygame_gui.UI_BUTTON_PRESSED and
                event.ui_object_id == "#pong_window.#title_bar" and
                event.ui_element == self.title_bar):
            handled = True
            event_data = {'ui_element': self,
                          'ui_object_id': self.most_specific_combined_id}
            window_selected_event = pygame.event.Event(PONG_WINDOW_SELECTED,
                                                       event_data)
            pygame.event.post(window_selected_event)
        return handled

    def update(self, time_delta):
        if self.alive():
            self.bombman_game.update(time_delta)

        super().update(time_delta)
        self.bombman_game.draw(self.game_surface_element.image)
        pygame.draw.rect(self.image, 'red',((0,0),self.get_relative_rect().size),1)




class MiniGamesApp:
    def __init__(self):
        pygame.init()

        self.root_window_surface = pygame.display.set_mode((1024, 600))

        self.background_surface = pygame.Surface((1024, 600)).convert()
        self.background_surface.fill(pygame.Color('#505050'))
        self.ui_manager = UIManager((1024, 600), 'data/themes/theme_3.json')
        self.clock = pygame.time.Clock()
        self.is_running = True

        gmaps=GameMaps(GMAPS)
        gmap=gmaps.use_map('gmap1')
        game_surface_size= (gmap.map_shape()[0] * GAMESCREENPROPORTION, gmap.map_shape()[1] * GAMESCREENPROPORTION)


        self.pong_window_1 = PongWindow((50, 50),game_surface_size, self.ui_manager)

    def run(self):
        while self.is_running:
            time_delta = self.clock.tick(60)/1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

                self.ui_manager.process_events(event)

            self.ui_manager.update(time_delta)

            self.root_window_surface.blit(self.background_surface, (0, 0))
            self.ui_manager.draw_ui(self.root_window_surface)

            pygame.display.update()


if __name__ == '__main__':
    app = MiniGamesApp()
    app.run()
