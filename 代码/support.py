import os
from os import listdir,walk
import pygame
from pygame_gui import UI_BUTTON_PRESSED

from game_timer import Timer

def import_folder(path):
    surface_list = []
    for _,f2,img_files in walk(path):
        for folder in f2:
            if not os.path.isfile(path+'/'+folder):
                for img_file in listdir(path+'/'+folder):
                    full_path = path + '/' + folder + '/' + img_file
                    image_surf = pygame.image.load(full_path).convert_alpha()
                    surface_list.append(image_surf)

        for image in img_files:
            full_path = path+'/'+image
            image_surf = pygame.image.load(full_path)
            surface_list.append(image_surf)

    return surface_list
class DoubleClick():
    MOUSE='1'
    KEY='2'
    def __init__(self,click_type,click_value):
        self.click_type=click_type
        self.click_value=click_value
        self.double_click_timer=Timer(300)
    def double_click(self,event:pygame.event.Event):
        if not self.double_click_timer.active:
            if self.click_type == self.MOUSE:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == self.click_value:
                    self.double_click_timer.start()
                if event.type == UI_BUTTON_PRESSED and event.mouse_button==self.click_value:
                    self.double_click_timer.start()
            if self.click_value == self.KEY:
                keys=pygame.key.get_pressed()
                if keys[self.click_value]:
                    self.double_click_timer.start()

        else:
            if self.click_type == self.MOUSE:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == self.click_value:
                    return True
                if event.type == UI_BUTTON_PRESSED and event.mouse_button == self.click_value:
                    return True
            if self.click_value == self.KEY:
                keys=pygame.key.get_pressed()
                if keys[self.click_value]:
                    return True
        return False


    def update(self):
        self.double_click_timer.update()

def import_frames(path):
    surface_list=[]
    for path, _, image_paths in os.walk(path):
        if '总' not in path and '站' not in path:
            for image_path in image_paths:
                surface_list.append(pygame.image.load(path+'/'+image_path))
    return surface_list

class OldVar():
    def __init__(self):
        self.values=[]

    def update(self,new_value):
        self.values.insert(0, new_value)
        if len(self.values)>2:
            self.values.pop()
    def get_value(self):
        return self.values[-1]

def is_range_equal(diff_value,value1,value2):
    def __abs(vlaue):
        abs_list=[]
        for i in vlaue:
            abs_list.append(abs(i))
        return tuple(abs_list)
    value=pygame.math.Vector2(value1)-pygame.math.Vector2(value2)
    return tuple(diff_value) >= __abs(value)
def get_distance(pos1, pos2):
    return ((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)**0.5

class GameObjectFactory():
    """
    游戏对象工厂类，用于创建不同类型的游戏对象。

    该工厂类根据通用变量和对应的类生成游戏对象，使得游戏对象的创建过程更加灵活和可扩展。
    """

    def __init__(self,common_variables,classes):
        """
        初始化游戏对象工厂。

        参数:
        common_variables -- 通用变量列表，用于标识不同的游戏对象类型。
        classes -- 游戏对象类的列表，这些类将被用于创建游戏对象。

        此方法将通用变量与类进行映射，以便在创建游戏对象时根据通用变量快速找到对应的类。
        """
        # 通过字典推导式将通用变量与对应的类进行映射
        self.game_classes={common_variable: class_ for common_variable, class_ in zip(common_variables, classes)}

    def create_game_object(self, common_variable,*args,**kwargs):
        """
        根据指定的通用变量创建游戏对象。

        参数:
        common_variable -- 用于标识游戏对象类型的通用变量。
        *args -- 传递给游戏对象构造函数的位置参数。
        **kwargs -- 传递给游戏对象构造函数的关键字参数。

        返回:
        返回创建的游戏对象实例。

        此方法根据通用变量找到对应的类，并使用提供的参数创建该游戏对象实例。
        """
        # 根据通用变量获取对应的游戏对象类
        cls=self.game_classes[common_variable]
        # 使用提供的参数创建游戏对象实例
        return cls(*args,**kwargs)
class State():
    def __init__(self,state_type):
        self.state=state_type

