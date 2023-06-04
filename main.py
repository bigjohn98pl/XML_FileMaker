import pygame
import xml.etree.ElementTree as ET
from typing import List

from Block import Block

# Initialize Pygame
pygame.init()

# Set up the window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("XML Block Editor")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)

# Button parameters
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 30
BUTTON_COLOR = (100, 100, 100)
BUTTON_TEXT_COLOR = WHITE

class Game:
    def __init__(self):
        self.objs: List[Block] = []
        self.is_rectangle = True
        self.update = False
        self.save_button_rect = pygame.Rect(
            WINDOW_WIDTH - BUTTON_WIDTH - 10,
            WINDOW_HEIGHT - BUTTON_HEIGHT - 10,
            BUTTON_WIDTH,
            BUTTON_HEIGHT
        )
        self.toggle_button_rect = pygame.Rect(
            WINDOW_WIDTH - BUTTON_WIDTH - 10,
            WINDOW_HEIGHT - BUTTON_HEIGHT * 2 - 20,
            BUTTON_WIDTH,
            BUTTON_HEIGHT
        )

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        if self.save_button_rect.collidepoint(event.pos):
                            self.save_xml()
                        elif self.toggle_button_rect.collidepoint(event.pos):
                            self.toggle_shape()
                        else:
                            if self.update == False:
                                if self.is_rectangle:
                                    self.create_block("block", event.pos)
                                else:
                                    self.create_block("circle", event.pos)
                                print(*self.objs,sep=" ")
                                pos = pygame.mouse.get_pos()
                                print(f"1: {pos}")
                                self.update = True
                elif event.type == pygame.MOUSEBUTTONUP:    
                    if event.button == 1:
                        # self.update = False
                        pos = pygame.mouse.get_pos()
                        print(f"2: {pos}")
            self.update_objs()
            self.draw_window()

        pygame.quit()

    def save_xml(self):
        root = ET.Element("root")
        for obj in self.objs:
            block_elem = ET.SubElement(root, obj.name)
            block_elem.set("id", obj.id)
            for param_name, param_value in obj.params.items():
                block_elem.set(param_name, param_value)
        xml_tree = ET.ElementTree(root)
        xml_tree.write("output.xml", encoding="utf-8", xml_declaration=True)
        print("XML file saved!")

    def toggle_shape(self):
        self.is_rectangle = not self.is_rectangle

    def create_block(self, name, pos):
        
        if name == "block":
            shape = pygame.Rect(pos[0], pos[1], 50, 50)
        elif name =="circle":
             shape = pygame.Rect(pos[0], pos[1], 50, 50)
        block = Block(name, shape)
        block.add_param("pos",str(pos))
        print(f"update: {self.update}")
        self.objs.append(block)

    def update_objs(self):
        for obj in self.objs:
            if pygame.mouse.get_pressed()[0]:  # Left mouse button pressed
                if obj.shape.collidepoint(pygame.mouse.get_pos()):
                    obj.shape.center = pygame.mouse.get_pos()
                    self.update = True
                else:
                    self.update = False

    def draw_window(self):
        window.fill(BLACK)

        for obj in self.objs:
            if obj.name == "block":
                pygame.draw.rect(window, WHITE, obj.shape)
            else:
                pygame.draw.ellipse(window, RED, obj.shape)

        pygame.draw.rect(window, BUTTON_COLOR, self.save_button_rect)
        save_font = pygame.font.Font(None, 24)
        save_text = save_font.render("Save", True, BUTTON_TEXT_COLOR)
        save_text_rect = save_text.get_rect(center=self.save_button_rect.center)
        window.blit(save_text, save_text_rect)

        pygame.draw.rect(window, BUTTON_COLOR, self.toggle_button_rect)
        toggle_font = pygame.font.Font(None, 24)
        toggle_text = toggle_font.render("Toggle", True, BUTTON_TEXT_COLOR)
        toggle_text_rect = toggle_text.get_rect(center=self.toggle_button_rect.center)
        window.blit(toggle_text, toggle_text_rect)

        pygame.display.flip()


# Create the game object and run the game
game = Game()
game.run()
