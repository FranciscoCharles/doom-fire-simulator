#_*_coding:utf-8_*_
from os import environ
if 'PYGAME_HIDE_SUPPORT_PROMPT' not in environ:
    environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hidden'
del environ

import pygame
import colorsys
import numpy as np

from menu   import Menu, HslColor
from fire   import FireColorArray
from random import randint
from typing import Tuple, List, Optional, NewType

RgbColor = Tuple[int,int,int]

def rgb_to_float(r:int, g:int, b:int) ->[HslColor]:
    return (r/255, g/255,  b/255)
def rgb_to_int(r:int, g:int, b:int) -> RgbColor:
    return (int(r*255), int(g*255), int(b*255))

class DoomFireSimulator:
    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()
        self.SCREEN_W = 830
        self.SCREEN_H = 480
        pygame.display.set_caption('FireDoomSimaltor v1.0.1')
        self.display = pygame.display.set_mode((self.SCREEN_W,self.SCREEN_H))
        icon = pygame.image.load('images/icon32.png')
        pygame.display.set_icon(icon)
        self.clock = pygame.time.Clock()

        self.FPS = 20
        self.on_fire = True
        self.fire_size = (8,8)
        self.fire_x = 40
        self.fire_y = 40
        self.decay_value = 3
        self.wind_force = 7
        self.wind_mi_force = 0
        self.colors = self.selectColorPalette()
        self.fire_array = FireColorArray(40,50)
        self.setBaseFlameValue(len(self.colors)-1)
        self.menu = Menu(len(self.colors)-1)

    def selectColorPalette(self, options: Optional[HslColor] = None) -> List[RgbColor]:
        self.colors = [
            (7,7,7),(31,7,7),(47,15,7),(71,15,7),(87,23,7),(103,31,7),(119,31,7),(143,39,7),(159,47,7),(175,63,7),
            (191,71,7),(199,71,7),(223,79,7),(223,87,7),(223,87,7),(215,95,7),(215,95,7),(215,103,15),(207,111,15),
            (207,119,15),(207,127,15),(207,135,23),(199,135,23),(199,143,23),(199,151,31),(191,159,31),(191,159,31),
            (191,167,39),(191,167,39),(191,175,47),(183,175,47),(183,183,47),(183,183,55),(207,207,111),(223,223,159),
            (239,239,199),(255,255,255)]

        if isinstance(options, tuple) and len(options)==3:
            (shift_color, decay_l,decay_s) = options
            shift_color = (shift_color%360)/360
            result = []
            for cor in self.colors:
                cor = rgb_to_float(*cor)
                (_,l,s) = colorsys.rgb_to_hls(*cor)
                cor = colorsys.hls_to_rgb(shift_color, decay_l*l, decay_s*s)
                result.append(rgb_to_int(*cor))
            self.colors = result
        return self.colors
        
    def setBaseFlameValue(self, value: int) -> None:
        row,columns = self.fire_array.shape
        row -= 1
        for column in range(columns):
            self.fire_array[row,column] = value
    
    def updatePixelFire(self, row: int, column: int) -> None:

        decay = randint(0, self.decay_value)
        shift = column + randint(self.wind_mi_force, self.wind_force)
        self.fire_array[row, shift] = (self.fire_array[row+1, column]-decay)
        if self.fire_array[row, shift]<0:
            self.fire_array[row, shift] = 0
        return shift
        
    def evaporateFire(self) -> None:
        rows,columns = self.fire_array.shape
        for row in range(rows-1):
            for column in range(columns):
                self.updatePixelFire(row, column)

    def drawFire(self) -> None:
        rows,columns = self.fire_array.shape
        w,h = self.fire_size
        for row in range(rows):
            for column in range(columns):
                color = self.fire_array[row,column]
                rect = (self.fire_x+column*w,self.fire_y+row*h,w,h)
                pygame.draw.rect(self.display, self.colors[color], rect)
        self.evaporateFire()

    @property
    def rectFire(self) -> Tuple[int,int,int,int]:
        h,w = self.fire_array.shape
        return (self.fire_x, self.fire_y, w*self.fire_size[0], h*self.fire_size[1])

    def run(self) -> None:
        ticks = 0
        game = True
        draw_menu = True
        valid_keys = ['q','w','a','s','z','left','right','up','down']
        key_pressed = ''
        (x,y,w,h) = self.rectFire
        fire_rect = (x-1, y-1, w+2, h+2)
        rect_menu = (399, 39, 392, 402)
        positions = self.menu.getListPositionMenu(620, 94)

        pygame.draw.rect(self.display, (0xaaaaaa), fire_rect, 1)

        while game:
            self.clock.tick(self.FPS)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    game = False
                    break
                elif e.type == pygame.KEYDOWN:
                    key = pygame.key.name(e.key)
                    if key == 'escape':
                        game = False
                        break
                    elif key in valid_keys:
                        ticks = pygame.time.get_ticks()
                        key_pressed = key
                        getattr(self, key_pressed)()
                        draw_menu = True

                elif e.type == pygame.KEYUP:
                    key_pressed = ''

            if key_pressed and (pygame.time.get_ticks()-ticks)>500:
                getattr(self, key_pressed)()
                draw_menu = True

            if game:

                if draw_menu:
                    pygame.draw.rect(self.display, (0), rect_menu)
                    self.menu.draw(self.display, positions)
                    pygame.draw.rect(self.display, (0xaaaaaa), rect_menu, 1)
                    pygame.display.update(rect_menu)
                    draw_menu = False

                self.drawFire()
                pygame.display.update(fire_rect)

        self.stop()

    def changePalette(self) -> None:
        color = None
        if self.menu['color intensity']['value']:
            color = self.menu.currentColorValue()
        self.selectColorPalette(color)

    def updateSimulationValues(self) -> None:
        name = self.menu.name
        if name=='FPS':
            self.FPS = self.menu['FPS']['value']
        elif name=='decay':
            self.decay_value = self.menu['decay']['value']
        elif name=='wind direction':
            type_index = self.menu['wind direction']['value']
            type_value = self.menu['wind direction']['types'][type_index]
            wind_force = self.menu['wind force']['value']
            if type_value=='left':
                self.wind_mi_force = 0
                self.wind_force = wind_force
            elif type_value=='right':
                self.wind_mi_force = -wind_force
                self.wind_force = 0
            else:
                self.wind_force = wind_force
                self.wind_mi_force = -wind_force
        elif name=='wind force':
            self.wind_force = self.menu['wind force']['value']
        elif name in ['H','S','L','color intensity']:
            self.changePalette()

    def left(self) -> None:
        self.menu.decrement()
        self.updateSimulationValues()
    def right(self) -> None:
        self.menu.increment()
        self.updateSimulationValues()
    def up(self) -> None:
        self.menu.up()
    def down(self) -> None:
        self.menu.down()
    def a(self) -> None:
        self.left()
    def s(self) -> None:
        self.right()
    def w(self) -> None:
        self.up()
    def z(self) -> None:
        self.down()
    def q(self) -> None:
        self.on_fire = not self.on_fire
        self.setBaseFlameValue((len(self.colors)-1) if self.on_fire else 0)
    def stop(self) -> None:
        pygame.quit()

if __name__ == '__main__':
    DoomFireSimulator().run()



