from consts import *
import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from Block import Block
from main import Game
class TkinterGui:
    label_row_count = 0
    def __init__(self):
        self.window: Game
        self.root = tk.Tk()
        
        # Create a menu bar
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        # Create a File menu
        file_menu = tk.Menu(menu_bar, tearoff=False)
        view_menu = tk.Menu(menu_bar, tearoff=False)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.file_new)
        file_menu.add_command(label="Open", command=self.file_open)
        file_menu.add_command(label="Save", command=self.file_save)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_app)

        menu_bar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Zoom in",command=self.view_zoom_in)
        view_menu.add_command(label="Zoom out",command=self.view_zoom_out)

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
        self.widgets: Dict[str,tuple[tk.Label,ttk.Entry]] = {}

        self.block_id = tk.Label(self.box,text="Block ID: ",relief="groove")
        self.block_id.grid(column=0,row=0,padx=PADDING_LABEL_X,pady=PADDING_LABEL_Y)
        self.block_id_value = tk.Label(self.box,text="None",relief="groove")
        self.block_id_value.grid(column=1,row=0,padx=PADDING_LABEL_X,pady=PADDING_LABEL_Y)
        TkinterGui.label_row_count+=1

        for parameter in BLOCK_PARAMETERS:
            self.widgets[parameter] = self.set_lab_and_enter(f"{parameter}:",parameter,TkinterGui.label_row_count)
            self.widgets[parameter][1].bind('<Return>', lambda event, name=parameter: self.handle_enter(event, name))       

        self.button1 = self.set_button(parent=self.footer,option=0,_row=0,_col=0,_padx=(5,0),_pady=(5,5),_sticky="nsew")
        self.button2 = self.set_button(parent=self.footer,option=1,_row=0,_col=1,_padx=(5,0),_pady=(5,5),_sticky="nsew")
        self.button3 = self.set_button(parent=self.footer,option=2,_row=0,_col=2,_padx=(5,0),_pady=(5,5),_sticky="nsew")
        
        self.save_button = tk.Button(self.footer, text="Save", command=self.file_save)
        self.save_button.grid(row=0,column=4,padx=(0,5),pady=(5,5),sticky="nsew")
    
    def file_new(self):
        print("New File")

    def file_open(self):
        print("Open File")
        file_path = filedialog.askopenfilename( initialdir="/__PROGRAMOWANIE_PROJEKTY__/__PYTHON__/XML_BlockMaker",
                                                filetypes=(("XML files", "*.xml"),("All files", "*.*")))
        self.window.upload_xml(file_path)

    def file_save(self):
        print("Save File")
        self.window.save_xml()

    def view_zoom_in(self):
        print("Zoom in")

    def view_zoom_out(self):
        print("Zoom out")

    def exit_app(self):
        self.root.destroy()

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
    
    def set_entery(self,_name="none",_row=0,_col=0):
        entry = ttk.Entry(self.box,name=_name)
        entry.grid(column=_col, row=_row, sticky=tk.E, padx=PADDING_ENTER_X, pady=PADDING_ENTER_Y)
        return entry
    
    def set_lab_and_enter(self,_text,_name="none",_row=0,_col=0) -> tuple[tk.Label,ttk.Entry]:
        next_row = TkinterGui.label_row_count
        if TkinterGui.label_row_count == 0:
            label = self.set_label(_text,_row,_col)
            enter = self.set_entery(_name,_row,_col+1)
        else:
            label = self.set_label(_text,next_row,_col)
            enter = self.set_entery(_name,next_row,_col+1)
            TkinterGui.label_row_count+=1
        return (label,enter)
    
    def handle_enter(self, event, para: str):
        widget: ttk.Entry = self.box.nametowidget(para)
        text = widget.get()
        block_id = self.block_id_value["text"]
        update_block(block_id,para,text)
        # Do something with the entered text

        print("Entered text in ", para, ":", text)

    def process_message_queue(self):
        # print("gui queue run")
        try:
            message = GUI_QUEUE.get_nowait()
            # Process the message as needed
            if isinstance(message, dict) and "action" in message:
                if message["action"] == "update_gui":
                    message.pop("action")
                    for key in self.widgets:
                        self.widgets[key][1].unbind('<Return>')
                        self.widgets[key][1].delete(0, tk.END)
                        self.widgets[key][1].grid_forget()
                        self.widgets[key][0].grid_forget()

                    self.block_id.configure(text="Block ID: ")
                    self.block_id.grid(column=0,row=0,padx=PADDING_LABEL_X,pady=PADDING_LABEL_Y)
                    self.block_id_value.configure(text=message.pop('id'))
                    self.block_id_value.grid(column=1,row=0,padx=PADDING_LABEL_X,pady=PADDING_LABEL_Y)

                    print("queueue gui: {x}".format(x=message))
                    for idx,mes in enumerate(message):
                        print(f"this is mes: {mes}")
                        self.widgets[mes][0].configure(text=f"{mes}: ",justify="left",anchor="w",width=10)
                        self.widgets[mes][1].insert(0,message[mes])
                        self.widgets[mes][1].widgetName = mes
                        print(f"name: {self.widgets[mes][1].winfo_name()}")
                        self.widgets[mes][1].bind('<Return>', lambda event, name=mes: self.handle_enter(event, name))
                        self.widgets[mes][0].grid(row=idx+1,column=0,padx=PADDING_LABEL_X,pady=PADDING_LABEL_Y,sticky="nsew")
                        self.widgets[mes][1].grid(row=idx+1,column=1, sticky=tk.E, padx=PADDING_ENTER_X, pady=PADDING_ENTER_Y)

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
def update_block(block_id,parameter,new_value):
    # Update the variables of the Game object here
    PY_QUEUE.put({"action": "update_block","block": block_id, parameter: new_value})
    print(f"update_block: {block_id} {parameter} {new_value}")
