import pygame


class Timer():
    def __init__(self, dealy_time, func=None):
        self.dealy_time = dealy_time
        self.func = func

        self.start_time = 0
        self.active = False

    def start(self):
        self.active = True
        self.start_time = pygame.time.get_ticks()

    def stop(self):
        self.active = False
        self.start_time = 0

    def update(self):
        current_time1 = pygame.time.get_ticks()
        if current_time1 - self.start_time >= self.dealy_time:
            if self.start_time!=0:
                if self.func:
                    self.func()
            self.stop()

class KeyTimer():
    KEY_LONGING='长按中'
    KEY_SHORT='短按'
    KEY_LONG='长按'
    KEY_NOT_PRESSED='未按'

    def __init__(self,key,min_time,max_time):
        self.__key_pressed_time=0
        self.__dealy_time=0
        self.__key_max_time=max_time
        self.__key_min_time=min_time
        self.__first_logged=False
        self.__last_logged= False
        self.__key=key

    def gat_key_status(self):
        keys = pygame.key.get_pressed()
        if self.__first_logged and not self.__last_logged:
            if self.__key_min_time <= self.__dealy_time <=self.__key_max_time:
                if keys[self.__key]:
                    return '长按中'
                else:
                    self.__last_logged = True
                    return '短按'
            elif self.__dealy_time >=self.__key_max_time:
                self.__last_logged = True
                return '长按'
        return '未按'

    def update(self):
        keys = pygame.key.get_pressed()
        current_time=pygame.time.get_ticks()
        if keys[self.__key] and not self.__first_logged:
            self.__first_logged = True
            self.__key_pressed_time = current_time
        if self.__first_logged:
            self.__dealy_time=current_time-self.__key_pressed_time
            if not keys[self.__key]:
                self.__first_logged = False
                self.__last_logged=False
                self.__dealy_time=0

