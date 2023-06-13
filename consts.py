from typing import Literal, Tuple
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

DIM_FACTOR = 0.85
# Set up the window dimensions
WINDOW_WIDTH    = 800
WINDOW_HEIGHT   = 600

# Button parameters
BUTTON_WIDTH    = 100
BUTTON_HEIGHT   = 30
BUTTON_COLOR: Color= (100, 100, 100)
BUTTON_TEXT_COLOR = WHITE

# Options for tk window
OPTIONS = [
    "parameter",
    "testcase",
    "testcasegroup",
    "None",
    ] #etc
OPTIONS_NUM = {
    0 : OPTIONS[0],
    1 : OPTIONS[1],
    2 : OPTIONS[2],
    3 : OPTIONS[3],
 } #etc
SELECTED_OPTION = OPTIONS[0]
BLOCK_SIZE = {
    "testcasegroup" : (200, 200),
    "testcase"      : (150, 50),
    "parameter"     : (120, 40),
    "None"          : (1,1),
}

MAP_NAME = {
    "testcasegroup" : 2,
    "testcase"      : 1,
    "parameter"     : 0,
    "None"          : 3,
}
MAP_COLOR = {
    "testcasegroup" : YELLOW,
    "testcase"      : RED_LIGHT,
    "parameter"     : BLUE,
    "None"          : GRAY,
}
MOUSE_POS = (0,0)