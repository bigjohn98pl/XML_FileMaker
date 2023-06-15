from consts import *
import os
import tkinter as tk
from tkinter import ttk
class TkinterGui:
    def __init__(self):
        self.root = tk.Tk()
        self.container = tk.Frame(self.root,width=GUI_WINDOW_WIDTH, height=GUI_WINDOW_HEIGHT,background="gray6")
        self.container.grid()

        self.embed = tk.Frame(self.container, width=PY_WINDOW_WIDTH, height=PY_WINDOW_HEIGHT,background="gray12")
        os.environ['SDL_WINDOWID'] = str(self.embed.winfo_id())
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        self.embed.grid(column=0,row=0,columnspan=1,rowspan=1)
        
        self.box = tk.Frame(self.container,width=GUI_WINDOW_WIDTH, height=GUI_WINDOW_HEIGHT, background="peach puff")
        self.box.columnconfigure(0, weight=1)
        self.box.columnconfigure(1, weight=3)
        self.box.grid(column=1,row=0,sticky="nwsw")
        

        # self.lab_id = self.set_label("ID:",0,0)
        # self.id_value = self.set_enter("None:",0,1)
        (self.lab_id,self.id_value) = self.set_lab_and_enter("ID",0,0)
        (self.lab_position,self.position_value) = self.set_lab_and_enter("Position",1,0)
        # self.lab_position = self.set_label("Position:",1,0)
        # self.position_value = self.set_enter("Children:",1,1)
        self.button1 = self.set_button(0,5,0)
        self.button2 = self.set_button(1,6,0)
        self.button3 = self.set_button(2,7,0)

        self.button1.configure(activebackground="black")
    
    def run_gui(self):
        self.root.after(100, self.process_message_queue)
        self.root.mainloop()
    
    def set_button(self,option,_row=0,_col=0):
        button = tk.Button(self.box, text=OPTIONS[option], command=lambda: update_option(option))
        button.grid(column=_col,row=_row,padx=10,pady=3,sticky=tk.S)
        return button
    def set_label(self,_text,_row=0,_col=0):
        label = tk.Label(self.box,text=_text)
        label.grid(column=_col,row=_row,padx=0,pady=0)
        return label
    def set_enter(self,_row=0,_col=0):
        entry = ttk.Entry(self.box)
        entry.grid(column=_col, row=_row, sticky=tk.E, padx=0, pady=0)
        entry
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
                    print("queueue {x}".format(x=message))
            # Handle other message types if needed
        except queue.Empty:
            pass
        except queue.Full:
            pass  
        self.root.after(100, self.process_message_queue)