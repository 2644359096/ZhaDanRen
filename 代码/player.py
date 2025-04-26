import pygame
from .setting import *
from .support import *
from .props import *
from .sprites import Bomb,UncheckableShield,ControllableBomb
from .gamemaps import GameMap
from .game_timer import Timer,KeyTimer


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, role, group, collision_sprites, gmap:GameMap, z=LAYERS['主层']):
        super().__init__(group)

        self.import_assets(role)
        self.directions=XIA
        self.status = '下_站'
        self.frame_index = 0
        self.group=group

        self.image=self.animations[self.status][self.frame_index]
        self.rect=self.image.get_rect(topleft=pos)
        self.direction = pygame.math.Vector2()

        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 120
        self.map_elemenl = PLAYER1
        self.z = z
        self.collision_sprites = collision_sprites
        self.hitbox=self.rect.copy().inflate((-self.rect.width*0.1,-self.rect.height*0.25))

        self.gmap=gmap
        self.keydown_maxtime= 500
        self.keydown_mintime= 50
        self.key_timers={
            pygame.K_j:KeyTimer(pygame.K_j,self.keydown_mintime,self.keydown_maxtime),
        }


        self.blood_volume=1
        self.bomb_num=1
        self.bomb_max_num=self.bomb_num
        self.bomb_atk=1
        self.explosion_range=1

        self.uncheckable_status=False


        self.controllable_status=False
        self.explosion_controllable_boob = False
        self.drop_controllable_boob = False
        self.drop_boob=False

        self.props_classes=(HPProp, BombNumProp, ExplosionRangeProp, SpeedProp, UncheckableProp, ControllableBombProp)
        self.props= []
        self.applied_props=set()

        self.timers={
            'drop_bombs':Timer(200,self.drop_boobs)
        }
    def import_assets(self,role):
        self.animations = {
            '_'.join((SHANG,ZHAN)):[],
            '_'.join((SHANG,ZOU)):[],
            '_'.join((XIA,ZHAN)):[],
            '_'.join((XIA,ZOU)):[],
            '_'.join((ZUO,ZHAN)):[],
            '_'.join((ZUO,ZOU)):[],
            '_'.join((YOU, ZHAN)):[],
            '_'.join((YOU, ZOU)):[],
            DEAD:[]
        }
        for animation in self.animations.keys():
            if animation == DEAD:
                full_path = './游戏素材/人物/人物状态/死亡'
            else:
                full_path='./游戏素材/人物/人物行为/'+role+'/'+animation
            self.animations[animation]=import_folder(full_path)
    def animate(self,dt):
        if self.status==DEAD:
            self.frame_index += 2.5*dt
        else:
            self.frame_index+=4*dt
        if self.frame_index>=len(self.animations[self.status]):
            self.frame_index=0
            if self.status==DEAD:
                self.kill()
        self.image =pygame.transform.scale(self.animations[self.status][int(self.frame_index % len(self.animations))],(PIXELSIZE,PIXELSIZE)).convert_alpha()


    def input(self):
        keys=pygame.key.get_pressed()
        if not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            self.direction.x = 0
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.directions=SHANG
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.directions=XIA
        if not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            self.direction.y = 0
            if keys[pygame.K_RIGHT]:
                self.direction.x=1
                self.directions=YOU
            elif keys[pygame.K_LEFT]:
                self.direction.x=-1
                self.directions=ZUO
            else:
                self.direction.x=0
        #检测j键是否处于长按状态并且检测长按时间是否大于最短时间
        key_status = self.key_timers[pygame.K_j].gat_key_status()
        if self.controllable_status:
            if key_status == KeyTimer.KEY_LONG:
                self.explosion_controllable_boob = True
            elif key_status == KeyTimer.KEY_SHORT:
                if not self.timers['drop_bombs'].active and not self.is_alive(BOMB):
                    self.timers['drop_bombs'].start()
            elif key_status == KeyTimer.KEY_NOT_PRESSED:
                self.explosion_controllable_boob = False
        elif key_status == KeyTimer.KEY_SHORT:
            if not self.timers['drop_bombs'].active and not self.is_alive(BOMB):
                self.timers['drop_bombs'].start()



    def get_bomb_pos(self):
        return self.gmap.get_map_elemenl_pos(self.map_elemenl, PIXELPOS)
    def is_alive(self,map_elemenl):
        if self.group.get_sprite(self.get_bomb_pos(),map_elemenl).map_elemenl == map_elemenl:
            return self.group.get_sprite(self.get_bomb_pos(), map_elemenl).alive()
        else:
            return False
    def drop_boobs(self):
        if self.bomb_num>0:
            if self.controllable_status:
                ControllableBomb(self, self.explosion_range, self.get_bomb_pos(),self.group, self.collision_sprites, self.gmap)

            else:
                Bomb(self, self.explosion_range, self.get_bomb_pos(), self.group, self.collision_sprites, self.gmap)
            self.bomb_num-=1

    def after_bombed(self):
        self.blood_volume-=self.bomb_atk

    def props_effect(self):
        for prop in self.props:
            if prop not in self.applied_props:
                prop.effect(self)
                self.applied_props.add(prop)
    def apply_props(self):
        if self.uncheckable_status:
            UncheckableShield(self,(self.rect.x,self.rect.y+20),self.group)
            self.uncheckable_status=False
    def get_status(self):
        if self.direction.magnitude() == 0:
            self.status='_'.join((self.directions,ZHAN))
        else:
            self.status = '_'.join((self.directions, ZOU))
        if self.blood_volume<=0:
            self.status=DEAD
    def collision(self,direction):
        for sprite in self.collision_sprites.sprites():
            if hasattr(sprite,"hitbox"):
                if sprite.hitbox.colliderect(self.hitbox):
                    if type(sprite) in self.props_classes:
                        sprite.collision(self)
                    if direction == 'horizontal':
                        if self.direction.x>=0:
                            self.hitbox.right=sprite.hitbox.left
                        if self.direction.x<=0:
                            self.hitbox.left=sprite.hitbox.right
                        self.rect.centerx=self.hitbox.centerx
                        self.pos.x=self.hitbox.centerx
                    if direction == 'vertical':
                        if self.direction.y>=0:
                            self.hitbox.bottom=sprite.hitbox.top
                        if self.direction.y<=0:
                            self.hitbox.top=sprite.hitbox.bottom
                        self.rect.centery=self.hitbox.centery
                        self.pos.y=self.hitbox.centery

    def move(self,dt):
        self.pos.x += self.direction.x*dt*self.speed
        self.hitbox.centerx=round(self.pos.x)
        self.rect.centerx=self.hitbox.centerx
        self.collision('horizontal')

        self.pos.y += self.direction.y*dt*self.speed
        self.hitbox.centery=round(self.pos.y)
        self.rect.centery=self.hitbox.centery
        self.collision('vertical')

    def gmap_update(self):
        self.gmap.set_map_elemenl(self.gmap.conversion_pos(self.pos,GMAPPOS),self.map_elemenl)
    def timer_update(self):
        for timer in self.timers.values():
            timer.update()
    def key_timers_update(self):
        for key_timer in self.key_timers.values():
            key_timer.update()
    def update(self, dt):
        self.gmap_update()
        if self.status != DEAD:
            self.input()
            self.get_status()
            self.move(dt)
            self.props_effect()
            self.apply_props()
            self.timer_update()
            self.key_timers_update()
        self.animate(dt)
        # print(f'血量：{self.blood_volume},炸弹数量：{self.bomb_num},爆炸范围：{self.explosion_range},速度：{self.speed}')





