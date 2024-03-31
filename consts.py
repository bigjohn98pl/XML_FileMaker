from typing import Literal, Tuple
from typing import List
from typing import Dict
from typing import Optional
from typing import Any
from math import floor
import queue

Color = Tuple[int, int, int]

# Colors
BLACK: Color       = (0, 0, 0)
GRAY: Color        = (128, 128, 128)
WHITE: Color       = (255, 255, 255)
RED: Color         = (255, 0, 0)
RED_LIGHT: Color   = (255, 77, 77)
BLUE: Color        = (102, 204, 255)
GREEN: Color       = (46, 184, 46)
YELLOW: Color      = (255, 204, 102)
PURPLE: Color      = (255, 0, 255)
DIM_FACTOR = 0.85
SCALE_FACTOR = 1.0
# Set up the window dimensions
PY_WINDOW_WIDTH    = 800
PY_WINDOW_HEIGHT   = 600
GUI_WINDOW_WIDTH    = 1200
GUI_WINDOW_HEIGHT   = 600
# Button parameters
BUTTON_WIDTH    = 100
BUTTON_HEIGHT   = 30
BUTTON_COLOR: Color= (100, 100, 100)
BUTTON_TEXT_COLOR = WHITE

# Options for tk window
OPTIONS = [
    "caplparam",
    "capltestcase",
    "testgroup",
    # "testmodule",
    # "None",
    ] #etc

SELECTED_OPTION = OPTIONS[0]
OPTIONS_NUM = {}
for idx,option in enumerate(OPTIONS):
    OPTIONS_NUM[idx] = OPTIONS[idx]

BLOCK_PARAMETERS = [
    "name",     #0
    "type",     #1
    "value",    #2
    "ident",    #3
    "title",    #4
    "func_name",#5
    "variants", #6
]

BLOCK_SIZE = {
    OPTIONS[0]      : (250, 20),
    OPTIONS[1]      : (260, 30),
    OPTIONS[2]      : (270, 40),
    # OPTIONS[4]      : (1,1),
}
MAP_NAME = {}
for idx,option in enumerate(OPTIONS):
    MAP_NAME[option] = idx

MAP_COLOR = {
    OPTIONS[0]  : BLUE,
    OPTIONS[1]  : RED_LIGHT,
    OPTIONS[2]  : YELLOW,
    # OPTIONS[4]  : GRAY,
}

MARGIN :int = 10
X_MARGIN :int= 20
TOP_MARGIN :int = 30
PADDING_LABEL_X = (5,0)
PADDING_LABEL_Y = (5,0)
PADDING_ENTER_X = (0,5)
PADDING_ENTER_Y = (5,0)

MOUSE_POS = (0,0)
# Create a queue for communication
PY_QUEUE :"queue.Queue[Dict[str, Any]]" = queue.Queue(10)
GUI_QUEUE :"queue.Queue[Dict[str, Any]]"= queue.Queue(10)

# Function to update the variables of the Game object
def update_option(option):
    # Update the variables of the Game object here
    PY_QUEUE.put({"action": "update_option", "selected_option": OPTIONS[option]})
    # print({OPTIONS[option]})
