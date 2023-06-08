import os
import pygame
import tkinter as tk
import tkinter.ttk as ttk
import xml.dom.minidom as MD
from typing import List
import threading

from Block import Block
from consts import *

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
        self.window: pygame.Surface = window
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
                            self.save_xml()
                        else:
                            if self.make_more:
                                # settings = set_parameters_for_obj()
                                self.create_block(SELECTED_OPTION, event.pos)
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
            elif name == OPTIONS[1]:
                block = Block(name,(pos[0], pos[1], 150, 50) , name)
            elif name == OPTIONS[2]:
                block = Block(name,(pos[0], pos[1], 100, 30) , name)
            else:
                raise ValueError("Invalid block name.")

            block.add_param("pos",str(pos))
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
        window.fill(GRAY)

        for obj in self.objs:
            obj.draw_on(window)

        pygame.draw.rect(window, BUTTON_COLOR, self.save_button_rect)
        save_font = pygame.font.Font(None, 24)
        save_text = save_font.render("Save", True, BUTTON_TEXT_COLOR)
        save_text_rect = save_text.get_rect(center=self.save_button_rect.center)
        window.blit(save_text, save_text_rect)

        pygame.display.flip()


# Create the game object and run the game
# game = Game()

def chose_option(chose):
    global SELECTED_OPTION
    SELECTED_OPTION = OPTIONS[chose]

# def pygame_event_loop(window):
#     print("start pygame thread")
#     game = Game()
#     game.run()

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

    pygame.init()
    window = pygame.display.set_mode((500, 500))
    window.fill(pygame.Color(255, 255, 255))
    pygame_thread = threading.Thread(target=pygame_thread_obj)
    pygame_thread.daemon = True
    pygame_thread.start()

    root.mainloop()
    # pygame_thread.join()


if __name__ == "__main__":
    print("mian start")
    main()
print("OUT")