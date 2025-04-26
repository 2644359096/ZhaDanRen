import pygame
from queue import Queue
from .generic import BaseUIState,BaseEnemyState
from .game_core_ui import *

class StateMachine:
    """状态机"""
    def __init__(self):
        self.states={}
        self.current_state=None
        self.__data_queue=Queue(1)

    def add_state(self,state_name,state_class,*args,**kwargs):
        """添加状态到状态机"""
        self.states[state_name] = (state_class,(self, *args, *kwargs))
    def add_states(self,state_configs:dict):
        for state_name,(state_class,args) in state_configs.items():
            self.states[state_name] = (state_class,(self, *args))
    def set_state(self,state_name):
        """切换到指定状态"""
        if self.current_state:
            self.current_state.exit()  # 退出当前状态
        self.current_state = self.states.get(state_name)[0](*self.states.get(state_name)[1])
        if self.current_state:
            self.current_state.enter()  # 进入新状态
    def set_data(self,data):
        self.__data_queue.put_nowait(data)
    def get_data(self):
        if not self.__data_queue.empty():
            return self.__data_queue.get_nowait()
        return

    def update(self, delta_time):
        """更新当前状态逻辑"""
        if self.current_state:
            self.current_state.update(delta_time)

    def process_event(self, event):
        """分发事件到当前状态"""
        harder=False
        if self.current_state:
            harder=self.current_state.process_event(event)
        return harder
class EnemyFSM:
    def __init__(self, ai):
        self.states = {}
        self.current_state = None
        self.ai = ai

    def add_state(self, state):
        self.states[state.__class__.__name__] = state

    def switch_state(self, new_state_class):
        if self.current_state:
            self.current_state.exit()
        self.current_state = self.states[new_state_class.__name__]
        self.current_state.enter()

    def update(self, delta_time):
        if self.current_state:
            self.current_state.update(delta_time)

class StartUIState(BaseUIState):
    def __init__(self, state_machine,display_surface,manager,title_surface):
        super().__init__(state_machine,display_surface,manager)
        self.title_surface=title_surface
        self.ui_window=self.start_window=StartWindow(self.display_rect, self.title_surface, self.get_start_window_layout(), self.manager)
    def get_start_window_layout(self):
        #布局
        #开始标题矩形
        default_start_title_rect=pygame.Rect((0,0),START_TITLE_SURFACE_SIZE)
        default_start_title_rect.centerx=self.display_rect.centerx
        default_start_title_rect.centery=self.display_rect.centery-200
        #开始游戏按钮矩形
        default_start_game_button_rect=pygame.Rect((0, 0), START_BUTTON_SURFACE_SIZE)
        default_start_game_button_rect.centerx=self.display_rect.centerx
        default_start_game_button_rect.centery = self.display_rect.centery
        #设置按钮
        default_setting_button_rect = pygame.Rect((0, 0), START_BUTTON_SURFACE_SIZE)
        default_setting_button_rect.centerx = self.display_rect.centerx
        default_setting_button_rect.centery = default_start_game_button_rect.centery+100
        #关于我们按钮矩形
        default_about_us_button_rect = pygame.Rect((0, 0), START_BUTTON_SURFACE_SIZE)
        default_about_us_button_rect.centerx = self.display_rect.centerx
        default_about_us_button_rect.centery = default_setting_button_rect.centery + 100
        #退出游戏按钮矩形
        default_exit_game_button_rect = pygame.Rect((0, 0), START_BUTTON_SURFACE_SIZE)
        default_exit_game_button_rect.centerx = self.display_rect.centerx
        default_exit_game_button_rect.centery = default_about_us_button_rect.centery + 100

        start_window_layout= {
            'start_title_rect': default_start_title_rect,
            'start_game_button':default_start_game_button_rect,
            'setting_button':default_setting_button_rect,
            'about_us_button':default_about_us_button_rect,
            'exit_game_button':default_exit_game_button_rect
        }
        return start_window_layout

    def process_event(self, event):
        header=super().process_event(event)
        if event.type==UI_START:
            self.state_machine.set_state('main')

        return header

class MainUIState(BaseUIState):
    def __init__(self, state_machine,display_surface,manager,roles):
        super().__init__(state_machine,display_surface,manager)
        self.roles=roles
        self.ui_window = MainWindow(self.display_rect, self.manager, self.get_main_layout(self.roles))
        self.ui_window.disable()
        self.ui_window.hide()
    def get_main_layout(self, role_list: list):
        # 布局
        # 顶部标题矩形
        default_top_label_rect = pygame.Rect((0, 0), (self.display_rect.width // 3, self.display_rect.height // 7))
        default_top_label_rect.centerx = self.display_rect.centerx
        default_top_label_rect.midtop = self.display_rect.midtop
        default_top_label_str1 = "选择人物"
        default_top_label_str2 = "选择地图"
        # 大型动态图矩形
        default_large_dynamic_diagrams_rect = pygame.Rect((0, 0),
                                                          (self.display_rect.width // 4, self.display_rect.height // 2))
        default_large_dynamic_diagrams_rect.centerx = self.display_rect.centerx
        default_large_dynamic_diagrams_rect.top = default_top_label_rect.bottom + 50
        # 可滑动缩略图容器矩形
        default_swipes_container_rect = pygame.Rect((0, 0), (450, default_top_label_rect.height))
        default_swipes_container_rect.centerx = self.display_rect.centerx
        default_swipes_container_rect.top = default_large_dynamic_diagrams_rect.bottom + 25
        # 缩略图矩形
        # 缩略图大小矩形(固定)
        default_thumbnail_rect = pygame.Rect((0, 0), (
        default_swipes_container_rect.width // 3, default_swipes_container_rect.height))
        # 缩略图y轴位置(固定)
        default_thumbnail_rect.centery = default_swipes_container_rect.height // 2
        # 缩略图初始x轴位置
        default_thumbnail_rect.x = 0
        # 角色缩略图矩形字典
        role_thumbnail_rects = {}
        # 根据角色数量增加缩略图
        for role in role_list:
            # 根据角色映射字典，值为缩略图矩形，缩略图图像
            role_thumbnail_rects[role] = pygame.Rect(default_thumbnail_rect), pygame.transform.scale(
                pygame.image.load(f'./游戏素材/人物/人物行为/{role}/下_站/{role}_站_下_01.png'),
                (default_swipes_container_rect.width // 3, default_swipes_container_rect.height))
            # 每隔一个缩略图增加半个个身位距离150*4
            default_thumbnail_rect.x += default_thumbnail_rect.width * 1.5
        # 主页面第一部分按钮(锁定，下一步，解锁)矩形
        default_main_once_button = pygame.Rect((0, 0), (
        default_swipes_container_rect.height - 10, default_top_label_rect.height // 2))
        # 主页第一部分按钮y轴定位
        default_main_once_button.top = default_swipes_container_rect.bottom + 25
        default_main_once_button.left = default_swipes_container_rect.left

        default_once_button_rects = {}
        default_once_button_strs = ['锁定', '下一步', '解锁']
        for once_button_str in default_once_button_strs:
            default_once_button_rects[once_button_str] = pygame.Rect(default_main_once_button)
            default_main_once_button.centerx += default_main_once_button.width * 2

        # 主页第二部分选择地图部件的容器矩形
        default_map_main_container_rect = pygame.Rect((0, 0), (SCREENWIDTH - 100, SCREENHEIGHT - 150))
        # 容器矩形定位
        default_map_main_container_rect.x += 50

        default_map_main_container_rect.y += 100

        # 地图选择列表相对矩形
        default_map_select_list_relative_rect = pygame.Rect((10, 10),
                                                            (200, default_map_main_container_rect.height - 20))
        # 地图选择列表字符串列表
        default_map_select_list_strs = GMAPS.keys()

        # 地图全貌展示图矩形
        default_map_full_image_rect = pygame.Rect((0, 10), (
        default_map_main_container_rect.width - default_map_select_list_relative_rect.width - 90,
        default_map_select_list_relative_rect.height))
        # 地图全貌展示图矩形定位
        default_map_full_image_rect.x = default_map_select_list_relative_rect.right + 70

        # 主页面第二部分按钮(上一步，确定)矩形
        default_main_twice_button = pygame.Rect((0, 0), (
        default_swipes_container_rect.height - 10, default_top_label_rect.height // 2))
        # 主页第二部分按钮y轴定位
        default_main_twice_button.top = default_swipes_container_rect.bottom + 25
        default_main_twice_button.left = default_swipes_container_rect.left

        default_twice_button_rects = {}
        default_twice_button_strs = ['上一步', "确定"]
        for twice_button_str in default_twice_button_strs:
            default_twice_button_rects[twice_button_str] = pygame.Rect(default_main_twice_button)
            default_main_twice_button.centerx += default_main_twice_button.width * 4

        main_layout = {
            'top_label': {
                'label': default_top_label_rect,
                'texts': (default_top_label_str1, default_top_label_str2)
            },
            'large_dynamic_diagrams_rect': default_large_dynamic_diagrams_rect,
            'swipes_container_rect': default_swipes_container_rect,
            'role_thumbnail_rects': role_thumbnail_rects,
            'once_buttons': default_once_button_rects,

            "map_main_container_rect": default_map_main_container_rect,
            'map_select_list': {
                'relative_rect': default_map_select_list_relative_rect,
                'strs': default_map_select_list_strs
            },
            'map_full_image_rect': default_map_full_image_rect,
            'twice_buttons': default_twice_button_rects
        }
        return main_layout

    def enter(self):
        self.ui_window.show()
        self.ui_window.change_main_screen('once')
        self.ui_window.enable()

    def process_event(self, event):
        header=super().process_event(event)
        if event.type==UI_START_GAME:
            data={
                'role_name':event.role_name,
                'map_name':event.map_name
            }
            self.state_machine.set_data(data)
            self.state_machine.set_state('game')

        return header

class GameUIState(BaseUIState):
    def __init__(self, state_machine,display_surface,manager,game):
        super().__init__(state_machine,display_surface,manager)
        self.data=self.state_machine.get_data()
        self.game=game(self.data)
        self.ui_window=GameWindow(self.display_rect,self.manager,self.get_game_layout(),self.game)
        self.ui_window.disable()
        self.ui_window.hide()
    def get_game_layout(self):
        game_screen_size=self.game.get_game_rect_size()
        # 顶部容器矩形
        default_top_container_rect = pygame.Rect((0, 0), (self.display_rect.width, (self.display_rect.height-game_screen_size[1])/2))
        # ----容器内元素-----


        # ----容器内元素-----

        #游戏屏幕矩形
        default_game_screen_rect=pygame.Rect((0, 0), game_screen_size)
        #游戏屏幕矩形定位
        default_game_screen_rect.midtop=default_top_container_rect.midbottom

        # 底部容器矩形
        default_bottom_container_rect = pygame.Rect((0, 0), (self.display_rect.width, (self.display_rect.height-game_screen_size[1])/2))
        #底部容器矩形定位
        default_bottom_container_rect.midtop=default_game_screen_rect.midbottom
        # ----容器内元素-----



        # ----容器内元素-----

        #左上角玩家信息容器矩形
        default_player_info_topleft_container_rect=pygame.Rect((0, 0),
                                                               ((self.display_rect.width-game_screen_size[0])/2,
                                                                game_screen_size[1]/2))
        #左上角玩家信息容器矩形定位
        default_player_info_topleft_container_rect.topright=default_game_screen_rect.topleft
        # ----容器内元素-----

        # ----容器内元素-----

        # 左下角玩家信息容器矩形
        default_player_info_bottomleft_container_rect = pygame.Rect((0, 0),
                                                                    ((self.display_rect.width - game_screen_size[0]) / 2,
                                                                  game_screen_size[1] / 2))
        # 左下角玩家信息容器矩形定位
        default_player_info_bottomleft_container_rect.midtop = default_player_info_topleft_container_rect.midbottom
        # ----容器内元素-----

        # ----容器内元素-----

        # 右上角玩家信息容器矩形
        default_player_info_topright_container_rect = pygame.Rect((0, 0),
                                                                  ((self.display_rect.width - game_screen_size[0]) / 2,
                                                                 game_screen_size[1]/ 2))

        # 右上角玩家信息容器矩形定位
        default_player_info_topright_container_rect.topleft=default_game_screen_rect.topright
        # ----容器内元素-----

        # ----容器内元素-----


        # 右下角玩家信息容器矩形
        default_player_info_bottomright_container_rect = pygame.Rect((0, 0),
                                                                     ((self.display_rect.width - game_screen_size[0]) / 2,
                                                                   game_screen_size[1]/ 2))
        # 右下角玩家信息容器矩形定位
        default_player_info_bottomright_container_rect.midtop=default_player_info_topright_container_rect.midbottom
        # ----容器内元素-----

        # ----容器内元素-----

        game_layout={
            'top_container':{
                'rect':default_top_container_rect,
                'elements':{}
            },
            'game_screen':default_game_screen_rect,
            'bottom_container':{
                'rect':default_bottom_container_rect,
                'elements':{}
            },
            'player_info_topleft_container': {
                'rect': default_player_info_topleft_container_rect,
                'elements': {}
            },
            'player_info_bottomleft_container': {
                'rect': default_player_info_bottomleft_container_rect,
                'elements': {}
            },
            'player_info_topright_container': {
                'rect': default_player_info_topright_container_rect,
                'elements': {}
            },
            'player_info_bottomright_container': {
                'rect': default_player_info_bottomright_container_rect,
                'elements': {}
            }
        }
        return game_layout

    def process_event(self, event):
        header=super().process_event(event)
        return header
    def update(self, delta_time):
        data=self.state_machine.get_data()
        if data:
            self.game

class PatrolState(BaseEnemyState):
    def update(self, delta_time):
        # 巡逻逻辑：随机移动或预设路径
        if self.get_player_distance() < CHASE_DISTANCE:
            self.state_machine.switch_state(ChaseState)
        # 检查危险区域切换状态
        elif self.get_danger_zones():
            self.state_machine.switch_state(AvoidState)
        # 其他巡逻逻辑...

    def calculate_weights(self):
        # 巡逻时的权重计算（可选）
        pass

class ChaseState(BaseEnemyState):
    def update(self, delta_time):
        # 追击玩家逻辑
        target_pos = self.ai.player.pos
        move_dir = target_pos - self.ai.pos
        # 根据move_dir移动
        # 检查危险区域优先级
        if self.get_danger_zones():
            self.state_machine.switch_state(AvoidState)
        # 距离过远时返回巡逻
        if self.get_player_distance() > CHASE_DISTANCE * 1.5:
            self.state_machine.switch_state(PatrolState)

    def calculate_weights(self):
        # 优先朝玩家方向移动，降低危险权重
        pass

class AvoidState(BaseEnemyState):
    def update(self, delta_time):
        # 避开危险区域逻辑
        danger_zones = self.get_danger_zones()
        safe_path = self.ai.find_safe_path(danger_zones)
        if safe_path:
            self.ai.move_along(safe_path)
        # 危险解除后返回之前状态
        if not danger_zones:
            self.state_machine.switch_state(PatrolState)

    def calculate_weights(self):
        # 提高危险区域权重，寻找安全路径
        pass

