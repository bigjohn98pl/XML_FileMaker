import pygame
import tkinter as tk
import tkinter.ttk as ttk
import xml.etree.ElementTree as ET
from typing import List

from Block import Block
from consts import *

# Initialize Pygame
pygame.init()

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("XML Block Editor")

def button_clicked(variable):
    print(variable.get())

def set_parameters_for_obj():
    set_window = tk.Tk()
    set_window.geometry('200x100')
    set_window.title("Block settings")
    label_type = tk.Label(text="Block Type:")

    variable = tk.StringVar(set_window)
    variable.set(OPTIONS[0])
    menu_type = tk.OptionMenu(set_window,variable,*OPTIONS)
    button_ok = tk.Button(set_window,text="OK",command=lambda: button_clicked(variable))
    value_in = tk.Label(text="Value in:")
    
    label_type.pack()
    value_in.pack()
    menu_type.pack()
    button_ok.pack()

    set_window.mainloop()
    return variable.get()

class Game:
    def __init__(self):
        self.objs: List[Block] = []
        self.make_more = True
        self.save_button_rect = pygame.Rect(
            WINDOW_WIDTH - BUTTON_WIDTH - 10,
            WINDOW_HEIGHT - BUTTON_HEIGHT - 10,
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
                        else:
                            if self.make_more:
                                settings = set_parameters_for_obj()
                                self.create_block(settings, event.pos)
                            print(*self.objs,sep=" ")
                elif event.type == pygame.MOUSEBUTTONUP:    
                    if event.button == 1:
                        pass

            self.update_objs()
            self.draw_window()

        pygame.quit()

    def save_xml(self):
        root = ET.Element("root")
        for obj in self.objs:
            block_elem = ET.SubElement(root, obj.name)
            block_elem.set("id", obj.id)
            block_elem.text = "lol"
            for param_name, param_value in obj.params.items():
                block_elem.set(param_name, param_value)
        xml_tree = ET.ElementTree(root)
        xml_tree.write("output.xml", encoding="utf-8", xml_declaration=True)
        print("XML file saved!")

    def create_block(self, name, pos):
        try:
            shape = None
            color = None
            if name == OPTIONS[0]:
                shape = pygame.Rect(pos[0], pos[1], 200, 200)
                color = YELLOW
            elif name == OPTIONS[1]:
                shape = pygame.Rect(pos[0], pos[1], 150, 50)
                color = RED_LIGHT
            elif name == OPTIONS[2]:
                shape = pygame.Rect(pos[0], pos[1], 100, 30)
                color = BLUE
            else:
                raise ValueError("Invalid block name.")

            block = Block(name, shape)
            block.add_param("pos",str(pos))
            block.add_param("color",color)
            print(f"make_more: {self.make_more}")
            self.objs.append(block)
            self.objs.sort()

        except ValueError as e:
            print(f"Error: {str(e)}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")


    def update_objs(self):
        MOUSE_POS = pygame.mouse.get_pos()
        for obj in self.objs:
            if pygame.mouse.get_pressed()[0]:  # Left mouse button pressed
                if obj.shape.collidepoint(MOUSE_POS):
                    obj.shape.center = MOUSE_POS
                    # if obj.shape.colliderect(pygame.Rect(MOUSE_POS[0],MOUSE_POS[1], 1, 1)):
                    #     print("siema ziom")
                    
            if obj.shape.colliderect(pygame.Rect(MOUSE_POS[0],MOUSE_POS[1], 1, 1)):
                obj.hover = True
                self.make_more = False
                break
            else:
                obj.hover = False
                self.make_more = True


    def draw_window(self):
        window.fill(BLACK)

        for obj in self.objs:
            obj.draw_on(window)

        pygame.draw.rect(window, BUTTON_COLOR, self.save_button_rect)
        save_font = pygame.font.Font(None, 24)
        save_text = save_font.render("Save", True, BUTTON_TEXT_COLOR)
        save_text_rect = save_text.get_rect(center=self.save_button_rect.center)
        window.blit(save_text, save_text_rect)

        pygame.display.flip()


# Create the game object and run the game
game = Game()
game.run()
