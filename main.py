import pygame
import xml.etree.ElementTree as ET

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
blocksCounter = 0
blockID = f"rect_{blocksCounter}"
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
                        block_elem = ET.SubElement(root, "rect_",block["params"])
                        for param_name, param_value in block["params"].items():
                            block_elem.set(param_name, param_value)
                    xml_tree = ET.ElementTree(root)
                    xml_tree.write("output.xml", encoding="utf-8", xml_declaration=True)
                    print("XML file saved!")
                else:
                    # Create a new block at the mouse position
                    
                    block_rect = pygame.Rect(event.pos[0], event.pos[1], 100, 50)
                    blocksCounter += 1
                    blockID = f"rect_{blocksCounter}"
                    block = {
                        "rect_": block_rect,
                        "params": {"position": block_rect.center}
                    }
                    blocks.append(block)

    # Clear the window
    window.fill(BLACK)

    # Update block positions
    for block in blocks:
        if pygame.mouse.get_pressed()[0]:  # Left mouse button pressed
            if block["rect_"].collidepoint(pygame.mouse.get_pos()):
                # Move the block with the mouse cursor
                block["rect_"].center = pygame.mouse.get_pos()
    # Draw the blocks
    for block in blocks:
        pygame.draw.rect(window, WHITE, block["rect_"])

    # Draw the "Save" button
    pygame.draw.rect(window, BUTTON_COLOR, save_button_rect)
    save_font = pygame.font.Font(None, 24)
    save_text = save_font.render("Save", True, BUTTON_TEXT_COLOR)
    save_text_rect = save_text.get_rect(center=save_button_rect.center)
    window.blit(save_text, save_text_rect)

    # Update the display
    pygame.display.flip()

# Quit the game
pygame.quit()
