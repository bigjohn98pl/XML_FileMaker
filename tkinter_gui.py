from consts import *
import os
import tkinter as tk
import tkinter.ttk as ttk
class TkinterGui:
    def __init__(self):
        self.root = tk.Tk()
        self.embed = tk.Frame(self.root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        self.embed.grid(columnspan=600, rowspan=500)
        self.embed.pack(side=tk.LEFT)
        buttonwin = tk.Frame(self.root, width=75, height=WINDOW_HEIGHT)
        buttonwin.pack(side=tk.LEFT)

        os.environ['SDL_WINDOWID'] = str(self.embed.winfo_id())
        os.environ['SDL_VIDEODRIVER'] = 'windib'

        button1 = tk.Button(buttonwin, text=OPTIONS[0], command=lambda: update_option(0))
        button1.pack(side=tk.TOP)
        button2 = tk.Button(buttonwin, text=OPTIONS[1], command=lambda: update_option(1))
        button2.pack(side=tk.TOP)
        button3 = tk.Button(buttonwin, text=OPTIONS[2], command=lambda: update_option(2))
        button3.pack(side=tk.TOP)
    
    def run_gui(self):
        self.root.mainloop()