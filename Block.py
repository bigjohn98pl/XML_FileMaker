from consts import *
import xml.dom.minidom as MD
import xml.etree.ElementTree as ET
import pygame
import ast
from typing import List
pygame.font.init()
class Block:
    count: int = 0  # Class variable to keep track of the block count
    font_size: int = 10
    scale: int = 0
    def __init__(self,surface: pygame.Surface, name: str, position: tuple[int,int],size: tuple[int,int]):
        self.surface = surface
        self.number: int = Block.count
        self.name: str = name
        self.id: str = f"{self.name}_{self.number}"
        self.hover = False
        self.press = False
        self.active = False
        self.position = position
        self.size: tuple[int,int] = size[0] + Block.scale, size[1] + Block.scale
        self.color: Color     = MAP_COLOR[self.name] or WHITE
        self.dim_color: Color = (int(self.color[0]*DIM_FACTOR),int(self.color[1]*DIM_FACTOR),int(self.color[2]*DIM_FACTOR))
        

        self.rect = pygame.Rect(
            self.position[0],
            self.position[1],
            self.size[0],
            self.size[1]
            )

        self.text_rects: List[tuple[pygame.Surface,pygame.Rect,str]] = []

        self.params = {}
        if self.name in OPTIONS_NUM[0]:
            self.add_param(BLOCK_PARAMETERS[0],"Def_name")
            self.add_param(BLOCK_PARAMETERS[1],"Def_type")
            self.add_param(BLOCK_PARAMETERS[2],"Def_value")
        if self.name in OPTIONS_NUM[1]:
            self.add_param(BLOCK_PARAMETERS[3],"Def_ident")
            self.add_param(BLOCK_PARAMETERS[4],"Def_title")
            self.add_param(BLOCK_PARAMETERS[0],"Def_func_name")
            self.add_param(BLOCK_PARAMETERS[6],"Def _var1 _var2")
        if self.name in OPTIONS_NUM[2]:
            self.add_param(BLOCK_PARAMETERS[4],"Def _title")
            self.add_param(BLOCK_PARAMETERS[6],"Def _var1 _var2")

        self.children: List[Block] = []
        Block.count += 1


    def add_param(self, key, value):
        self.params[key] = value
        try:
            self.text_rects.append(self.render_parameter_text(key))
        except ValueError as e:
            print(f"Error: {str(e)}")
        except Exception as e:
            print(f"An error occurred add_param(): {str(e)}")

    def render_parameter_text(self,key):
        # if key == "variants":
        #     Block.font_size = int(float(Block.font_size) * 0.8)
        text_parameter_value = pygame.font.Font('freesansbold.ttf', Block.font_size)
        if self.name == OPTIONS[1] and key == BLOCK_PARAMETERS[0]:
            text_surface =  text_parameter_value.render(f"{self.params[key]}()", True, BLACK, self.dim_color)
        else:
            text_surface =  text_parameter_value.render(f"{self.params[key]}", True, BLACK, self.dim_color)
        text_rect  = text_surface.get_rect()
        
        self.text_positioning(self.name,key,text_rect)

        return (text_surface,text_rect,key)
            
    def update_render_text(self,updated_key: str, font_size: int):
        # if updated_key == "variants":
        #     Block.font_size = int(floor(Block.font_size) * 0.8)
        text_parameter_value = pygame.font.Font('freesansbold.ttf', font_size)
        updated_text_surface =  text_parameter_value.render(self.params[updated_key], True, BLACK, self.dim_color)
        updated_text_rect  = updated_text_surface.get_rect()
        
        self.text_positioning(self.name,updated_key,updated_text_rect)

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
            self.update_chldren_positions()
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

        for text_surf,text_rect,key in self.text_rects:
            self.text_positioning(self.name,key,text_rect)

        # Update the position of child blocks relative to the new parent position
        y_offset = self.rect.top + TOP_MARGIN  # Start with an offset below the parent block

        for child in self.children:
            new_child_position = (self.position[0] + child_position_offset[0] + X_MARGIN, y_offset)
            child.update_position(new_child_position)
            y_offset += child.rect.height + MARGIN  # Increment the offset for the next child block
        self.size = self.rect.size

    def text_positioning(self, block_name, key_parameter, text_rect: pygame.Rect):
        try:
            if block_name == OPTIONS[0]:
                if key_parameter == BLOCK_PARAMETERS[0]:
                    text_rect.topleft = self.rect.topleft
                if key_parameter == BLOCK_PARAMETERS[1]:
                    text_rect.topright = self.rect.topright
                if key_parameter == BLOCK_PARAMETERS[2]:
                    text_rect.bottomleft = self.rect.bottomleft

            if block_name == OPTIONS[1]:
                if key_parameter == BLOCK_PARAMETERS[3]:
                    text_rect.bottomleft = self.rect.topleft
                if key_parameter == BLOCK_PARAMETERS[4]:
                    text_rect.topleft = self.rect.topleft
                if key_parameter == BLOCK_PARAMETERS[0]:
                    text_rect.topleft = self.rect.topleft
                    text_rect.y += text_rect.h
                if key_parameter == BLOCK_PARAMETERS[6]:
                    text_rect.bottomright = self.rect.topright

            if block_name == OPTIONS[2]:
                if key_parameter == BLOCK_PARAMETERS[4]:
                    text_rect.bottomleft = self.rect.topleft
                if key_parameter == BLOCK_PARAMETERS[6]:
                    text_rect.bottomright = self.rect.topright


        except ValueError as e:
            print(f"Error text_positioning(): {str(e)}")
        except Exception as e:
            print(f"An error occurred in text_positioning(): {str(e)}")

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

    def scale_block(self, scale_value_block: int, scale_value_font: int):

        self.rect.inflate_ip(scale_value_block, scale_value_block)
        print(self.rect.size)
        for label in self.text_rects:
            self.update_render_text(label[2], scale_value_font)

        for child in self.children:
            child.scale_block(scale_value_block, scale_value_font)

    def create_xml_element(self,doc: MD.Document, obj: 'Block'):
        element = doc.createElement(obj.name)
        for param in obj.params:
            element.setAttribute(param, obj.params[param])

        for child in obj.children:
            child_element = self.create_xml_element(doc, child)
            element.appendChild(child_element)

        return element
    
    def load_from_xml(self,surface,xml_element:ET.Element):
        for para in xml_element.attrib.keys():
            self.add_param(para,xml_element.attrib[para])
        
        if self.name == OPTIONS[0]:
            self.add_param(BLOCK_PARAMETERS[2],xml_element.text)

        for child_element in xml_element:
            child = Block(surface,child_element.tag,self.position,BLOCK_SIZE[child_element.tag])
            child.load_from_xml(surface,child_element)
            self.add_child(child)
        
        return self
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