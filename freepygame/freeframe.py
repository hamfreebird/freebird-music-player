import pygame
import pygame.draw
import pygame.colordict
from freepygame import freetext
import time

pygame.init()
frame_number = 60
display_size = (720, 480)
pygame.display.set_caption("freebird application")
pygame.display.set_icon(pygame.image.load("assets\\freebird_music.ico"))
screen = pygame.display.set_mode(display_size, pygame.DOUBLEBUF | pygame.HWSURFACE)
screen.fill(pygame.colordict.THECOLORS.get("grey0"))
buffer = pygame.Surface(display_size)
clock = pygame.time.Clock()

event_text = freetext.SuperText(screen, [3, 5], "", "assets\\simhei.ttf", size = 10,
	                                color = pygame.colordict.THECOLORS.get("grey70"))

while True:
    event_text.set_msg("现在时间：" + str(time.localtime().tm_year) + "年 " + str(time.localtime().tm_mon) + "月 " +
	                   str(time.localtime().tm_mday) + "日 " + str(time.localtime().tm_hour) + "时 " +
					   str(time.localtime().tm_min) + "分 " + str(time.localtime().tm_sec) + "秒   " +
					   "当前帧速率 " + str(int(clock.get_fps())) + "     Copyright (c) 2023 freebird")
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
    event_text.draw()
    pygame.display.flip()
    screen.fill(pygame.colordict.THECOLORS.get("grey0"))
    clock.tick(frame_number)
