import os
import sys
import pygame
import tkinter as tk
import tkinter.ttk as ttk
import xml.dom.minidom as MD
from typing import List
from typing import Dict
from typing import Optional
import threading

from Block import Block
from consts import *

class Game:
    def __init__(self):
        self.window: pygame.Surface = window
        self.objs: List[Block] = []
        self.block_dict: Dict[str,Block] = {}
        self.active_obj: Optional[Block] = None
        self.make_more = True
        self.save_button_rect = pygame.Rect(
            WINDOW_WIDTH - BUTTON_WIDTH - 10,
            WINDOW_HEIGHT - BUTTON_HEIGHT - 10,
            BUTTON_WIDTH,
            BUTTON_HEIGHT
        )

    def __getitem__(self, item):
        for obj in self.objs:
            if obj.id == item:
                return obj
        raise KeyError(f"Object block with id '{item}' not found.")
    
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.MOUSEBUTTONDOWN:  # Left mouse button
                        if pygame.mouse.get_pressed()[0]:
                            os.system('cls')
                            print(self.active_obj)
                            if self.save_button_rect.collidepoint(event.pos):
                                self.save_xml()
                            else:
                                if self.make_more:
                                    self.create_block(SELECTED_OPTION, event.pos)
                                else:
                                    pass
                        elif pygame.mouse.get_pressed()[2]:
                            os.system('cls')
                            print(self.active_obj)
                            print("======================")
                            print(*self.objs)
                        
                elif event.type == pygame.MOUSEBUTTONUP:    
                    if pygame.MOUSEBUTTONUP:
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
            if name == SELECTED_OPTION:
                block = Block(name,f"{name}_{Block.count+1}",pos,BLOCK_SIZE[name])
                self.block_dict[block.id] = block
            else:
                raise ValueError("Invalid block name.")

            block.add_param("pos",str(pos))
            self.active_obj = block
            self.active_obj.active = True
            self.objs.append(self.active_obj)
            self.objs.sort()

        except ValueError as e:
            print(f"Error: {str(e)}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")


    def update_objs(self): 
        MOUSE_POS = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]  # Check if the left mouse button is pressed

        if self.active_obj is not None:
            if mouse_pressed:
                self.active_obj.press = True
                self.active_obj.update_position(MOUSE_POS)
            else:
                self.active_obj.press = False
                for obj in self.objs:
                    if obj.rect.colliderect(self.active_obj.rect) and obj.id != self.active_obj.id:
                        print(f"Add {self.active_obj.id} as a child to {obj.id}")
                        obj.add_child(self.block_dict[self.active_obj.id])
                        self.objs.remove(self.block_dict[self.active_obj.id])
                        
                self.active_obj = None
        else:
            self.make_more = True

            for obj in self.objs:
                if obj.rect.collidepoint(MOUSE_POS):
                    self.make_more = False
                    obj.hover = True
                    if mouse_pressed:
                        self.active_obj = obj
                        self.active_obj.active = True
                        break
                else:
                    obj.hover = False


    def draw_window(self):
        window.fill(GRAY)

        if self.active_obj != None:
            self.active_obj.draw_on(window)

        for obj in reversed(self.objs):
            obj.draw_on(window)

        pygame.draw.rect(window, BUTTON_COLOR, self.save_button_rect)
        save_font = pygame.font.Font(None, 24)
        save_text = save_font.render("Save", True, BUTTON_TEXT_COLOR)
        save_text_rect = save_text.get_rect(center=self.save_button_rect.center)
        window.blit(save_text, save_text_rect)

        pygame.display.flip()

def chose_option(chose):
    global SELECTED_OPTION
    SELECTED_OPTION = OPTIONS[chose]

def pygame_thread_obj():
    print("pygame_thread_obj")
    game = Game()
    game.run()

def main():
    root = tk.Tk()
    embed = tk.Frame(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
    embed.grid(columnspan=600, rowspan=500)
    embed.pack(side=tk.LEFT)
    buttonwin = tk.Frame(root, width=75, height=WINDOW_HEIGHT)
    buttonwin.pack(side=tk.LEFT)

    os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
    os.environ['SDL_VIDEODRIVER'] = 'windib'

    global window
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    window.fill(pygame.Color(255, 255, 255))
    pygame.display.init()
    button1 = tk.Button(buttonwin, text=OPTIONS[0], command=lambda: chose_option(0))
    button1.pack(side=tk.TOP)
    button2 = tk.Button(buttonwin, text=OPTIONS[1], command=lambda: chose_option(1))
    button2.pack(side=tk.TOP)
    button3 = tk.Button(buttonwin, text=OPTIONS[2], command=lambda: chose_option(2))
    button3.pack(side=tk.TOP)

    pygame_thread = threading.Thread(target=pygame_thread_obj)
    pygame_thread.daemon = True
    pygame_thread.start()

    root.mainloop()

if __name__ == "__main__":
    print("mian start")
    main()
print("OUT")