from consts import *
import pygame
import ast

class Block:
    count = 0  # Class variable to keep track of the block count
    map = {"testcasegroup": 0,"testcase": 1,"parameter": 2,}
    def __init__(self, name, shape, params=None):
        self.name = name
        self.number = Block.count + 1
        self.id = f"{self.name}_{self.number}"
        self.hover = False
        self.shape = shape
        self.params = params or {}
        Block.count += 1
        self.children = []

    def add_param(self, key, value):
        self.params[key] = value

    def add_child(self, child_block):
        self.children.append(child_block)
    
    def draw_on(self,screen):
        pygame.draw.rect(screen,self.params["color"] or RED, self.shape)
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