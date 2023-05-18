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

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                # Create a new block at the mouse position
                block_rect = pygame.Rect(event.pos[0], event.pos[1], 100, 50)
                block = {
                    "rect": block_rect,
                    "params": {}
                }
                blocks.append(block)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Generate and save the XML file
                root = ET.Element("root")
                for block in blocks:
                    block_elem = ET.SubElement(root, "block")
                    for param_name, param_value in block["params"].items():
                        block_elem.set(param_name, param_value)
                xml_tree = ET.ElementTree(root)
                xml_tree.write("output.xml", encoding="utf-8", xml_declaration=True)
                print("XML file saved!")

    # Update block positions
    for block in blocks:
        if pygame.mouse.get_pressed()[0]:  # Left mouse button pressed
            if block["rect"].collidepoint(pygame.mouse.get_pos()):
                # Move the block with the mouse cursor
                block["rect"].center = pygame.mouse.get_pos()

    # Clear the window
    window.fill(BLACK)

    # Draw the blocks
    for block in blocks:
        pygame.draw.rect(window, WHITE, block["rect"])

    # Update the display
    pygame.display.flip()

# Quit the game
pygame.quit()
