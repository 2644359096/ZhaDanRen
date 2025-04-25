import pygame, sys
# from 代码.game_timer import KeyTimer
import pygame_gui

pygame.init()
screen_size = (800, 600)
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
# key_timers={
#         pygame.K_j:KeyTimer(pygame.K_j,50,500),
#     }
list1=[]
a=0
for i in range(4):
    a += 1
    list1.insert(i, a)
print(list1)
manege = pygame_gui.UIManager(screen_size)

rongqi = pygame_gui.core.UIContainer(pygame.Rect((0, 0), (400, 200)), manege)
anniu = pygame_gui.elements.UIButton(pygame.Rect((0, 0), (40, 20)), '容器内按钮', manege, rongqi,allow_double_clicks=True)

gundongtiao=pygame_gui.elements.UIScrollingContainer(pygame.Rect((50, 50), (300, 300)),manege,container=rongqi,allow_scroll_y=True)
# huakuaitiao=pygame_gui.elements.UIHorizontalSlider(pygame.Rect((50, 50), (100, 20)),100,(0,100),manege,gundongtiao)
# huakuai=pygame_gui.elements.UIHorizontalScrollBar(pygame.Rect((50, 100), (200, 50)),0.1,manege,gundongtiao)
def print_button(data):
    print(f'button is process,data is {data}')
anniu.bind(pygame_gui.UI_BUTTON_DOUBLE_CLICKED,print_button)
while True:
    dt = clock.tick(60) / 1000
    screen.fill('white')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        manege.process_events(event)

    # key_status=key_timers[pygame.K_j].gat_key_status()
    #
    # if key_status==KeyTimer.KEY_SHORT:
    #     print('短按')
    # if key_status==KeyTimer.KEY_LONG:
    #     print('长按')
    #
    # for key_timer in key_timers.values():
    #     key_timer.update()
    manege.update(dt)

    manege.draw_ui(screen)
    pygame.display.update()
