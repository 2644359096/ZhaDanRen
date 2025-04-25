import pygame,random
from setting import *
from support import *
from queue import PriorityQueue
from props import *
from player import Player
from sprites import PathLine
from gamemaps import GameMap
from game_timer import Timer


class Enemy(Player):
    def __init__(self,pos, role,player,group, collision_sprites, gmap:GameMap, z=LAYERS['主层']):
        super().__init__(pos,role, group,collision_sprites, gmap,z)
        self.player=player
        self.current_action=ZUO
        self.current_direction=self.current_action
        self.current_pos=self.pos
        self.map_elemenl = PLAYER2
        self.path_sprites=pygame.sprite.Group()
        self.speed=60
        self.costs={}
        self.path_lines=[]
        self._actions={
            SHANG: (0,-1),
            XIA:(0,1),
            ZUO: (-1,0),
            YOU: (1,0),
            ZHAN:(0,0)
        }
        self.timers = {
            'drop_bombs': Timer(200, self.drop_boobs),
            'start_move':Timer(500),
            'update_path':Timer(250)
        }
        self.timers['start_move'].start()
        self.timers['update_path'].start()
    def __get_action_delta(self,action) -> tuple[int]:
        return self._actions.get(action,ZHAN)

    def get_face(self):
        if self.current_action!=ZHAN:
            self.directions=self.current_action

    def is_walkable(self,pos,walk_type,flag=PIXELPOS):
        if flag==PIXELPOS:
            return self.gmap.get_map_elemenl(self.gmap.conversion_pos(pos,GMAPPOS)) == walk_type
        elif flag==GMAPPOS:
            return self.gmap.get_map_elemenl(pos) == walk_type


    def move(self,dt):
        if not self.timers['start_move'].active:
            self.auto_action()
            if self.current_action:
                if self.current_pos:
                    # 走完当前节点才能转弯
                    if is_range_equal((3,3),  self.rect.topleft, self.current_pos):
                        self.current_direction = self.current_action
                        self.direction.xy=self.__get_action_delta(self.current_direction)
            super().move(dt)



    def auto_action(self):

        # 获取 A* 路径
        paths = self.get_a_star_path()
        if paths:
            # 获取下一个方向
            directions = self.get_direction(paths)
            if directions:
                    self.current_action=directions[0]
                    self.current_pos=self.gmap.conversion_pos(paths[0],PIXELPOS)
            else:
                # 如果没有方向，则停止移动
                self.current_action = ZHAN
        else:
            # 如果没有路径，则停止移动
            self.current_action = ZHAN
    # 否则，继续沿当前方向移动

    @staticmethod
    def heuristic(a, b) -> float:
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)

    def a_star_search(self,start, goal):
        frontier = PriorityQueue()
        frontier.put((0,start))
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while not frontier.empty():
            _,current= frontier.get()
            if current == goal:
                break

            for next in self.get_neighbors(current):
                new_cost = cost_so_far[current] + self.cost(current, next)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.heuristic(goal,next)
                    frontier.put((priority,next))
                    came_from[next] = current

        return came_from, cost_so_far

    def get_neighbors(self, pos):
        """获取可行走的邻居节点"""
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            x = pos[0] + dx
            y = pos[1] + dy
            if self.is_walkable((x, y), ROAD,GMAPPOS) or self.is_walkable((x,y),PLAYER1,GMAPPOS) or self.is_walkable((x,y),PLAYER2,GMAPPOS):
                neighbors.append((x, y))


        return neighbors

    def cost(self, from_node, to_node) -> float:
        return self.costs.get(to_node,1)

    @staticmethod
    def reconstruct_path(came_from, start, goal):
        current= goal
        path = []
        if goal not in came_from:  # 未找到路径
            return []
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start)  # optional
        path.reverse()  # optional
        return path
    def get_a_star_path(self):
        # 获取玩家位置和当前敌人位置
        start_pos = self.gmap.conversion_pos(self.pos, GMAPPOS)
        glob_pos = self.gmap.conversion_pos(self.player.pos, GMAPPOS)
        # 寻找路径
        came_from, cost = self.a_star_search(start_pos, glob_pos)
        path = self.reconstruct_path(came_from, start=start_pos, goal=glob_pos)
        return path

    def path_update(self):
        if not self.timers['update_path'].active:
            self.timers['update_path'].start()
            self.draw_a_star_path(self.get_a_star_path())

    def draw_a_star_path(self,paths):
        self.group.remove(self.path_sprites.sprites())
        self.path_sprites.empty()
        if not paths:
            return
        for direction,path in zip(self.get_direction(paths),paths[1:-1]):
            PathLine(self.gmap.conversion_pos(path,PIXELPOS),'../游戏素材/ui/主界面/箭头样式',direction,[self.group,self.path_sprites],self.gmap,map_elemenl=ROAD,z=LAYERS['上层'])
    @staticmethod
    def get_direction(paths):
        directions = []
        for i in range(len(paths) - 1):
            current_pos = paths[i]
            next_pos = paths[i + 1]
            dx = next_pos[0] - current_pos[0]
            dy = next_pos[1] - current_pos[1]
            if dx > 0:
                directions.append(YOU)
            elif dx < 0:
                directions.append(ZUO)
            elif dy > 0:
                directions.append(XIA)
            elif dy < 0:
                directions.append(SHANG)
        return directions
    def update(self, dt):
        self.gmap_update()
        if self.status != DEAD:
            self.get_face()
            self.get_status()
            self.move(dt)
            self.props_effect()
            self.path_update()
            self.timer_update()
            self.apply_props()
        self.animate(dt)