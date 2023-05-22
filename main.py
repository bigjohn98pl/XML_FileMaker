import pygame
import xml.etree.ElementTree as ET
from typing import List

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

# Button parameters
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 30
BUTTON_COLOR = (100, 100, 100)
BUTTON_TEXT_COLOR = WHITE


class Block:
    count = 0  # Class variable to keep track of the block count

    def __init__(self, name, shape, params=None):
        self.name = name
        self.number = Block.count + 1
        self.id = f"{self.name}_{self.number}"
        self.shape = shape
        self.params = params or {}
        Block.count += 1


class Game:
    def __init__(self):
        self.blocks: List[Block] = []
        self.is_rectangle = True
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
                            self.create_block("block", event.pos)

            self.update_blocks()
            self.draw_window()

        pygame.quit()

    def save_xml(self):
        root = ET.Element("root")
        for obj in self.blocks:
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
        shape = pygame.Rect(pos[0], pos[1], 100, 50) if self.is_rectangle else pygame.Rect(pos[0], pos[1], 50, 50)
        block = Block(name, shape)
        self.blocks.append(block)

    def update_blocks(self):
        for block in self.blocks:
            if pygame.mouse.get_pressed()[0]:  # Left mouse button pressed
                if block.shape.collidepoint(pygame.mouse.get_pos()):
                    block.shape.center = pygame.mouse.get_pos()

    def draw_window(self):
        window.fill(BLACK)

        for block in self.blocks:
            if self.is_rectangle:
                pygame.draw.rect(window, WHITE, block.shape)
            else:
                pygame.draw.ellipse(window, WHITE, block.shape)

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
