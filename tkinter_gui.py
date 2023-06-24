from consts import *
import os
import tkinter as tk
from tkinter import ttk
from Block import Block
from main import Game
class TkinterGui:
    label_row_count = 0
    def __init__(self):
        self.window: Game
        self.root = tk.Tk()
        
        self.container = tk.Frame(self.root,width=GUI_WINDOW_WIDTH, height=GUI_WINDOW_HEIGHT,background="gray12")
        self.container.grid(sticky="nsew")

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.embed = tk.Frame(self.container, width=PY_WINDOW_WIDTH, height=PY_WINDOW_HEIGHT,background="gray12")
        os.environ['SDL_WINDOWID'] = str(self.embed.winfo_id())
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        self.embed.grid(row=0, column=0, sticky="nsew")
        
        self.box = tk.Frame(self.container,width=600, height=GUI_WINDOW_HEIGHT, background="peach puff")
        self.box.columnconfigure(0, weight=1)
        self.box.columnconfigure(1, weight=3)
        self.box.grid(row=0, column=1, sticky="nsew")
        
        self.footer = tk.Frame(self.root,width=GUI_WINDOW_WIDTH, height=100, background="#f84018")
        self.footer.grid(row=1, column=0, columnspan=6, sticky="ew")
        # Configure grid weights for the footer frame
        self.footer.grid_columnconfigure(0, weight=1)
        self.footer.grid_columnconfigure(1, weight=1)
        self.footer.grid_columnconfigure(2, weight=1)
        self.footer.grid_columnconfigure(3, weight=1)
        self.footer.grid_columnconfigure(4, weight=2)
        self.widgets: List[tuple[tk.Label,ttk.Entry]] = []

        self.block_id = tk.Label(self.box,text="Block ID:",relief="groove")
        self.block_id.grid(column=0,columnspan=2,row=0,padx=PADDING_LABEL_X,pady=PADDING_LABEL_Y)
        TkinterGui.label_row_count+=1

        for parameter in BLOCK_PARAMETERS:
            self.widgets.append( self.set_lab_and_enter(f"{parameter}:",TkinterGui.label_row_count) )

        for idx,widget in enumerate(self.widgets):
            widget[1].bind('<Return>', lambda event, nr=idx: self.handle_enter(event, nr))

        self.button1 = self.set_button(parent=self.footer,option=0,_row=0,_col=0,_padx=(5,0),_pady=(5,5),_sticky="nsew")
        self.button2 = self.set_button(parent=self.footer,option=1,_row=0,_col=1,_padx=(5,0),_pady=(5,5),_sticky="nsew")
        self.button3 = self.set_button(parent=self.footer,option=2,_row=0,_col=2,_padx=(5,0),_pady=(5,5),_sticky="nsew")

        self.save_button = tk.Button(self.footer, text="Save", command=lambda: self.window.save_xml())
        self.save_button.grid(row=0,column=4,padx=(0,5),pady=(5,5),sticky="nsew")

        self.button1.configure(activebackground="black")
    
    def run_gui(self):
        self.root.after(100, self.process_message_queue)
        self.root.mainloop()
    
    def set_window(self, _window: Game):
        self.window = _window

    def set_button(self,parent=None,option=0,_row=0,_col=0,_padx=(0,0),_pady=(0,0),_sticky="nw"):
        button = tk.Button(parent, text=OPTIONS[option].upper(), command=lambda: update_option(option))
        if _sticky == None:
            button.grid(column=_col,row=_row,padx=_padx,pady=_pady)
        else:
            button.grid(column=_col,row=_row,padx=_padx,pady=_pady,sticky=_sticky)
        return button
    
    def set_label(self,_text: str,_row=0,_col=0):
        label = tk.Label(self.box,text=_text,relief="groove",justify="left",anchor="w",width=10)
        label.grid(column=_col,row=_row,padx=PADDING_LABEL_X,pady=PADDING_LABEL_Y)
        TkinterGui.label_row_count+=1
        return label
    
    def set_entery(self,_row=0,_col=0):
        entry = ttk.Entry(self.box)
        entry.grid(column=_col, row=_row, sticky=tk.E, padx=PADDING_ENTER_X, pady=PADDING_ENTER_Y)
        return entry
    
    def set_lab_and_enter(self,_text,_row=0,_col=0) -> tuple[tk.Label,ttk.Entry]:
        next_row = TkinterGui.label_row_count
        if TkinterGui.label_row_count == 0:
            label = self.set_label(_text,_row,_col)
            enter = self.set_entery(_row,_col+1)
        else:
            label = self.set_label(_text,next_row,_col)
            enter = self.set_entery(next_row,_col+1)
            TkinterGui.label_row_count+=1
        return (label,enter)
    
    def handle_enter(self, event, nr: int):
        text = self.widgets[nr][1].get()
        # Do something with the entered text

        print("Entered text in nr", nr, ":", text)

    def process_message_queue(self):
        # print("gui queue run")
        try:
            message = GUI_QUEUE.get_nowait()
            # Process the message as needed
            if isinstance(message, dict) and "action" in message:
                if message["action"] == "update_gui":
                    message.pop("action")
                    for widget in self.widgets:
                        widget[1].delete(0, tk.END)
                        widget[1].grid_forget()
                        widget[0].grid_forget()

                    self.block_id.configure(text=f"Block ID: {message.pop('id')}")
                    self.block_id.grid(column=0,columnspan=2,row=0,padx=PADDING_LABEL_X,pady=PADDING_LABEL_Y)

                    for idx,mes in enumerate(message):
                        self.widgets[idx][0].configure(text=f"{mes.capitalize()}: ",justify="left",anchor="w",width=10)
                        self.widgets[idx][1].insert(0,message[mes])
                        self.widgets[idx][0].grid(row=idx+1,column=0,padx=PADDING_LABEL_X,pady=PADDING_LABEL_Y,sticky="nsew")
                        self.widgets[idx][1].grid(row=idx+1,column=1, sticky=tk.E, padx=PADDING_ENTER_X, pady=PADDING_ENTER_Y)

                    print("queueue {x}".format(x=message))
            # Handle other message types if needed
        except queue.Empty:
            pass
        except queue.Full:
            pass  
        self.root.after(100, self.process_message_queue)

def update_gui(object: Block):
    item = {"action": "update_gui"}
    item["id"] = object.id
    for param in object.params:
        item[param] = object.params[param]
    GUI_QUEUE.put(item)
    print({object.id})
    
# Function to update the variables of the Block object
def update_block(parameter,new_value):
    # Update the variables of the Game object here
    PY_QUEUE.put({"action": "update_block", parameter: new_value})
    print(f"update: {new_value}")

# def update_block(block_id):
#     PY_QUEUE.put({"action": "update_block", "parameter": OPTIONS[option]})
#     print({OPTIONS[option]})