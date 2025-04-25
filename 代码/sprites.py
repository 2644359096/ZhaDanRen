import pygame
import random
from setting import *
from generic import Generic
from gamemaps import GameMap
from props import *
from support import import_folder, GameObjectFactory

prop_factory = GameObjectFactory([HP, BOMBNUM, EXPLOSIONRANGE, SPEED, UNCHECKABLE, CONTROLLABLEBOMB],
                                 [HPProp, BombNumProp, ExplosionRangeProp, SpeedProp, UncheckableProp,
                                  ControllableBombProp])


class PlayerInitialPoint():
    def __init__(self):
        self.__player_points = {}

    def record_point(self, map_elemenl, pos):
        self.__player_points[map_elemenl] = pos

    def get_point(self, player):
        return self.__player_points[player][0], self.__player_points[player][1]


class MapBlock(Generic):
    def __init__(self, pos, surf_path, groups, gmap, map_elemenl=ROAD, z=LAYERS['底层']):
        self.image = pygame.transform.scale(random.choice(import_folder(surf_path)), (PIXELSIZE, PIXELSIZE))
        self.rect = self.image.get_rect(topleft=pos)
        super().__init__(self.rect.topleft, self.image, groups, gmap, map_elemenl, z)

        if z == LAYERS['底层']:
            self.hitbox = self.rect.copy().inflate(-self.rect.width, -self.rect.height)

    def after_bombed(self):
        if self.map_elemenl == BREAKABLEWALL:
            self.spawn_props()
            self.kill()

    def spawn_props(self):
        selected_prop = random.choices(PROPS_KEYS, weights=PROPS_PROBABILITYS, k=1)[0]
        if selected_prop is not None:
            prop_factory.create_game_object(selected_prop, self.rect.topleft, self.groups(), self.gmap, self.z)


class PathLine(Generic):
    def __init__(self, pos,surf_path,direction, groups,gmap, map_elemenl=ROAD, z=LAYERS['上层']):
        image = pygame.transform.scale(random.choice(import_folder(surf_path)), (PIXELSIZE, PIXELSIZE))
        if direction is not None:
            angle = self.get_angle_from_direction(direction)
            image = pygame.transform.rotate(image, angle)

        super().__init__(pos,image,groups,gmap,map_elemenl,z)

    @staticmethod
    def get_angle_from_direction(direction):
        """根据方向返回旋转角度"""
        if direction == XIA:
            return 0
        elif direction == SHANG:
            return 180
        elif direction == YOU:
            return 90
        elif direction == ZUO:
            return -90
        else:
            return 0

class Bomb(Generic):
    def __init__(self, player, explosion_range, pos, group:GameMap, collosion_sprites, gmap,
                 z=LAYERS['主层']):
        self.frame_index = 0
        self.frames = import_folder('../游戏素材/炸弹/炸弹')
        self.player = player
        self.map_elemenl = BOMB
        super().__init__(pos, self.frames[int(self.frame_index)], group, gmap, self.map_elemenl, z)
        self.explosion_range = explosion_range
        self.explosion_range_surfaces = import_folder('../游戏素材/炸弹/炸弹范围')
        self.explosion_start = False
        self.exploding = False
        self.explosion_end = False
        self.explosion_range_frame_index = 0

        self.group = group
        self.collision_sprites = collosion_sprites

    def animate(self, dt):
        self.frame_index += 3 * dt
        if self.frame_index > len(self.frames):
            self.frame_index = 0
            self.explosion_end = True
            self.kill()
        if int(self.frame_index) == 10:
            self.explosion_start = True
        self.image = pygame.transform.scale(self.frames[int(self.frame_index)],
                                            (PIXELSIZE, PIXELSIZE)).convert_alpha()

    def collision(self):
        if not self.rect.colliderect(self.player.rect):
            self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.15, -self.rect.height * 0.4)
            self.add(self.collision_sprites)

    # 炸弹附近的上下左右坐标, 并检查地图元素
    def get_explosion_pos(self, explosion_range: int):
        return_ranges_pos = set()
        center_x, center_y = self.rect.centerx / PIXELSIZE, self.rect.centery / PIXELSIZE

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            for i in range(1, explosion_range + 1):
                x, y = center_x + dx * i, center_y + dy * i
                if self.gmap.get_map_elemenl((int(x), int(y))) != UNBREAKABLEWALL:
                    return_ranges_pos.add(self.gmap.conversion_pos((int(x), int(y)), PIXELPOS))
                else:
                    break
        return_ranges_pos.add(self.rect.topleft)
        return return_ranges_pos

    def explosion(self):
        if self.explosion_start and not self.exploding:
            for pos in self.get_explosion_pos(self.explosion_range):
                ExplosionRange(
                    player=self.player,
                    pos=pos,
                    frames=self.explosion_range_surfaces,
                    group=self.group,
                    gmap=self.gmap,
                    frame_index=self.explosion_range_frame_index,
                    z=LAYERS['主层'])

            self.explosion_start = False
            self.exploding = True
        if self.explosion_end:
            self.player.bomb_num += 1

    def after_bombed(self):
        self.frame_index = 10

    def update(self, dt):
        self.gamp_update()
        self.collision()
        self.animate(dt)
        self.explosion()


class ControllableBomb(Bomb):
    def __init__(self, player, explosion_range, pos, group, collosion_sprites, gmap: GameMap, z=LAYERS['主层']):
        super().__init__(player, explosion_range, pos, group, collosion_sprites, gmap, z)
        self.standby_frames = import_folder('../游戏素材/炸弹/遥控炸弹/待命中')
        self.explosion_frames = import_folder('../游戏素材/炸弹/遥控炸弹/接收信号')
        self.frames = self.standby_frames
        self.explosion_range_surfaces = import_folder('../游戏素材/炸弹/遥控炸弹范围')
        self.explosion_status=False

    def animate(self, dt):
        if self.player.explosion_controllable_boob:
            self.frame_index=0
            self.frames=self.explosion_frames
            self.explosion_status=True

        if self.explosion_status:
            self.frame_index += 3*dt
            if int(self.frame_index) == 7:
                self.explosion_start = True
        else:
            self.frame_index += 2 * dt

        if self.frame_index > len(self.frames):
            self.frame_index = 0
            if self.explosion_status:
                self.frame_index = 0
                self.restore_bomb_num()
                self.kill()
        self.image = pygame.transform.scale(self.frames[int(self.frame_index)], (PIXELSIZE, PIXELSIZE)).convert_alpha()
    def restore_bomb_num(self):
        if self.player.bomb_num == 0:
            self.player.controllable_status=False
            self.player.bomb_num = self.player.bomb_max_num

class ExplosionRange(Generic):
    def __init__(self, player, pos, frames, group, gmap: GameMap, frame_index=0, z=LAYERS['主层']):
        self.frame_index = frame_index
        self.frames = frames
        self.map_elemenl = BOMBRANGER
        super().__init__(pos, self.frames[int(self.frame_index)], group, gmap, self.map_elemenl, z)
        self.group = group
        self.player = player
        self.explosion_start = False

    def animate(self, dt):
        self.frame_index += 3 * dt
        if self.frame_index > len(self.frames):
            self.frame_index = 0
            self.explosion_start = True
            self.kill()
        self.image = pygame.transform.scale(self.frames[int(self.frame_index)], (PIXELSIZE, PIXELSIZE)).convert_alpha()

    def explosion_kill(self):
        if self.group.get_sprite(self.rect.center).map_elemenl in (
        BOMB, BREAKABLEWALL, PROP, PLAYER1, PLAYER2, PLAYER3, PLAYER4):
            self.group.get_sprite(self.rect.center).after_bombed()

    def update(self, dt):
        self.gamp_update()
        self.animate(dt)
        self.explosion_kill()




class UncheckableShield(pygame.sprite.Sprite):
    def __init__(self, player, pos, group, z=LAYERS['主层']):
        super().__init__(group)
        self.frame_index = 0
        self.start_frame_index = 0
        self.end_frame_index = 0
        self.prop_type = UNCHECKABLE
        self.start_frames = import_folder('../游戏素材/人物/人物状态/无敌/开始')
        self.end_frames = import_folder('../游戏素材/人物/人物状态/无敌/结束')
        self.frames = self.start_frames
        self.image = pygame.transform.scale(self.frames[int(self.frame_index)],
                                            (PIXELSIZE + 5, PIXELSIZE + 10)).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.map_elemenl = PROP
        self.group = group
        self.z = z
        self.uncheckable_dealy = PROPS['uncheckable']['uncheckable time']
        self.uncheckable_end = False
        self.unchecking = False
        self.start_time = pygame.time.get_ticks()
        self.player = player
        self.player_blood_volume = self.player.blood_volume

    def animate(self, dt):
        self.frame_index += 2.5 * dt
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time <= self.uncheckable_dealy:
            self.frames = self.start_frames
        else:
            self.frame_index += 3 * dt
            self.frames = self.end_frames
            self.unchecking = True

        if self.frame_index > len(self.frames):
            self.frame_index = 0
            if self.unchecking:
                self.uncheckable_end = True
                self.kill()
        self.image = pygame.transform.scale(self.frames[int(self.frame_index)], (PIXELSIZE, PIXELSIZE)).convert_alpha()

    def after_bombed(self):
        if not self.uncheckable_end:
            self.player.bomb_atk = 0
        else:
            self.player.bomb_atk = 1

    def update(self, dt):
        self.after_bombed()
        self.animate(dt)
