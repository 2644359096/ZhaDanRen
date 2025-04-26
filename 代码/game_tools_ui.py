
import pygame
import typing
import random
from typing import Union, Dict, Tuple, Optional, List, Iterator
from pygame_gui.core.interfaces import IContainerLikeInterface, IUIElementInterface, IUIContainerInterface,IUIManagerInterface
from pygame_gui.core import UIContainer,ObjectID,UIElement
from pygame_gui.elements import  UIImage
from pygame.locals import  *
from .setting import *
from .gamemaps import GameMaps
from .game_timer import Timer
from .support import  DoubleClick




class RollingDisplayContainers(UIContainer):

    def __init__(self,
                 relative_rect: pygame.Rect,
                 manager: Optional[IUIManagerInterface] = None,
                 *,
                 starting_height: int = 1,
                 container: Optional[IContainerLikeInterface] = None,
                 parent_element: Optional[UIElement] = None,
                 object_id: Optional[Union[ObjectID, str]] = None,
                 element_id: Union[List[str], None] = None,
                 anchors: Optional[Dict[str, Union[str, UIElement]]] = None,
                 visible: int = 1,
                 ):

        self.mouse_wheel_y = 0
        self.current_element=None
        self.__copy_current_element=None

        self.start_width=0
        self.elements_interval=0
        self.element_lock=False
        self.locked_element=None
        self.unlock_lost_timer=Timer(2000)
        self.lock_surfaces={
            'lock':pygame.transform.scale(pygame.image.load('./游戏素材/ui/主界面/锁/锁定.png'), (ELEMENT_RECT_WIGHT/3,ELEMENT_RECT_HEIGHT/3)).convert_alpha(),
            'unlock':pygame.transform.scale(pygame.image.load('./游戏素材/ui/主界面/锁/解锁.png'), (ELEMENT_RECT_WIGHT/3,ELEMENT_RECT_HEIGHT/3)).convert_alpha()
        }

        self.double_click_mouse=DoubleClick(DoubleClick.MOUSE,BUTTON_LEFT)

        if element_id is None:
            element_id = ['scrolling_container']
        super().__init__(
            relative_rect=relative_rect,
            manager=manager,
            starting_height=starting_height,
            container=container,
            parent_element=parent_element,
            object_id=object_id,
            element_id=element_id,
            anchors=anchors,
            visible=visible
        )
        self._root_containers=UIContainer(
            relative_rect=relative_rect,
            manager=manager,
            starting_height=starting_height,
            container=container,
            parent_element=parent_element,
            object_id=object_id,
            element_id=element_id,
            anchors=anchors,
            visible=self.visible
        )
        view_rect=pygame.Rect((0,0),self.relative_rect.size)

        self._view_container = GameContainer(
            relative_rect=view_rect,
            manager=manager,
            starting_height=1,
            container=self._root_containers,
            parent_element=parent_element,
            object_id=ObjectID(
                object_id='#scrollable_container',
                class_id=None),
        )


    def draw_lock(self):
        if self.locked_element is not None:

            if self.element_lock:
                self.locked_element.image.blit(self.lock_surfaces['lock'],
                                            dest=(self.locked_element.rect.width/6-self.lock_surfaces['lock'].width/3,
                                                  self.locked_element.rect.height/4-self.lock_surfaces['lock'].height/4))
            elif self.unlock_lost_timer.active:
                self.locked_element.recover_surface()
                self.locked_element.image.blit(self.lock_surfaces['unlock'],
                                   dest=(self.locked_element.rect.width / 6 - self.lock_surfaces['unlock'].width / 3,
                                         self.locked_element.rect.height / 4 - self.lock_surfaces['unlock'].height / 4))
            else:
                self.locked_element.recover_surface()



    def update(self, time_delta: float):
        super().update(time_delta)
        self.get_current_element()
        self.draw_lock()
        self.unlock_lost_timer.update()
        self.double_click_mouse.update()

        self.update_scrolling_container()
    def process_event(self, event: pygame.event.Event) -> bool:
        mouse_status=pygame.mouse.get_pressed(5)
        mouse_pos = pygame.mouse.get_pos()
        header=super().process_event(event)

        #当鼠标处于滚动框内，监听鼠标滚动事件
        if  self._view_container.rect.collidepoint(mouse_pos):
            if event.type == MOUSEWHEEL :
                self.mouse_wheel_y=event.y
        #监听元素是否被锁定
            if  self.double_click_mouse.double_click(event) and not self.element_lock:
                self.locked_element = self.current_element
                self.element_lock=True

            elif  mouse_status[2] and self.element_lock and self.locked_element==self.current_element:
                self.element_lock=False
                self.locked_element=self.current_element
                self.unlock_lost_timer.start()
        elif event.type == ELEMENT_LOCK and not self.element_lock:
            self.locked_element = self.current_element
            self.element_lock = True
        elif event.type == ELEMENT_UNLOCK and self.element_lock and self.locked_element==self.current_element:
            self.element_lock = False
            self.locked_element = self.current_element
            self.unlock_lost_timer.start()
        return header

    def get_mouse_wheel_y(self) -> int:
        mouse_wheel_y=0
        if self.mouse_wheel_y != 0:
            mouse_wheel_y=self.mouse_wheel_y
            self.mouse_wheel_y=0
        else:
            return  self.mouse_wheel_y
        return mouse_wheel_y

    def get_current_element(self) -> UIElement:
        for element in self._view_container.elements:
            if element.rect.centerx == self._view_container.rect.centerx:
                self.current_element=element
                self.__copy_current_element=element
            else:
                self.current_element=self.__copy_current_element

        return self.current_element
    def _compute_scroll_amount(self, element,mouse_wheel_y):
        scroll_amount= element.relative_rect.width*1.5
        self.start_width=mouse_wheel_y* scroll_amount+element.relative_rect.x
    def update_scrolling_container(self):
        mouse_wheel_y=self.get_mouse_wheel_y()
        for element in self._view_container.elements:
            #根据鼠标滚轮移动元素
            self._compute_scroll_amount(element, mouse_wheel_y)
            new_pos=(self.start_width,element.relative_rect.y)
            element.set_relative_position(new_pos)
            # 边界检测与元素重置
            if self.current_element is not None:
                if mouse_wheel_y>0:
                    if element.relative_rect.x>self.current_element.relative_rect.x:
                        element.set_relative_position((element.relative_rect.x-element.relative_rect.width*(len(self._view_container.elements)+2),element.relative_rect.y))
                if  mouse_wheel_y<0:
                    if element.relative_rect.x<self.current_element.relative_rect.x:
                        element.set_relative_position((element.relative_rect.x + element.relative_rect.width * ( len(self._view_container.elements) + 2), element.relative_rect.y))


    def show(self,show_contents: bool = True):
        super().show()
        self._root_containers.show(show_contents=False)


        if self._view_container is not None:
            self._view_container.show(show_contents)
    def hide(self, hide_contents: bool = True):
        if not self.visible:
            return
        self._root_containers.hide(hide_contents=False)
        if self._view_container is not  None:
            self._view_container.hide(hide_contents)
        super().hide()

    def get_container(self) -> IUIContainerInterface:
        return self._view_container

    def __iter__(self) -> typing.Iterator[IUIElementInterface]:
        return iter(self.get_container())

    def __contains__(self, item: IUIElementInterface) -> bool:
        return item in self.get_container()

class GameContainer(UIContainer):
    def __init__(self,
                 relative_rect,
                 manager: Optional[IUIManagerInterface] = None,
                 *,
                 starting_height: int = 1,
                 container: Optional[IContainerLikeInterface] = None,
                 parent_element: Optional[UIElement] = None,
                 object_id: Optional[Union[ObjectID, str]] = None,
                 anchors: Optional[Dict[str, Union[str, UIElement]]] = None,
                 visible: int = 1):
        super().__init__(
            relative_rect=relative_rect,
            manager=manager,
            starting_height=starting_height,
            container=container,
            parent_element=parent_element,
            object_id=object_id,
            anchors=anchors,
            visible=visible
        )


    def add_element(self, element: IUIElementInterface):
        element.set_relative_position((element.relative_rect.x + element.relative_rect.width, element.relative_rect.y))
        super().add_element(element)

class GameThumbnail(UIImage):
    def __init__(self,
                 relative_rect,
                 thumbnail_name:str,
                 thumbnail_surface: pygame.surface.Surface,
                 manager: Optional[IUIManagerInterface] = None,
                 image_is_alpha_premultiplied: bool = False,
                 container: Optional[IContainerLikeInterface] = None,
                 parent_element: Optional[UIElement] = None,
                 object_id: Optional[Union[ObjectID, str]] = None,
                 anchors: Optional[Dict[str, Union[str, UIElement]]] = None,
                 visible: int = 1,
                 *,
                 starting_height: int = 1,
                 scale_func=pygame.transform.smoothscale):
        self.thumbnail_name=thumbnail_name
        super().__init__(
            relative_rect=relative_rect,
            image_surface=thumbnail_surface,
            manager=manager,
            image_is_alpha_premultiplied=image_is_alpha_premultiplied,
            container=container,
            parent_element=parent_element,
            object_id=object_id,
            anchors=anchors,
            visible=visible,
            starting_height=starting_height,
            scale_func=scale_func
        )
        self.__copy_image=thumbnail_surface.convert_alpha()
    def recover_surface(self,image_is_alpha_premultiplied: bool = False,scale_func = pygame.transform.smoothscale):
        self.set_image(self.__copy_image,image_is_alpha_premultiplied,scale_func)



class GameDynamicDiagrams(UIImage):
    def __init__(self,
                 relative_rect,
                 animate_frames,
                 manager: Optional[IUIManagerInterface] = None,
                 image_is_alpha_premultiplied: bool = False,
                 container: Optional[IContainerLikeInterface] = None,
                 parent_element: Optional[UIElement] = None,
                 object_id: Optional[Union[ObjectID, str]] = None,
                 anchors: Optional[Dict[str, Union[str, UIElement]]] = None,
                 visible: int = 1,
                 *,
                 starting_height: int = 1,
                 scale_func=pygame.transform.smoothscale):
        super().__init__(
            relative_rect=relative_rect,
            image_surface=animate_frames[0],
            manager=manager,
            image_is_alpha_premultiplied=image_is_alpha_premultiplied,
            container=container,
            parent_element=parent_element,
            object_id=object_id,
            anchors=anchors,
            visible=visible,
            starting_height=starting_height,
            scale_func=scale_func
        )
        self.animate_frames=animate_frames
        self.frames_index=0

    def set_animate_frames(self,animate_frames):
        if animate_frames!=self.animate_frames:
            self.animate_frames=animate_frames
    def animate(self,dt):
        self.frames_index+=3.5*dt
        if self.frames_index>=len(self.animate_frames):
            self.frames_index=0
        self.image=pygame.transform.scale(self.animate_frames[int(self.frames_index)],self.relative_rect.size)
    def update(self, time_delta: float):
        self.animate(time_delta)
        super().update(time_delta)

class SelectMapListTool():
    def __init__(self,maps):
        self.gmaps={}

        # 加载所有地图
        gmaps = GameMaps(maps)
        self.gmap_objects = {k: gmaps.use_map(k) for k in GMAPS.keys()}
        print(self.gmap_objects)

    def load_maps(self,map_element_images:dict[int,str]):
        for gmap_name,gmap_object in self.gmap_objects.items():
            gmap_surface=pygame.Surface((gmap_object.map_shape()[0]*PIXELSIZE,gmap_object.map_shape()[1]*PIXELSIZE))
            gmap_list=gmap_object.init_pixle_map()

            gmap_elements = []
            for map_element, element_pos in gmap_list:
                    image_path=map_element_images[map_element]
                    gmap_elements.append((pygame.transform.scale(random.choice(import_folder(image_path)), (PIXELSIZE, PIXELSIZE)).convert_alpha(),element_pos))
            gmap_surface.fblits(gmap_elements)

            self.gmaps[gmap_name]=gmap_surface

    def draw_map(self,map_name,draw_surface:pygame.Surface):
        draw_rect=draw_surface.get_rect()
        draw_surface.blit(pygame.transform.scale(self.gmaps[map_name],draw_rect.size),draw_rect)

