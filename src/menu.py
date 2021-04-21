#_*_coding:utf-8_*_
import pygame
from pygame import Surface
from typing import Tuple, List, NewType

HslColor = Tuple[int,float,float]
Positions = List[Tuple[int, int]]

class Menu:
    def __init__(self,  max_color:int = 0) -> None:
        self.font = pygame.font.SysFont('Verdana', 20)
        self.font.set_bold(True)
        self.menus = {
            0:{'name':'FPS','value':20,'step':10,'min':10,'max':60,'callback':None},
            1:{'name':'decay','value':3,'step':1,'min':1,'max':max_color,'callback':None},
            2:{'name':'wind direction','value':1,'step':1,'min':0,'max':2,'types':['right','left','both'],'callback':None},
            3:{'name':'wind force','value':7,'step':1,'min':0,'max':10,'callback':None},
            4:{'name':'color intensity','value':False,'color':{'H':180,'L':1.0,'S':1.0}},
            5:{'name':'H','value':180,'step':1,'min':0,'max':360,'callback':None},
            6:{'name':'S','value':1.0,'step':0.05,'min':0.0,'max':1.0,'callback':None},
            7:{'name':'L','value':1.0,'step':0.05,'min':0.0,'max':1.0,'callback':None},
        }
        self.current_menu_key = 0

    @property
    def name(self) -> str:
        return self.menus[self.current_menu_key]['name']

    def __getitem__(self, key:str) -> dict:
        for value in self.menus.values():
            if value['name']==key:
                return value
        raise KeyError

    def up(self) -> None:
        if self.current_menu_key == 0 and not self['color intensity']['value']:
            self.current_menu_key = 4
        else:
            self.current_menu_key = 7 if self.current_menu_key == 0 else self.current_menu_key-1

    def down(self) -> None:
        if self.current_menu_key==4 and not self['color intensity']['value']:
            self.current_menu_key = 0
        else:
            self.current_menu_key = 0 if self.current_menu_key==len(self.menus.keys())-1 else self.current_menu_key+1

    def updateColor(self) -> None:
        menu = self.currentMenuValue()
        if self.name in ['H','L','S']:
            self["color intensity"]['color'][self.name] = menu['value']

    def decrement(self) -> None:
        menu = self.currentMenuValue()
        if menu['name'] == 'color intensity':
            menu['value'] = not menu['value']
        elif menu['min'] < menu['value']:
            menu['value'] -= menu['step']
            self.updateColor()

    def currentColorValue(self) -> Tuple[int, float, float]:
        return tuple(self['color intensity']['color'].values())

    def increment(self) -> None:
        menu = self.currentMenuValue()
        if menu['name']=='color intensity':
            menu['value'] = not menu['value']
        elif menu['max']>menu['value']:
            menu['value'] += menu['step']
            self.updateColor()

    def currentMenuValue(self) -> dict:
        return self.menus[self.current_menu_key]

    def draw(self, surface: Surface, positions: Positions) -> None:
        name = self.name
        for position, menu in zip(positions, self.menus.values()):
            color = (255,255,0) if menu['name']==name else (255,255,255)
            text = self.font.render(f"{menu['name']}:", True, color)
            (x, y, x_value) = position
            surface.blit(text, (x, y))
            if menu['name'] == 'wind direction':
                value = menu['types'][menu['value']]
            else:
                value = menu['value']
                if isinstance(value, float):
                    value = '%.2lf'%abs(value)
            text = self.font.render(f"{value}", True, color)
            surface.blit(text, (x_value, y))

    def getListPositionMenu(self, x: int, y: int, space_y: int = 40, space_value: int = 10) -> Positions:
        next_y = y
        positions = []
        for key in self.menus.keys():
            text = self.font.render(f"{self.menus[key]['name']}:", True, (0,0,0))
            width = text.get_width()
            x_value = x+space_value
            new_x = x-width
            positions.append((new_x,next_y,x_value))
            next_y += space_y
        return positions