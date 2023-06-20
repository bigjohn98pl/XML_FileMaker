from consts import *
import os
import tkinter as tk
from tkinter import ttk
from Block import Block
from main import Game
class TkinterGui:
    def __init__(self):
        self.window: Game
        self.root = tk.Tk()
        self.container = tk.Frame(self.root,width=GUI_WINDOW_WIDTH, height=GUI_WINDOW_HEIGHT,background="gray6")
        self.container.grid()

        self.embed = tk.Frame(self.container, width=PY_WINDOW_WIDTH, height=PY_WINDOW_HEIGHT,background="gray12")
        os.environ['SDL_WINDOWID'] = str(self.embed.winfo_id())
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        self.embed.grid(column=0,row=0,columnspan=1,rowspan=1,padx=(5,5),pady=(5,0))
        
        self.box = tk.Frame(self.container,width=GUI_WINDOW_WIDTH, height=GUI_WINDOW_HEIGHT, background="peach puff")
        self.box.columnconfigure(0, weight=1)
        self.box.columnconfigure(1, weight=3)
        self.box.grid(column=1,row=0,sticky="nwsw",padx=(0,5),pady=(5,0))
        

        # self.lab_id = self.set_label("ID:",0,0)
        # self.id_value = self.set_enter("None:",0,1)
        (self.lab_id,self.id_value) = self.set_lab_and_enter("ID:",0,0)
        (self.lab_position,self.position_value) = self.set_lab_and_enter("Position:",1,0)
        (self.lab_hover,self.hover_value) = self.set_lab_and_enter("Hover:",2,0)
        (self.lab_press,self.press_value) = self.set_lab_and_enter("Press:",3,0)
        (self.lab_size,self.size_value) = self.set_lab_and_enter("Size:",4,0)
        # self.lab_position = self.set_label("Position:",1,0)
        # self.position_value = self.set_enter("Children:",1,1)
        self.button1 = self.set_button(parent=self.box,option=0,_row=5,_col=0,_padx=(5,0),_pady=(5,5))
        self.button2 = self.set_button(parent=self.box,option=1,_row=6,_col=0,_padx=(5,0),_pady=(5,5))
        self.button3 = self.set_button(parent=self.box,option=2,_row=7,_col=0,_padx=(5,0),_pady=(5,5))

        self.save_button = tk.Button(self.container, text="Save", command=lambda: self.window.save_xml())
        self.save_button.grid(row=1,column=1,columnspan=2,padx=(0,5),pady=(5,5),sticky="ew")

        self.button1.configure(activebackground="black")
    
    def run_gui(self):
        self.root.after(100, self.process_message_queue)
        self.root.mainloop()
    
    def set_window(self, _window: Game):
        self.window = _window
    def set_button(self,parent=None,option=0,_row=0,_col=0,_padx=(0,0),_pady=(0,0)):
        button = tk.Button(parent, text=OPTIONS[option].upper(), command=lambda: update_option(option))
        button.grid(column=_col,row=_row,padx=_padx,pady=_pady,sticky="nsew")
        return button
    def set_label(self,_text,_row=0,_col=0):
        label = tk.Label(self.box,text=_text,relief="groove")
        label.grid(column=_col,row=_row,padx=PADDING_LABEL_X,pady=PADDING_LABEL_Y,sticky="nsew")
        return label
    def set_enter(self,_row=0,_col=0):
        entry = ttk.Entry(self.box)
        entry.grid(column=_col, row=_row, sticky=tk.E, padx=PADDING_ENTER_X, pady=PADDING_ENTER_Y)
        return entry
    def set_lab_and_enter(self,_text,_row=0,_col=0):
        label = self.set_label(_text,_row,_col)
        enter = self.set_enter(_row,_col+1)
        return (label,enter)
    def process_message_queue(self):
        print("gui queue run")
        try:
            message = GUI_QUEUE.get_nowait()
            # Process the message as needed
            if isinstance(message, dict) and "action" in message:
                if message["action"] == "update_gui":
                    self.id_value.delete(0, tk.END)
                    self.id_value.insert(0,message["id"])
                    self.position_value.delete(0, tk.END)
                    self.position_value.insert(0,message["position"])
                    self.hover_value.delete(0, tk.END)
                    self.hover_value.insert(0,message["hover"])
                    self.press_value.delete(0, tk.END)
                    self.press_value.insert(0,message["press"])
                    self.size_value.delete(0, tk.END)
                    self.size_value.insert(0,message["size"])
                    print("queueue {x}".format(x=message))
            # Handle other message types if needed
        except queue.Empty:
            pass
        except queue.Full:
            pass  
        self.root.after(100, self.process_message_queue)

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