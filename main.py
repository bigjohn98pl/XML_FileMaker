import pygame
import xml.dom.minidom as MD
import threading
from Block import Block
from consts import *
from tkinter_gui import TkinterGui
class Game:
    def __init__(self):
        self.window: pygame.Surface = window
        self.objs: List[Block] = []
        self.block_dict: Dict[str,Block] = {}
        self.active_obj: Optional[Block] = None
        self.make_more = True
        self.selected_option = OPTIONS[0]
        self.save_button_rect = pygame.Rect(
            PY_WINDOW_WIDTH - BUTTON_WIDTH - 10,
            PY_WINDOW_HEIGHT - BUTTON_HEIGHT - 10,
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
            queue_event_handle(self)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.MOUSEBUTTONDOWN:  # Left mouse button
                        if pygame.mouse.get_pressed()[0]:
                            if self.save_button_rect.collidepoint(event.pos):
                                self.save_xml()
                            else:
                                if self.make_more:
                                    self.create_block(self.selected_option, event.pos)
                                else:
                                    pass
                        elif pygame.mouse.get_pressed()[2]:
                            # os.system('cls')
                            print(f"{pygame.mouse.get_pos()}")
                        
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
            if name in OPTIONS:
                block = Block(name,f"{name}_{Block.count+1}",pos,BLOCK_SIZE[name])
                self.block_dict[block.id] = block
            else:
                raise ValueError(f"Invalid block name {name}.")

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
                    if obj.rect.contains(self.active_obj.rect) and obj.id != self.active_obj.id:
                        print(f"Add {self.active_obj.id} as a child to {obj.id}")
                        if len(obj.children) == 0:
                            obj.rect.h = TOP_MARGIN    
                        obj.add_child(self.block_dict[self.active_obj.id])
                        obj.update_chldren_positions()
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
                        update_gui(self.active_obj)
                        break
                else:
                    obj.hover = False


    def draw_window(self):
        self.window.fill(GRAY)

        if self.active_obj != None:
            self.active_obj.draw_on(self.window)

        for obj in reversed(self.objs):
            obj.draw_on(self.window)

        pygame.draw.rect(self.window, BUTTON_COLOR, self.save_button_rect)
        save_font = pygame.font.Font(None, 24)
        save_text = save_font.render("Save", True, BUTTON_TEXT_COLOR)
        save_text_rect = save_text.get_rect(center=self.save_button_rect.center)
        self.window.blit(save_text, save_text_rect)

        pygame.display.flip()

def update_gui(object: Block):
    # Update the variables of the Game object here
    GUI_QUEUE.put({"action": "update_gui", 
                   "id": object.id,
                   "position": object.position,
                   "hover": object.hover,
                   "press": object.press,
                   "size": object.size
                   })
    print({object.id})

# Function to run the game in a separate thread
def pygame_thread_obj():
    print("pygame_thread_obj")
    pygame.display.init()
    game = Game()
    game.run()

def main():
    gui_window = TkinterGui()
    global window
    window = pygame.display.set_mode((PY_WINDOW_WIDTH, PY_WINDOW_HEIGHT))
    window.fill(BLACK)

    pygame_thread = threading.Thread(target=pygame_thread_obj)
    pygame_thread.daemon = True
    pygame_thread.start()

    gui_window.run_gui()

if __name__ == "__main__":
    print("mian start")
    main()
print("OUT")