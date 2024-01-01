"""free frame v1.0"""

import time
import pygame
from pygame.colordict import THECOLORS       # pygame的颜色列表
from freepygame import freetext, freebutton, freecircle

display_set = {
        "fps": 60,
        "size": (720, 480),
        "title": "freepygame",
        "icon": None
    }

class Main:
    
    def __init__(self, setting: dict | None):
        self.set = setting
        if self.set is None:
            self.set = display_set
        self.screen = None
        self.clock = None
        self._go = True
    
    # noinspection PyAttributeOutsideInit
    def element(self):
        self.event_text = freetext.SuperText(self.screen, [3, 5], "", size=10, color=THECOLORS.get("grey30"))
        self.text = [self.event_text]
        self.button = []
        
    def _run(self):
        pygame.init()
        pygame.display.set_caption(self.set.get("title"))
        if self.set.get("icon") is not None:
            pygame.display.set_icon(self.set.get("icon"))
        self.screen = pygame.display.set_mode(self.set.get("size"))
        self.clock = pygame.time.Clock()
        self.element()
        
    def run(self):
        if self._go is True:
            self._run()
        while True:
            self.event_text_set()
            self.event()
            self.draw()
            pygame.display.flip()
            self.clock.tick(self.set.get("fps"))
            self.screen.fill(THECOLORS.get("grey100"))
            
    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                
    def draw(self):
        for unit in self.text:
            unit.draw()
        for unit in self.button:
            unit.draw()
            
    def event_text_set(self):
        try:
            self.event_text.set_msg(
                "现在时间：" + str(time.localtime().tm_year) + "年 " + str(time.localtime().tm_mon) + "月 " + str(
                    time.localtime().tm_mday) +
                "日 " + str(time.localtime().tm_hour) + "时 " + str(time.localtime().tm_min) + "分 " + str(
                    time.localtime().tm_sec) + "秒")
        except NameError:
            pass


# noinspection PyAttributeOutsideInit
class App(Main):
    def element(self):
        self.event_text = freetext.SuperText(self.screen, [3, 5], "", "assets\\simhei.ttf", size=10,
                                             color=THECOLORS.get("grey30"))
        self.text = [self.event_text]
        self.button = []
        
if __name__ == "__main__":
    app = App(None)
    app.run()
        
