import pygame
from pygame import Event

from generic import BaseContainer
from setting import *
from pygame_gui._constants import UI_BUTTON_PRESSED,UI_SELECTION_LIST_NEW_SELECTION
from pygame_gui.core import ObjectID, UIContainer
from game_tools_ui import RollingDisplayContainers,GameThumbnail,GameDynamicDiagrams,SelectMapListTool
from pygame_gui.elements import UIImage, UIButton, UILabel, UISelectionList


#开始界面
class StartWindow(BaseContainer):
    def __init__(self, display_surface_rect, title_surface, layout, manager):
        super().__init__(display_surface_rect,manager ,layout)
        start_title_image = title_surface
        start_title_rect = layout['start_title_rect']
        self.buttons={}
        buttons_themes_class_id="@start_buttons"
        self.start_title = UIImage(
            relative_rect=start_title_rect,
            image_surface=start_title_image,
            manager=manager,
            container=self,
            parent_element=self
        )
        for k,v in layout.items():
            if k != 'start_title_rect':
                self.buttons[k]=UIButton(
            relative_rect=v,
            text='',
            manager=manager,
            container=self,
            object_id=ObjectID(
                class_id=buttons_themes_class_id,
                object_id="#"+k
            ),
            parent_element=self
        )
    def process_event(self, event: pygame.event.Event):
        harder=super().process_event(event)

        if event.type==UI_BUTTON_PRESSED:
            #开始游戏
            if event.ui_element==self.buttons["start_game_button"]:
                pygame.event.post(Event(UI_START))
                print("开始游戏")
            if event.ui_element == self.buttons["setting_button"]:
                pygame.event.post(Event(UI_SETTING))
                print("游戏设置")
            if event.ui_element == self.buttons["about_us_button"]:
                pygame.event.post(Event(UI_ABOUT))
            if event.ui_element == self.buttons["exit_game_button"]:
                pygame.event.post(Event(UI_EXIT))
                print('退出游戏')

        return harder
#主界面
class MainWindow(BaseContainer):
    def __init__(self, relative_rect,manager,layout):
        self.smlt=SelectMapListTool(GMAPS)
        map_element_images={
            ROAD:'../游戏素材/路',
            UNBREAKABLEWALL:'../游戏素材/墙/不可破坏墙',
            BREAKABLEWALL:'../游戏素材/墙/可破坏墙',
            PLAYER1:'../游戏素材/ui/主界面/箭头样式',
            PLAYER2:'../游戏素材/ui/主界面/箭头样式',
            PLAYER3:'../游戏素材/ui/主界面/箭头样式',
            PLAYER4:'../游戏素材/ui/主界面/箭头样式',
        }
        self.smlt.load_maps(map_element_images)
        super().__init__(relative_rect, manager,layout)
        #第一部分布局
        top_label_rect=layout['top_label']['label']
        self.__top_label_str1 = layout['top_label']['texts'][0]
        self.__top_label_str2 = layout['top_label']['texts'][1]
        large_dynamic_diagrams_rect=layout['large_dynamic_diagrams_rect']
        swipes_container_rect=layout['swipes_container_rect']
        role_thumbnail_rects=layout['role_thumbnail_rects']
        once_buttons=layout['once_buttons']

        #第二部分布局
        map_main_container_rect=layout['map_main_container_rect']
        map_select_list_relative_rect=layout['map_select_list']['relative_rect']
        map_select_list_strs=layout['map_select_list']['strs']
        map_full_image_rect=layout['map_full_image_rect']
        twice_buttons=layout['twice_buttons']

        #第一部分元素
        self.top_label=UILabel(
            relative_rect=top_label_rect,
            text=self.__top_label_str1,
            manager=manager,
            container=self,
            parent_element=self,
            object_id=ObjectID(
                class_id="@main_labels",
                object_id="#top_label"
            )
        )
        #--------------------------------
        #可滚动容器
        self.swipes_container=RollingDisplayContainers(
                relative_rect=swipes_container_rect,
                manager=manager,
                container=self,
                parent_element=self
        )
        self.role_thumbnails = {}
        # 缩略图
        for role,(role_thumbnail_rect,role_surface) in role_thumbnail_rects.items():
            # print(role_thumbnail_rect)
            self.role_thumbnails[role]=GameThumbnail(
                relative_rect=role_thumbnail_rect,
                thumbnail_name=role,
                thumbnail_surface=role_surface,
                manager=manager,
                container=self.swipes_container,
                parent_element=self
            )
        # 用于动态图插入
        self.animate_frames=import_frames(f'../游戏素材/人物/人物行为/{self.swipes_container.get_current_element().thumbnail_name}/')

        # 大型动态图，用于展示角色
        self.large_dynamic_diagrams = GameDynamicDiagrams(
            relative_rect=large_dynamic_diagrams_rect,
            animate_frames=self.animate_frames,
            manager=manager,
            container=self,
            parent_element=self
        )
        self.once_buttons={}
        for button_str,button_rect in once_buttons.items():
            self.once_buttons[button_str]=UIButton(
                relative_rect=button_rect,
                text=button_str,
                manager=manager,
                container=self,
                parent_element=self
            )

        #第二部分元素
        #存放选择地图部件的容器
        self.map_main_container=BaseContainer(
            relative_rect=map_main_container_rect,
            manager=manager,
            container=self,
            layout=None,
            boundary_width=5,
            boundary_radius=2
        )

        #地图选择列表
        self.map_select_list=UISelectionList(
            relative_rect=map_select_list_relative_rect,
            item_list=map_select_list_strs,
            manager=manager,
            container=self.map_main_container,
            allow_multi_select=False,
            allow_double_clicks=False,
            parent_element=self
        )
        # 地图全貌展示图
        self.map_full_image=GameThumbnail(
            relative_rect=map_full_image_rect,
            thumbnail_name='',
            thumbnail_surface=pygame.Surface(map_full_image_rect.size),
            manager=manager,
            container=self.map_main_container,
            parent_element=self
        )

        self.twice_buttons={}
        for button_str, button_rect in twice_buttons.items():
            self.twice_buttons[button_str] = UIButton(
                relative_rect=button_rect,
                text=button_str,
                manager=manager,
                container=self,
                parent_element=self
            )


        self.change_main_screen('once')

    def process_event(self, event: pygame.event.Event) -> bool:
        harder = super().process_event(event)
        if event.type==UI_BUTTON_PRESSED:
            lock_element_event = pygame.event.Event(ELEMENT_LOCK, {'lock': True})
            unlock_element_event = pygame.event.Event(ELEMENT_UNLOCK, {'unlock': True})
            if event.ui_element==self.once_buttons['锁定']:
                pygame.event.post(lock_element_event)
            elif event.ui_element==self.once_buttons['解锁']:
                pygame.event.post(unlock_element_event)
            elif event.ui_element==self.once_buttons['下一步'] and self.swipes_container.element_lock:
                self.change_main_screen('twice')
            elif event.ui_element==self.twice_buttons['上一步']:
                self.change_main_screen('once')
            elif event.ui_element==self.twice_buttons['确定'] and self.map_select_list.get_single_selection():
                data={
                    'role_name':self.swipes_container.locked_element.thumbnail_name,
                    'map_name':self.map_select_list.get_single_selection()
                }
                pygame.event.post(Event(UI_START_GAME,data))

        if event.type == UI_SELECTION_LIST_NEW_SELECTION:
            if event.ui_element == self.map_select_list:
                self.smlt.draw_map(event.text,self.map_full_image.image)
        return harder
    def change_main_screen(self,screen_type):
        if screen_type=='once':
            self.top_label.set_text(self.__top_label_str1)
            self.map_main_container.hide()
            self.map_main_container.disable()
            list(map(lambda twice_button: twice_button.hide(), self.twice_buttons.values()))
            list(map(lambda twice_button: twice_button.disable(), self.twice_buttons.values()))

            self.swipes_container.show()
            self.swipes_container.enable()
            self.large_dynamic_diagrams.show()
            self.large_dynamic_diagrams.enable()
            list(map(lambda once_button: once_button.show(), self.once_buttons.values()))
            list(map(lambda once_button: once_button.enable(), self.once_buttons.values()))
        elif screen_type=='twice':
            self.top_label.set_text(self.__top_label_str2)
            self.swipes_container.hide()
            self.swipes_container.disable()
            self.large_dynamic_diagrams.hide()
            self.large_dynamic_diagrams.disable()
            list(map(lambda once_button: once_button.hide(), self.once_buttons.values()))
            list(map(lambda once_button: once_button.disable(), self.once_buttons.values()))

            self.map_main_container.show()
            self.map_main_container.enable()
            list(map(lambda twice_button: twice_button.show(), self.twice_buttons.values()))
            list(map(lambda twice_button: twice_button.enable(), self.twice_buttons.values()))
    def update(self, time_delta: float):
        super().update(time_delta)
        self.large_dynamic_diagrams.set_animate_frames(import_frames(f'../游戏素材/人物/人物行为/{self.swipes_container.get_current_element().thumbnail_name}/'))

#设置界面
class SettingContainer(BaseContainer):
    def __init__(self, relative_rect, manager):
        super().__init__(relative_rect, manager, draggable=False)


#游戏界面
class GameWindow(BaseContainer):
    def __init__(self, relative_rect, manager, layout,game):
        super().__init__(relative_rect,manager, layout)
        top_container_rect=layout['top_container']['rect']
        game_screen_rect=layout['game_screen']
        bottom_container_rect=layout['bottom_container']['rect']
        player_info_topleft_container_rect=layout['player_info_topleft_container']['rect']
        player_info_bottomleft_container_rect=layout['player_info_bottomleft_container']['rect']
        player_info_topright_container_rect=layout['player_info_topright_container']['rect']
        player_info_bottomright_container_rect=layout['player_info_bottomright_container']['rect']

        #顶部容器
        self.top_container=BaseContainer(
            relative_rect=top_container_rect,
            manager=manager,
            layout=None,
            container=self,
            boundary_width=2,
            boundary_color=(123,123,123)
        )

        #游戏画面
        self.game_screen = UIImage(
            relative_rect=game_screen_rect,
            image_surface=pygame.Surface(game_screen_rect.size).convert(),
            manager=manager,
            container=self,
            parent_element=self
        )
        #游戏画面导入
        self.game = game
        self.game.set_display_surface(self.game_screen.image)
        self.is_active=False

        #底部容器
        self.bottom_container=BaseContainer(
            relative_rect=bottom_container_rect,
            manager=manager,
            layout=None,
            container=self,
            boundary_width=2,
            boundary_color=(123, 123, 123)
        )

        #左上角玩家信息容器
        self.player_info_topleft_container=BaseContainer(
            relative_rect=player_info_topleft_container_rect,
            manager=manager,
            layout=None,
            container=self,
            boundary_width=2,
            boundary_color=(123, 123, 123)
        )

        #左下角玩家信息容器
        self.player_info_bottomleft_container = BaseContainer(
            relative_rect=player_info_bottomleft_container_rect,
            manager=manager,
            layout=None,
            container=self,
            boundary_width=2,
            boundary_color=(123, 123, 123)
        )

        #右上角玩家信息容器
        self.player_info_topright_container = BaseContainer(
            relative_rect=player_info_topright_container_rect,
            manager=manager,
            layout=None,
            container=self,
            boundary_width=2,
            boundary_color=(123, 123, 123)
        )

        #右下角玩家信息容器
        self.player_info_bottomright_container = BaseContainer(
            relative_rect=player_info_bottomright_container_rect,
            manager=manager,
            layout=None,
            container=self,
            boundary_width=2,
            boundary_color=(123, 123, 123)
        )
    def update(self, time_delta: float):
        super().update(time_delta)
        if self.alive() and self.is_active:
            self.game.update(time_delta)
            self.game.draw()
    def disable(self):
        super().disable()
        self.is_active=False
    def enable(self):
        super().enable()
        self.is_active=True

