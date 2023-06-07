from consts import *
import pygame
import ast

pygame.font.init()

class Block:
    count = 0  # Class variable to keep track of the block count
    map = {"testcasegroup": 0,"testcase": 1,"parameter": 2,}
    font = pygame.font.Font('freesansbold.ttf', 32)
    def __init__(self, name: str, shape: pygame.Rect, text):
        self.name = name
        self.number = Block.count + 1
        self.id = f"{self.name}_{self.number}"
        self.hover = False
        self.shape = shape
        self.text =  Block.font.render(text, True, BLUE, RED_LIGHT)
        self.text_rect  = self.text.get_rect()
        self.text_rect.center = self.shape.center
        self.params = {}
        Block.count += 1
        self.children = []

    def add_param(self, key, value):
        self.params[key] = value

    def add_child(self, child_block):
        self.children.append(child_block)
    
    def update_position(self,position: tuple[int,int]):
        self.shape.center = position
        self.text_rect.center = self.shape.center

    def draw_on(self,screen: pygame.Surface):
        pygame.draw.rect(screen,self.params["color"] or RED, self.shape)
        screen.blit(self.text,self.text_rect)
        for child in self.children:
            child.draw(screen)

    def get_count(self):
        return self.count

    def __eq__(self, other):
        if isinstance(other, Block):
            return self.map[self.name] == other.map[self.name]
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Block):
            return self.map[self.name] < other.map[self.name]
        return NotImplemented
    
    def __str__(self) -> str:
        return f"ID: {self.id} hover: {self.hover}"