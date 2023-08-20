import pygame
import random
import numpy as np

PURPLE = pygame.Color('#644172')
BLUE = pygame.Color('#236B8E')
GREEN = pygame.Color('#00FF00')
ORANGE = pygame.Color('#FF862F')


class Main(object):
    def __init__(self, r, k, width, height):

        # Pygame setup
        pygame.init()
        pygame.display.set_caption("Poisson-Disk")
        self.width, self.height = width, height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        # Variables
        self.r, self.k = r, k
        self.grid, self.active = [], []
        self.w = self.r / np.sqrt(2)

        self.cols = self.width // int(self.w)
        self.rows = self.height // int(self.w)
        self.grid = [None] * (self.cols * self.rows)
        # self.cols, self.rows = 0, 0

    def is_inside_canvas(self, x, y):
        ''' check if elements are inside the canvas'''
        return 0 <= x < self.width and 0 <= y < self.height

    def find_distance(self, position1, position2):
        '''find distance between position 1 and position 2 '''
        X = position1[0] - position2[0]
        Y = position1[1] - position2[1]
        diff = X*X + Y*Y
        distance = np.sqrt(diff)

        return distance

    def setup(self):
        ''' selecting a random point from the active list '''
        # global cols, rows, grid

        x = random.randint(0, self.width)
        y = random.randint(0, self.height)
        pos = (x, y)

        i = int(x / self.w)
        j = int(y / self.w)
        self.grid[i + j * self.cols] = pos
        self.active.append(pos)

    def main(self):
        ''' main function for poisson-disc distribution'''
        self.setup()

        while self.active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            rand_index = random.randint(0, len(self.active) - 1)
            pos = self.active[rand_index]
            found = False

            for n in range(self.k):
                angle = random.uniform(0, 2 * np.pi)
                m = random.uniform(self.r, 2 * self.r)
                sample_x = pos[0] + np.cos(angle) * m
                sample_y = pos[1] + np.sin(angle) * m
                sample = (sample_x, sample_y)

                col = int(sample_x / self.w)
                row = int(sample_y / self.w)

                ok = True
                if 0 <= col < self.cols and 0 <= row < self.rows:
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            new_col = col + i
                            new_row = row + j
                            if self.is_inside_canvas(new_col, new_row):
                                neighbor_index = new_col + new_row * self. cols
                                if 0 <= neighbor_index < len(self.grid):
                                    neighbor = self.grid[neighbor_index]
                                    if neighbor:
                                        d = self.find_distance(
                                            sample, neighbor)
                                        if d < self.r:
                                            ok = False
                                            break

                    if ok:
                        found = True
                        self.grid[col + row * self.cols] = sample
                        self.active.append(sample)
                        # break

            if not found:
                self.active.pop(rand_index)

            self.screen.fill((0, 0, 0))

            for point in self.grid:
                if point:
                    pygame.draw.circle(self.screen, GREEN,
                                       (int(point[0]), int(point[1])), 5)

            for point in self.active:
                pygame.draw.circle(self.screen, ORANGE,
                                   (int(point[0]), int(point[1])), 5)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
