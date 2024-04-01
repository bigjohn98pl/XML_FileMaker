import pygame
import xml.dom.minidom as MD
import xml.etree.ElementTree as ET
import threading
from Block import Block
from consts import *
from tkinter_gui import *

class Game:
    def __init__(self):
        self.window: pygame.Surface = window
        self.objs: List[Block] = []
        self.block_dict: Dict[str,Block] = {}
        self.active_obj: Optional[Block] = None
        self.make_more = True
        self.selected_option = OPTIONS[0]

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
                            if self.make_more:
                                self.create_block(self.selected_option, event.pos)
                            else:
                                pass
                        elif pygame.mouse.get_pressed()[2]:
                            pass# print(*self.block_dict,sep="\n")
                        
                elif event.type == pygame.MOUSEBUTTONUP:    
                    if pygame.MOUSEBUTTONUP:
                        pass

                elif event.type == pygame.MOUSEWHEEL:
                    if event.y > 0:
                        print("Scrolled up")
                        self.scale_all_elements(-10,-1)
                    elif event.y < 0:
                        print("Scrolled down")
                        self.scale_all_elements(10,1)

            self.update_objs()
            self.draw_window()

        pygame.quit()

    def save_xml(self):
        # TODO: make a upload_xml funcionality base on xml.etree.ElementTree (faster for upload?)
        doc = MD.Document()
        module = doc.createElement("testmodule")
        doc.appendChild(module)

        for obj in self.objs:
            obj_xml = obj.create_xml_element(doc, obj)
            module.appendChild(obj_xml)
        
        xml_str = doc.toprettyxml(indent="    ")
        with open("output.xml", "w") as f:
            f.write(xml_str)
        print("XML file saved!")

    def upload_xml(self,xml_file):
        tree = ET.parse(xml_file)
        module = tree.getroot()
        # self.active_obj = None
        objects = []

        for name in OPTIONS:
            for idx,obj_xml in enumerate(module.findall(name)):
                pos = (idx * 30,idx * 30)
                block = Block(self.window,name,pos,BLOCK_SIZE[name])
                block.load_from_xml(self.window,obj_xml)
                self.block_dict[block.id] = block
                objects.append(block)
                self.objs.sort()

        self.objs = objects

    def create_block(self, name, pos):
        try:
            if name in OPTIONS:
                block = Block(self.window,name,pos,BLOCK_SIZE[name])
            else:
                raise ValueError(f"Invalid block name {name}.")
            self.block_dict[block.id] = block
            self.active_obj = block
            self.active_obj.active = True
            self.objs.append(self.active_obj)
            self.objs.sort()

        except ValueError as e:
            print(f"Error: {str(e)}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def delete_block(self,block_id):
        pass
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
                        # print(f"Add {self.active_obj.id} as a child to {obj.id}")
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

        if self.objs != None: 
            for obj in reversed(self.objs):
                obj.draw_on(self.window)
                # pygame.display.update(obj.rect)
        pygame.display.flip()

    def scale_all_elements(self, scale_value, font_scale):
        Block.scale += scale_value
        Block.font_size += font_scale
            
        for obj in self.objs:
            obj.scale_block(scale_value,Block.font_size)

def queue_event_handle(object: Game):
    try:
        message = PY_QUEUE.get_nowait()
        # Process the message as needed
        if isinstance(message, dict) and "action" in message:

            if message["action"] == "update_option":
                object.selected_option = message["selected_option"]
                # print(f"update_option: {message}")
            print(f"Message received: {message}")    
            if message["action"] == "update_block":
                message.pop("action")
                block = game.block_dict[message.pop("block")]
                while message:
                    param, value = message.popitem()
                    block.params[param] = value
                    block.update_render_text(param,Block.font_size)
            print(f"Message received: {message}")
            if "zoom" in message:
                if message["zoom"] == "+":
                    object.scale_all_elements(10,1)
                elif message["zoom"] == "-":
                    object.scale_all_elements(-10,-1)
        # Handle other message types if needed
    except queue.Empty:
        pass #print("Queue is empty")
    except queue.Full:
        print("Queue is full")

# Function to run the game in a separate thread
def pygame_thread_obj():
    print("pygame_thread_obj")
    pygame.display.init()
    global game
    game = Game()
    gui_window.set_window(game)
    game.run()

def main():
    global gui_window
    global window

    gui_window = TkinterGui()
    window = pygame.display.set_mode((PY_WINDOW_WIDTH, PY_WINDOW_HEIGHT))

    pygame_thread = threading.Thread(target=pygame_thread_obj)
    pygame_thread.daemon = True
    pygame_thread.start()

    gui_window.run_gui()

if __name__ == "__main__":
    print("mian start")
    main()
print("OUT")