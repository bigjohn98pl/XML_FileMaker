import pygame
import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
import numpy as np
import xml.dom.minidom as MD
from typing import List

from Block import Block
from consts import *

# Initialize Pygame
pygame.init()
pygame_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

def tk_window(obj:Block):
    # Initialize Tkinter
    tk_window = tk.Tk()
    tk_window.geometry('500x500')
    tk_window.title("Pygame in Tkinter")

    # Create a Tkinter canvas to hold the Pygame surface
    canvas = tk.Canvas(tk_window, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
    canvas.pack()

    # Convert the Pygame surface to a NumPy array
    pygame_surface = pygame_window
    obj.draw_on(pygame_surface)
    pygame_image = pygame.surfarray.array3d(pygame_surface).swapaxes(0, 1)
    pygame_image = np.ascontiguousarray(pygame_image)

    # Create a PIL image from the NumPy array
    pil_image = Image.frombytes('RGB', (WINDOW_WIDTH, WINDOW_HEIGHT), pygame_image.tobytes())

    # Create a Tkinter image from the PIL image
    tk_image = ImageTk.PhotoImage(pil_image)

    # Draw the Tkinter image on the canvas
    canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)

    # Start the Tkinter event loop
    tk_window.mainloop()

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
                    if pygame.MOUSEBUTTONDOWN:  # Left mouse button
                        if self.save_button_rect.collidepoint(event.pos):
                            tk_window(self.objs[0])
                            self.save_xml()
                        else:
                            if self.make_more:
                                settings = set_parameters_for_obj()
                                self.create_block(settings, event.pos)
                            print(*self.objs,sep=" ")
                elif event.type == pygame.MOUSEBUTTONUP:    
                    if pygame.MOUSEBUTTONUP:
                        print("click")
                        pass

            self.update_objs()
            self.draw_window()

        pygame.quit()

    def save_xml(self):
        # TODO: make a uploat_xml funcionality base on xml.etree.ElementTree (faster for upload?)
        doc = MD.Document()
        module = doc.createElement("module")
        doc.appendChild(module)

        for obj in self.objs:
            obj_xml = doc.createElement(obj.name)
            obj_xml.setAttribute("id",obj.id)
            obj_xml.appendChild(doc.createTextNode(str(obj.params["pos"])))
            module.appendChild(obj_xml)
        
        xml_str = doc.toprettyxml(indent="    ")
        with open("output.xml", "w") as f:
            f.write(xml_str)
        print("XML file saved!")

    def create_block(self, name, pos):
        try:
            color = None
            if name == OPTIONS[0]:
                block = Block(name,(pos[0], pos[1], 200, 200) , name)
                color = YELLOW
            elif name == OPTIONS[1]:
                block = Block(name,(pos[0], pos[1], 150, 50) , name)
                color = RED_LIGHT
            elif name == OPTIONS[2]:
                block = Block(name,(pos[0], pos[1], 100, 30) , name)
                color = BLUE
            else:
                raise ValueError("Invalid block name.")

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
                if obj.rect.collidepoint(MOUSE_POS):
                    obj.update_position(MOUSE_POS)
                    # if obj.rect.colliderect(pygame.Rect(MOUSE_POS[0],MOUSE_POS[1], 1, 1)):
                    #     print("siema ziom")
                    
            if obj.rect.colliderect(pygame.Rect(MOUSE_POS[0],MOUSE_POS[1], 1, 1)):
                obj.hover = True
                self.make_more = False
                break
            else:
                obj.hover = False
                self.make_more = True


    def draw_window(self):
        pygame_window.fill(BLACK)

        for obj in self.objs:
            obj.draw_on(pygame_window)

        pygame.draw.rect(pygame_window, BUTTON_COLOR, self.save_button_rect)
        save_font = pygame.font.Font(None, 24)
        save_text = save_font.render("Save", True, BUTTON_TEXT_COLOR)
        save_text_rect = save_text.get_rect(center=self.save_button_rect.center)
        pygame_window.blit(save_text, save_text_rect)

        pygame.display.flip()


# Create the game object and run the game
game = Game()
game.run()
