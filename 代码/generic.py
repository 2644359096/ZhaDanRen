import pygame
from setting import *
from gamemaps import GameMap
from pygame_gui.core import UIContainer
from pygame_gui.elements import  UIImage

class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, gmap: GameMap, map_elemenl=ROAD, z=LAYERS['底层']):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.gmap = gmap
        self.z = z
        self.map_elemenl = map_elemenl
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.15, -self.rect.height * 0.4)

    def gamp_update(self):
        self.gmap.set_map_elemenl((int(self.rect.centerx / PIXELSIZE), int(self.rect.centery / PIXELSIZE)),
                                  self.map_elemenl)

    def after_bombed(self):
        pass

    def update(self, *args, **kwargs):
        self.gamp_update()


class BaseProp(Generic):
    def __init__(self, pos, prop_name, groups, gmap: GameMap, z=LAYERS['主层']):
        self.prop = PROPS[prop_name]
        self.frames = self.prop['frames']
        self.picked_frames = import_folder('../游戏素材/道具/被拾取')
        self.picked_status = False
        self.frame_index = 0
        self.map_elemenl = PROP
        super().__init__(pos, self.frames[int(self.frame_index)], groups, gmap, self.map_elemenl, z)
        self.prop_type = self.prop['type']
        self.group = groups[0]
        self.start_time = pygame.time.get_ticks()

    def animate(self, dt):
        if self.picked_status:
            self.frames = self.picked_frames
            self.frame_index += 3 * dt
        else:
            self.frame_index += 4 * dt
        if self.frame_index > len(self.frames):
            self.frame_index = 0
            if self.picked_status:
                self.kill()
        self.image = pygame.transform.scale(self.frames[int(self.frame_index)],
                                            (PIXELSIZE, PIXELSIZE)).convert_alpha()

    def collision(self, player):
        player.props.append(self)
        self.picked_status = True
        self.hitbox = self.rect.copy().inflate(-self.rect.width, -self.rect.height)

    def effect(self, player):
        print('effect')

    def time_out(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time > self.prop['existence time']:
            self.kill()

    def after_bombed(self):
        self.kill()

    def update(self, dt):
        self.gamp_update()
        self.time_out()
        self.animate(dt)

class BaseState():
    """状态基类"""
    def __init__(self,state_machine):
        self.state_machine=state_machine

    def enter(self):
        """状态进入时的初始化"""
        pass

    def exit(self):
        """状态退出时的清理"""
        pass

    def update(self, delta_time):
        """状态逻辑更新"""
        pass

    def process_event(self, event):
        """事件处理（如按键、碰撞等）"""
        harder=False


        return harder


class BaseUIState(BaseState):
    def __init__(self, state_machine,display_surface,manager):
        super().__init__(state_machine)
        self.display_surface = display_surface
        self.display_rect = self.display_surface.get_rect()
        self.manager = manager
        self.ui_window=None #type:UIContainer

    def enter(self):
        self.ui_window.show()
        self.ui_window.enable()

    def exit(self):
        self.ui_window.disable()
        self.ui_window.hide()


class BaseEnemyState(BaseState):
    def __init__(self, state_machine, ai):
        super().__init__(state_machine)
        self.ai = ai  # AI对象引用

    def get_player_distance(self):
        """获取玩家距离"""
        return get_distance(self.ai.pos, self.ai.player.pos)

    def get_danger_zones(self):
        """获取危险区域（如炸弹、障碍物）"""
        return self.ai.gmap.get_danger_zones()

    def calculate_weights(self):
        """根据环境计算权重（子类需重写）"""
        pass

    def update(self, delta_time):
        """状态逻辑更新（子类需重写）"""
        pass

class BaseContainer(UIContainer):
    def __init__(self, relative_rect, manager, layout,container=None,boundary_width=0,boundary_color=(0,0,0),boundary_radius=-1):
        super().__init__(relative_rect, manager,container=container)
        self.boundary_width=boundary_width
        self.boundary_color=boundary_color
        self.boundary_radius=boundary_radius
        if self.boundary_width>0:
            self.ui_image=UIImage(
                relative_rect=pygame.Rect((0,0),relative_rect.size),
                image_surface=pygame.Surface(relative_rect.size),
                manager=manager,
                container=self,
                parent_element=self
            )
    def update(self, time_delta: float):
        super().update(time_delta)
        if self.boundary_width>0:
            self.ui_image.image.fill((255,255,255))
            pygame.draw.rect(self.ui_image.image,self.boundary_color,self.ui_image.relative_rect,self.boundary_width,border_radius=self.boundary_radius)


