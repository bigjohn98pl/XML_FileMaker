from consts import *
import pygame
import ast
from typing import List
pygame.font.init()
class Block:
    count: int = 0  # Class variable to keep track of the block count
    font_size: int = 12
    def __init__(self,surface: pygame.Surface, name: str,text: str, position: tuple[int,int],size: tuple[int,int]):
        self.surface = surface
        self.number: int = Block.count
        self.name: str = name
        self.id: str = f"{self.name}_{self.number}"
        self.hover = False
        self.press = False
        self.active = False
        self.position = position
        self.size: tuple[int,int] = size
        self.color: Color     = MAP_COLOR[self.name] or WHITE
        self.dim_color: Color = tuple(int(component * DIM_FACTOR) for component in self.color)
        

        self.rect = pygame.Rect(position[0],position[1],size[0],size[1])
        self.text_rects: List[tuple[pygame.Surface,pygame.Rect,str]] = []
        self.params = {}

        self.children: List[Block] = []
        Block.count += 1

    def add_param(self, key, value):
        self.params[key] = value
        try:
            self.text_rects.append(self.render_parameter_text(key))
        except ValueError as e:
            print(f"Error: {str(e)}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def render_parameter_text(self,key):
        try:
            print("render_parameter_text")
            font_size: int = Block.font_size
            if key == "variants":
                font_size = int(float(Block.font_size) * 0.8)
            text_parameter_value = pygame.font.Font('freesansbold.ttf', font_size)
            text_surface =  text_parameter_value.render(self.params[key], True, BLACK, self.dim_color)
            text_rect  = text_surface.get_rect()
            
            if self.name == "parameter":
                    if key == "name":
                        text_rect.topleft = self.rect.topleft
                    if key == "type":
                        text_rect.topright = self.rect.topright
                    if key == "value":
                        text_rect.center = self.rect.center

            if self.name == "testcase":
                if key == "ident":
                    text_rect.bottomleft = self.rect.topleft
                if key == "title":
                    text_rect.topleft = self.rect.topleft
                if key == "func_name":
                    text_rect.topleft = self.rect.topleft
                    text_rect.y += text_rect.h
                if key == "variants":
                    text_rect.bottomright = self.rect.topright

            if self.name == "testcasegroup":
                if key == "title":
                    text_rect.bottomleft = self.rect.topleft
                if key == "variants":
                    text_rect.bottomright = self.rect.topright
            self.update_position(self.position)
            return (text_surface,text_rect,key)
        except:
            self.update_position(self.position)
            return (self.surface,pygame.Rect(MOUSE_POS,(10,10)),key)
            
    def update_render_text(self,updated_key: str):
        print("render_parameter_text")
        font_size: int = Block.font_size
        if updated_key == "variants":
            font_size = int(float(Block.font_size) * 0.8)
        text_parameter_value = pygame.font.Font('freesansbold.ttf', font_size)
        updated_text_surface =  text_parameter_value.render(self.params[updated_key], True, BLACK, self.dim_color)
        updated_text_rect  = updated_text_surface.get_rect()
        
        if self.name == "parameter":
            if updated_key == "name":
                updated_text_rect.topleft = self.rect.topleft
            if updated_key == "type":
                updated_text_rect.topright = self.rect.topright
            if updated_key == "value":
                updated_text_rect.center = self.rect.center

        if self.name == "testcase":
            if updated_key == "ident":
                updated_text_rect.bottomleft = self.rect.topleft
            if updated_key == "title":
                updated_text_rect.topleft = self.rect.topleft
            if updated_key == "func_name":
                updated_text_rect.topleft = self.rect.topleft
                updated_text_rect.y += updated_text_rect.h
            if updated_key == "variants":
                updated_text_rect.bottomright = self.rect.topright

        if self.name == "testcasegroup":
            if updated_key == "title":
                updated_text_rect.bottomleft = self.rect.topleft
            if updated_key == "variants":
                updated_text_rect.bottomright = self.rect.topright

        upate_para = (updated_text_surface,updated_text_rect,updated_key)
        for idx, para in enumerate(self.text_rects):
            if para[2] == updated_key:
                self.text_rects[idx] = upate_para
                self.update_position(self.position)

    def add_child(self, child_block):
        if isinstance(child_block, Block):
            self.children.append(child_block)
            self.rect.h += child_block.rect.h + MARGIN
            self.size = self.rect.size
        else:
            raise ValueError("Invalid child block. Expected instance of Block class.")

    def remove_last_child(self):
        child = self.children.pop()
        self.rect.h -= child.rect.h + MARGIN
        self.size = self.rect.size
    
    def update_position(self, new_position: tuple[int, int]):
        # Calculate the position offset
        child_position_offset = (new_position[0] - self.position[0], new_position[1] - self.position[1])

        # Update the position of the block
        self.position = new_position
        self.rect.topleft = self.position
        try:
            for text_surf,text_rect,key in self.text_rects:
                if self.name == "parameter":
                    if key == "name":
                        text_rect.topleft = self.rect.topleft
                    if key == "type":
                        text_rect.topright = self.rect.topright
                    if key == "value":
                        text_rect.center = self.rect.center

                if self.name == "testcase":
                    if key == "ident":
                        text_rect.bottomleft = self.rect.topleft
                    if key == "title":
                        text_rect.topleft = self.rect.topleft
                    if key == "func_name":
                        text_rect.topleft = self.rect.topleft
                        text_rect.y += text_rect.h
                    if key == "variants":
                        text_rect.bottomright = self.rect.topright

                if self.name == "testcasegroup":
                    if key == "title":
                        text_rect.bottomleft = self.rect.topleft
                    if key == "variants":
                        text_rect.bottomright = self.rect.topright

        except ValueError as e:
            print(f"Error: {str(e)}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

        # Update the position of child blocks relative to the new parent position
        y_offset = self.rect.top + TOP_MARGIN  # Start with an offset below the parent block
        for child in self.children:
            new_child_position = (self.position[0] + child_position_offset[0] + X_MARGIN, y_offset)
            child.update_position(new_child_position)
            y_offset += child.rect.height + MARGIN  # Increment the offset for the next child block
        self.size = self.rect.size

    def update_chldren_positions(self):
        child_position_offset = (self.position[0] - self.position[0], self.position[1] - self.position[1])
        y_offset = self.rect.top + TOP_MARGIN
        for child in self.children:
            new_child_position = (self.position[0] + child_position_offset[0] + X_MARGIN, y_offset)
            child.update_position(new_child_position)
            y_offset += child.rect.height + MARGIN  # Increment the offset for the next child block
        self.size = self.rect.size

    def draw_on(self,screen: pygame.Surface):
        pygame.draw.rect(screen,self.color, self.rect)
        try:
            for tex_surf,tex_rect,key in self.text_rects:
                screen.blit(tex_surf,tex_rect)
        except:
            print("Error in draw on. cant draw parameters.")

        for child in self.children:
            child.draw_on(screen)

    def scale_font_size(self, rect: pygame.Rect, reference_size) -> pygame.font.Font:
        # Calculate the scaling factor based on the width and height ratios
        # width_ratio =  rect.width / Block.font_size
        # height_ratio = rect.height / Block.font_size
        # scaling_factor = min(width_ratio, height_ratio)

        # Scale the font size based on the scaling factor
        # scaled_font_size = int(Block.font_size * scaling_factor)

        # Create a new font with the scaled font size
        scaled_font = pygame.font.Font('freesansbold.ttf', Block.font_size)
        return scaled_font
    
    def get_count(self):
        return self.count

    def __eq__(self, other):
        if isinstance(other, Block):
            return MAP_NAME[self.name] == MAP_NAME[other.name]
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Block):
            return MAP_NAME[self.name]+self.count < MAP_NAME[other.name]+other.count
        return NotImplemented

    def __str__(self) -> str:
        child_positions = '\n'.join(f"\tID: {child.id} pos:{child.position} rect:{child.rect}" for child in self.children)
        return f"ID: {self.id}\nPress: {self.press}\nHover: {self.hover}\nActive: {self.active}\nRec: {self.rect}\nChildren:\n{child_positions}"