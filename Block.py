from consts import *
import pygame
import ast
from typing import List

pygame.font.init()

class Block:
    count: int = 0  # Class variable to keep track of the block count
    font = pygame.font.Font('freesansbold.ttf', 32)

    def __init__(self, name: str,text: str, position: tuple[int,int],size: tuple[int,int]):
        Block.count += 1
        self.number: int = Block.count + 1
        self.name: str = name
        self.id: str = f"{self.name}_{self.number}"
        self.hover = False
        self.position = position
        self.size     = size
        self.color: Color     = MAP_COLOR[self.name] or WHITE
        self.dim_color: Color = tuple(int(component * DIM_FACTOR) for component in self.color)
        

        self.rect = pygame.Rect(position+size)
        self.text =  Block.font.render(text, True, BLACK, self.dim_color)
        self.text_rect  = self.text.get_rect()
        self.text_rect.center = self.rect.center

        self.params = {}
        self.children: List[Block] = []

    def add_param(self, key, value):
        self.params[key] = value

    def add_child(self, child_block):
        self.children.append(child_block)
    
    def update_position(self,position: tuple[int,int]):
        self.rect.center = position
        self.text_rect.center = self.rect.center

    def draw_on(self,screen: pygame.Surface):
        pygame.draw.rect(screen,self.color, self.rect)
        screen.blit(self.text,self.text_rect)
        for child in self.children:
            child.draw_on(screen)

    def get_count(self):
        return self.count

    def __eq__(self, other):
        if isinstance(other, Block):
            return MAP_NAME[self.name] == MAP_NAME[other.name]
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Block):
            return MAP_NAME[self.name] < MAP_NAME[other.name]
        return NotImplemented
    
    def __str__(self) -> str:
        return f"ID: {self.id} hover: {self.hover}"