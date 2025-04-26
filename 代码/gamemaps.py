import pygame
from pygame.sprite import Group
from .setting import *
from .support import *


class GameMaps():
    def __init__(self, maps: dict):
        self.__gmaps_dict = maps

    def use_map(self, map_name: str):
        return GameMap(self.__gmaps_dict[map_name])



class GameMap():
    def __init__(self,map:dict):
        self.__gmap=map
    def __str__(self):
        map_list_str = '\n'.join(str(i) for i in self.map_elemenls())
        return map_list_str
    def map_shape(self):
        return self.__gmap[0]

    def map_elemenls(self):
        return self.__gmap[1]

    def set_map_elemenl(self, _index: tuple[int, int], new_elemenl):
        self.__gmap[1][_index[1]][_index[0]] = new_elemenl

    def get_map_elemenl(self, _index: tuple[int, int]):
        return self.__gmap[1][_index[1]][_index[0]]

    @staticmethod
    def conversion_pos(pos, mode):
        if mode == GMAPPOS:
            return int(pos[0] // PIXELSIZE), int(pos[1] // PIXELSIZE)
        elif mode == PIXELPOS:
            return pos[0] * PIXELSIZE, pos[1] * PIXELSIZE


    def get_danger_zones(self):
        pass
    def get_map_elemenl_pos(self, elemenl, flag=GMAPPOS):
        for c in range(self.map_shape()[1]):
            for r in range(self.map_shape()[0]):
                if self.__gmap[1][c][r] == elemenl:
                    if flag == GMAPPOS:
                        return r, c
                    if flag == PIXELPOS:
                        return (r * PIXELSIZE), (c * PIXELSIZE)



    def get_pixel_coordinates(self):
        pixel_coordinates = []
        pixel_pos_slist = []
        for y in range(0, self.map_shape()[1]):
            for x in range(0, self.map_shape()[0]):
                pixel_y = PIXELSIZE * y
                pixel_x = PIXELSIZE * x
                pixel_pos_slist.append((pixel_x, pixel_y))
            pixel_coordinates.append(pixel_pos_slist)
            pixel_pos_slist = []
        return pixel_coordinates

    def init_pixle_map(self):
        map_elemenl_and_pixle_pos_list = []
        for map_elemenl_list, pos_list in zip(self.map_elemenls(), self.get_pixel_coordinates()):
            for map_elemenl, pixle_pos in zip(map_elemenl_list, pos_list):
                map_elemenl_and_pixle_pos_list.append((map_elemenl, pixle_pos))
        return map_elemenl_and_pixle_pos_list
class PixleMap(Group):
    def __init__(self, gmap: GameMaps):
        super().__init__()
        self.gmap = gmap
        self.__map_shape = self.gmap.map_shape()
        self.offset = pygame.math.Vector2()


    def get_sprite(self, pos, map_elemenl: None|int=None):
        sprites = []
        for sprite in self.sprites():
            if sprite.rect.collidepoint(pos):
                if sprite.map_elemenl == map_elemenl:
                    return sprite
                else:
                    sprites.append(sprite)
        return sprites[-1]

    def custom_draw(self, draw_surf,player):
            # 绘制游戏表面并居中
            self.game_surface=draw_surf
            self.game_rect=self.game_surface.get_rect()

            # 计算偏移量
            self.offset.x = self._calculate_offset(player.rect.centerx, self.game_rect.centerx, PIXELSIZE * self.__map_shape[0], self.game_rect.width)
            self.offset.y = self._calculate_offset(player.rect.centery, self.game_rect.centery, PIXELSIZE * self.__map_shape[1], self.game_rect.height)

            # 排序
            sorted_sprites = sorted(self.sprites(), key=lambda sprite: sprite.rect.centery)

            for layer in LAYERS.values():
                for sprite in sorted_sprites:
                    if sprite.z == layer:
                        self._draw_sprite(sprite, player)

    @staticmethod
    def _calculate_offset(player_center, game_center, map_size, game_size):
        if player_center <= game_center:
            return 0
        elif player_center >= map_size - game_center:
            return map_size - game_size
        else:
            return player_center - game_center

    def _draw_sprite(self, sprite, player):
        offset_rect = sprite.rect.copy()
        if hasattr(sprite, 'prop_type'):
            if sprite.prop_type == UNCHECKABLE:
                offset_rect.topleft = player.rect.topleft
            else:
                offset_rect.center = sprite.rect.center
        else:
            offset_rect.center = sprite.rect.center

        offset_rect.topleft -= self.offset
        self.game_surface.blit(sprite.image, offset_rect)

    def update(self, *args, **kwargs):

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.map_elemenl):
            sprite.update(*args, **kwargs)
