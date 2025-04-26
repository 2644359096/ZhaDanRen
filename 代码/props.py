import  pygame
from .setting import *
from .generic  import  BaseProp

class BombNumProp(BaseProp):
    def __init__(self ,pos, groups ,gmap ,z=LAYERS['主层']):
        self.prop_name =BOMBNUM
        super().__init__(pos, self.prop_name, groups, gmap, z)
    def effect(self,player):
        player.bomb_num+=self.prop['effect']['add value']
        player.bomb_max_num += self.prop['effect']['add value']

class ExplosionRangeProp(BaseProp):
    def __init__(self ,pos, groups ,gmap ,z=LAYERS['主层']):
        self.prop_name =EXPLOSIONRANGE
        super().__init__(pos, self.prop_name, groups, gmap, z)
    def effect(self,player):
        player.explosion_range+=self.prop['effect']['add value']
class HPProp(BaseProp):
    def __init__(self ,pos, groups ,gmap  ,z=LAYERS['主层']):
        self.prop_name =HP
        super().__init__(pos, self.prop_name, groups, gmap, z)
    def effect(self,player):
        player.blood_volume+=self.prop['effect']['add value']
class SpeedProp(BaseProp):
    def __init__(self ,pos, groups ,gmap ,z=LAYERS['主层']):
        self.prop_name =SPEED
        super().__init__(pos, self.prop_name, groups, gmap, z)
    def effect(self,player):
        player.speed+=self.prop['effect']['add value']

class UncheckableProp(BaseProp):
    def __init__(self ,pos, groups ,gmap  ,z=LAYERS['主层']):
        self.prop_name =UNCHECKABLE
        super().__init__(pos, self.prop_name, groups, gmap, z)
    def effect(self,player):
        player.uncheckable_status=self.prop['effect']['uncheckable status']

        
class ControllableBombProp(BaseProp):
    def __init__(self ,pos, groups ,gmap ,z=LAYERS['主层']):
        self.prop_name =CONTROLLABLEBOMB
        super().__init__(pos, self.prop_name, groups, gmap, z)
    def effect(self,player):
        player.controllable_status=self.prop['effect']['controllable status']


