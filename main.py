from typing import List, Optional
import pygame


class Block:
    count = 0

    def __init__(self, name: str, shape: pygame.Rect, params: Optional[dict] = None):
        self.name = name
        self.number = Block.count + 1
        self.id = f"{self.name}_{self.number}"
        self.shape = shape
        self.params = params or {}
        Block.count += 1


class GUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.is_rectangle = True
        self.blocks: List[Block] = []  # List of Block objects

    def create_block(self, name: str, pos: tuple[int, int]):
        shape = pygame.Rect(pos[0], pos[1], 100, 50) if self.is_rectangle else pygame.Rect(pos[0], pos[1], 50, 50)
        block = Block(name, shape)
        self.blocks.append(block)

    def draw_blocks(self):
        for block in self.blocks:
            pygame.draw.rect(self.screen, (255, 0, 0), block.shape)
            # You can add additional drawing code for different block shapes or parameters

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pos = pygame.mouse.get_pos()
                        self.create_block("Block", pos)

            self.screen.fill((255, 255, 255))
            self.draw_blocks()
            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()


gui = GUI()
gui.run()
