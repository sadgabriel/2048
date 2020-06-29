import random
import pygame
import os
import copy

os.environ['SDL_VIDEO_CENTERED'] = '1'


LINECOLOR = (15, 30, 170)
colormap = {2: (234, 242, 255), 4: (213, 228, 255), 8: (191, 216, 255), 16: (170, 202, 255),
            32: (149, 189, 255), 64: (128, 175, 255), 128: (106, 163, 255), 256: (85, 149, 255), 512: (64, 136, 225),
            1024: (43, 122, 255), 2048: (21, 109, 255), 4096: (0, 96, 255), 8192: (0, 88, 234), 16384: (0, 80, 213),
            32768: (0, 72, 191), 65536: (0, 64, 170), 131072: (0, 56, 149)}


class GameOverSignal(Exception):
    def __init__(self, string):
        super().__init__(string)


class Board:
    def __init__(self, screen):
        self.coordinate = [[None for i in range(4)] for j in range(4)]
        self.screen = screen
        self.font = pygame.font.Font('arial.ttf', 40)

        self.spawn()
        self.spawn()
        self.render()

    def is_empty(self, x, y):
        if self.coordinate[x][y] is None:
            return True
        return False

    def spawn(self):
        while True:
            x = random.randrange(4)
            y = random.randrange(4)

            if self.is_empty(x, y):
                if random.randrange(2) == 0:
                    self.coordinate[x][y] = 2
                else:
                    self.coordinate[x][y] = 4
                break
            else:
                game_over = True
                for x in range(4):
                    for y in range(4):
                        if self.is_empty(x, y):
                            game_over = False
                if game_over:
                    raise GameOverSignal('Game Over')

    def render(self):
        self.screen.fill(LINECOLOR)
        for x in range(4):
            for y in range(4):
                if self.is_empty(x, y):
                    color = (255, 255, 255)
                else:
                    color = colormap[self.coordinate[x][y]]
                self.screen.fill(color, pygame.rect.Rect(5 + 105 * x, 5 + 105 * y, 100, 100))
                if self.coordinate[x][y] is not None:
                    surface = self.font.render(str(self.coordinate[x][y]), True, LINECOLOR, color)
                    rect = surface.get_rect(center=(55 + 105*x, 55 + 105*y))
                    self.screen.blit(surface, rect)
        pygame.display.flip()

    def up(self):
        stable = True
        for x in range(4):
            empty_phase = False
            for y in range(4):
                if self.is_empty(x, y):
                    empty_phase = True
                elif empty_phase:
                    stable = False

        for x in range(4):
            old_list = list()
            new_list = list()

            for y in range(4):
                if not self.is_empty(x, y):
                    old_list.append(self.coordinate[x][y])

            while old_list:
                if len(old_list) == 1:
                    new_list.append(old_list.pop(0))
                    break
                if old_list[0] == old_list[1]:
                    new_list.append(old_list[0] * 2)
                    del old_list[0:2]
                    stable = False
                else:
                    new_list.append(old_list.pop(0))

            for y in range(4):
                self.coordinate[x][y] = None

            for y in range(len(new_list)):
                self.coordinate[x][y] = new_list[y]

        if stable:
            raise GameOverSignal('Game Over')
        else:
            self.spawn()
            self.render()

    def down(self):
        stable = True
        for x in range(3, -1, -1):
            empty_phase = False
            for y in range(3, -1, -1):
                if self.is_empty(x, y):
                    empty_phase = True
                elif empty_phase:
                    stable = False

        for x in range(4):
            old_list = list()
            new_list = list()

            for y in range(3, -1, -1):
                if not self.is_empty(x, y):
                    old_list.append(self.coordinate[x][y])

            while old_list:
                if len(old_list) == 1:
                    new_list.append(old_list.pop(0))
                    break
                if old_list[0] == old_list[1]:
                    new_list.append(old_list[0] * 2)
                    del old_list[0:2]
                    stable = False
                else:
                    new_list.append(old_list.pop(0))

            for y in range(4):
                self.coordinate[x][y] = None

            for y in range(len(new_list)):
                self.coordinate[x][3-y] = new_list[y]

        if stable:
            raise GameOverSignal('Game Over')
        else:
            self.spawn()
            self.render()

    def left(self):
        stable = True
        for y in range(4):
            empty_phase = False
            for x in range(4):
                if self.is_empty(x, y):
                    empty_phase = True
                elif empty_phase:
                    stable = False

        for y in range(4):
            old_list = list()
            new_list = list()

            for x in range(4):
                if not self.is_empty(x, y):
                    old_list.append(self.coordinate[x][y])

            while old_list:
                if len(old_list) == 1:
                    new_list.append(old_list.pop(0))
                    break
                if old_list[0] == old_list[1]:
                    new_list.append(old_list[0] * 2)
                    del old_list[0:2]
                    stable = False
                else:
                    new_list.append(old_list.pop(0))

            for x in range(4):
                self.coordinate[x][y] = None

            for x in range(len(new_list)):
                self.coordinate[x][y] = new_list[x]

        if stable:
            raise GameOverSignal('Game Over')
        else:
            self.spawn()
            self.render()

    def right(self):
        stable = True
        for y in range(3, -1, -1):
            empty_phase = False
            for x in range(3, -1, -1):
                if self.is_empty(x, y):
                    empty_phase = True
                elif empty_phase:
                    stable = False

        for y in range(4):
            old_list = list()
            new_list = list()

            for x in range(3, -1, -1):
                if not self.is_empty(x, y):
                    old_list.append(self.coordinate[x][y])

            while old_list:
                if len(old_list) == 1:
                    new_list.append(old_list.pop(0))
                    break
                if old_list[0] == old_list[1]:
                    new_list.append(old_list[0] * 2)
                    del old_list[0:2]
                    stable = False
                else:
                    new_list.append(old_list.pop(0))

            for x in range(4):
                self.coordinate[x][y] = None

            for x in range(len(new_list)):
                self.coordinate[3-x][y] = new_list[x]

        if stable:
            raise GameOverSignal('Game Over')
        else:
            self.spawn()
            self.render()


def main():
    pygame.init()
    pygame.display.set_icon(pygame.image.load('icon.png'))
    pygame.display.set_caption('2048')
    screen = pygame.display.set_mode((425, 425))
    board = Board(screen)

    game_over = False

    running = True
    while running:
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if game_over and event.key == pygame.K_SPACE:
                        board = Board(screen)
                        game_over = False
                    elif event.key == pygame.K_UP:
                        board.up()
                    elif event.key == pygame.K_DOWN:
                        board.down()
                    elif event.key == pygame.K_LEFT:
                        board.left()
                    elif event.key == pygame.K_RIGHT:
                        board.right()
        except GameOverSignal:
            raised_error = 0
            try:
                test_board = Board(pygame.Surface((425, 425)))
                test_board.coordinate = board.coordinate.copy()
                test_board.up()
            except GameOverSignal:
                raised_error += 1
            try:
                test_board = Board(pygame.Surface((425, 425)))
                test_board.coordinate = board.coordinate.copy()
                test_board.down()
            except GameOverSignal:
                raised_error += 1
            try:
                test_board = Board(pygame.Surface((425, 425)))
                test_board.coordinate = board.coordinate.copy()
                test_board.left()
            except GameOverSignal:
                raised_error += 1
            try:
                test_board = Board(pygame.Surface((425, 425)))
                test_board.coordinate = board.coordinate.copy()
                test_board.right()
            except GameOverSignal:
                raised_error += 1

            if raised_error == 4:
                game_over = True
                surface = pygame.font.Font('arial.ttf', 65).render('Game Over', True, (0, 0, 0))
                rect = surface.get_rect(center=(212, 180))
                screen.blit(surface, rect)

                surface = pygame.font.Font('arial.ttf', 25).render('Press space', True, (0, 0, 0))
                rect = surface.get_rect(center=(212, 240))
                screen.blit(surface, rect)
                pygame.display.flip()





if __name__ == '__main__':
    main()