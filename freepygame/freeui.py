"""freebird ui"""

import pygame
import pygame.gfxdraw
import pygame.draw

class Ui():
    def __init__(self, size : list | tuple):
        self.size = size
        self.member = {"_main_ui" : [0, None]}
        
    def get(self):
        return self.member
    
    def add(self, member_name, member_number, member_instance):
        self.member[member_name] = [member_number, member_instance]
    
class _Basic():
    def __init__(self, name : str, ui):
        self.name = name
        self.ui = ui
    
    def __init_subclass__(cls, /, _type, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._type = _type
    
class Text(_Basic, "text"):
    def __init__(self, ui, 
                 name : str, 
                 position : list | tuple = (None, None), 
                 msg : str = "text", 
                 size : int | float = 20, 
                 font : str = "SimHei", 
                 color : list | tuple = (255, 255, 255)):
        super().__init__(name, ui)
        if position == (None, None):
            self.position = (int(ui.size[0] / 2), int(ui.size[1] / 2))
        else:
            self.position = position
        self.msg = msg
        self.size = size
        self.font = font
        self.color = color

class Image(_Basic, "image"):
    pass

class Figure(_Basic, "figure"):
    pass
