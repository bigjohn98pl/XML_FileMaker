import pygame
import xml.etree.ElementTree as ET
import uuid

# Initialize Pygame
pygame.init()

# Set up the window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("XML Block Editor")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# List to store the blocks
blocks = []

# Button parameters
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 30
BUTTON_COLOR = (100, 100, 100)
BUTTON_TEXT_COLOR = WHITE

# Create the "Save" button
save_button_rect = pygame.Rect(
    WINDOW_WIDTH - BUTTON_WIDTH - 10,
    WINDOW_HEIGHT - BUTTON_HEIGHT - 10,
    BUTTON_WIDTH,
    BUTTON_HEIGHT
)

# Create the "Toggle Shape" button
toggle_button_rect = pygame.Rect(
    WINDOW_WIDTH - BUTTON_WIDTH - 10,
    WINDOW_HEIGHT - BUTTON_HEIGHT * 2 - 20,
    BUTTON_WIDTH,
    BUTTON_HEIGHT
)
is_rectangle = True

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if save_button_rect.collidepoint(event.pos):
                    # Generate and save the XML file
                    root = ET.Element("root")
                    for block in blocks:
                        block_elem = ET.SubElement(root, "block")
                        block_elem.set("id", block["id"])  # Set the ID attribute
                        for param_name, param_value in block["params"].items():
                            block_elem.set(param_name, param_value)
                    xml_tree = ET.ElementTree(root)
                    xml_tree.write("output.xml", encoding="utf-8", xml_declaration=True)
                    print("XML file saved!")
                elif toggle_button_rect.collidepoint(event.pos):
                    # Toggle between rectangle and circle shapes
                    is_rectangle = not is_rectangle
                else:
                    # Create a new block at the mouse position with a unique ID
                    block_shape = pygame.Rect(event.pos[0], event.pos[1], 100, 50) if is_rectangle else pygame.Rect(
                        event.pos[0], event.pos[1], 50, 50)
                    block = {
                        "id": str(uuid.uuid4()),  # Generate a unique ID
                        "shape": block_shape,
                        "params": {}
                    }
                    blocks.append(block)

    # Update block positions
    for block in blocks:
        if pygame.mouse.get_pressed()[0]:  # Left mouse button pressed
            if block["shape"].collidepoint(pygame.mouse.get_pos()):
                # Move the block with the mouse cursor
                block["shape"].center = pygame.mouse.get_pos()

    # Clear the window
    window.fill(BLACK)

    # Draw the blocks
    for block in blocks:
        if is_rectangle:
            pygame.draw.rect(window, WHITE, block["shape"])
        else:
            pygame.draw.ellipse(window, WHITE, block["shape"])

    # Draw the "Save" button
    pygame.draw.rect(window, BUTTON_COLOR, save_button_rect)
    save_font = pygame.font.Font(None, 24)
    save_text = save_font.render("Save", True, BUTTON_TEXT_COLOR)
    save_text_rect = save_text.get_rect(center=save_button_rect.center)
    window.blit(save_text, save_text_rect)

    # Draw the "Toggle Shape" button
    pygame.draw.rect(window, BUTTON_COLOR, toggle_button_rect)
    toggle_font = pygame.font.Font(None, 24)
    toggle_text = toggle_font.render("Toggle", True, BUTTON_TEXT_COLOR)
    toggle_text_rect = toggle_text.get_rect(center=toggle_button_rect.center)
    window.blit(toggle_text, toggle_text_rect)

    # Update the display
    pygame.display.flip()

# Quit the game
pygame.quit()
