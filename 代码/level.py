import random

import pygame
from pygame.locals import *
from setting import *
from player import Player
from sprites import *
from support import *
from gamemaps import GameMaps,PixleMap
from enemy import Enemy
class Level():
    def __init__(self,game_info:dict):
        self.display_surface=None
        self.collision_sprites = pygame.sprite.Group()
        self.game_info = game_info
        self.setup()
    def setup(self):
        self.gmaps=GameMaps(GMAPS)
        self.gmap=self.gmaps.use_map(self.game_info['map_name'])
        self.map_elemenl_and_pixle_pos_list=self.gmap.init_pixle_map()
        self.pixle_map_sprites = PixleMap(self.gmap)
        self.player_initial_point=PlayerInitialPoint()

        # 路
        for map_elemenl,pixle_pos in self.map_elemenl_and_pixle_pos_list:
            MapBlock(pixle_pos, '../游戏素材/路', self.pixle_map_sprites, self.gmap, ROAD, z=LAYERS['底层'])
        # 墙
            if map_elemenl==UNBREAKABLEWALL:
                MapBlock(pixle_pos, '../游戏素材/墙/不可破坏墙', [self.pixle_map_sprites, self.collision_sprites], self.gmap, UNBREAKABLEWALL, z=LAYERS['主层'])

        #障碍物
            if map_elemenl==BREAKABLEWALL:
                MapBlock(pixle_pos, '../游戏素材/墙/可破坏墙', [self.pixle_map_sprites, self.collision_sprites], self.gmap, BREAKABLEWALL, z=LAYERS['主层'])
        #玩家出生点
            if map_elemenl in [PLAYER1,PLAYER2,PLAYER3,PLAYER4]:
                self.player_initial_point.record_point(map_elemenl,pixle_pos)


        self.player=Player(self.player_initial_point.get_point(PLAYER1), self.game_info['role_name'], self.pixle_map_sprites, self.collision_sprites,self.gmap)
        self.enemy=Enemy(self.player_initial_point.get_point(PLAYER2),ZI,self.player,self.pixle_map_sprites, self.collision_sprites,self.gmap)
    def set_display_surface(self,game_surface):
        self.display_surface=game_surface

    def get_game_rect_size(self):
        return self.gmap.map_shape()[0] * GAMESCREENPROPORTION, self.gmap.map_shape()[1] * GAMESCREENPROPORTION
    def update(self,dt):
        self.pixle_map_sprites.update(dt)
    def draw(self):
        self.pixle_map_sprites.custom_draw(self.display_surface,self.player)


