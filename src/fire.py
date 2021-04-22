#_*_coding:utf-8_*_
#created by FranciscoCharles in april,2021.

from pygame import Surface
from typing import Tuple, NewType

Index = Tuple[int,int]

class FireColorArray:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.data = [0 for _ in range(width*height)]
    
    @property
    def shape(self) -> Tuple[int,int]:
        return (self.height, self.width)

    def  validateIndex(self, pos: Index) -> Index:
        (row, column) = pos
        if row<0:
            row = self.height - abs(row)%self.height
        if column<0:
            column = self.width - abs(column)%self.width
        
        return (row%self.height, column%self.width)

    def __getitem__(self, pos: Index) -> int:
        pos = self.validateIndex(pos)
        return self.data[pos[1] + self.width*pos[0]]

    def __setitem__(self, pos: Index, value: int) -> None:
        pos = self.validateIndex(pos)
        self.data[pos[1] + self.width*pos[0]] = value