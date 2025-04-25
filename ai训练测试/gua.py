import time

import  pygetwindow as gw
import  pyautogui as pg
window_anyVPN=gw.getWindowsWithTitle("Any VPN")[0]




button_pos=window_anyVPN.centerx,window_anyVPN.centery-40

while True:
    window_anyVPN.activate()
    time.sleep(0.5)
    pg.click(button_pos)
    time.sleep(119)


