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


class Board:
    def __init__(self, screen):
        self.coordinate = [[None for i in range(4)] for j in range(4)]
        self.screen = screen
        self.font = pygame.font.Font('arial.ttf', 40)
        self.save = list()

        self.spawn()
        self.spawn()
        self.render()

    def append_save(self, save):
        self.save.append(save)
        if len(self.save) > 100:
            self.save.pop(0)

    def spawn(self):
        while True:
            x = random.randrange(4)
            y = random.randrange(4)

            if self.coordinate[x][y] is None:
                if 0 <= random.randrange(10) <= 7:
                    self.coordinate[x][y] = 2
                else:
                    self.coordinate[x][y] = 4
                break

    def render(self):
        self.screen.fill(LINECOLOR)
        for x in range(4):
            for y in range(4):
                if self.coordinate[x][y] is None:
                    color = (255, 255, 255)
                else:
                    color = colormap[self.coordinate[x][y]]
                self.screen.fill(color, pygame.rect.Rect(5 + 105 * x, 5 + 105 * y, 100, 100))
                if self.coordinate[x][y] is not None:
                    surface = self.font.render(str(self.coordinate[x][y]), True, LINECOLOR, color)
                    rect = surface.get_rect(center=(55 + 105*x, 55 + 105*y))
                    self.screen.blit(surface, rect)
        pygame.display.flip()

    def check(self):
        count = 0
        test_board = Board(self.screen.copy())
        test_board.coordinate = copy.deepcopy(self.coordinate)
        if not test_board.up():
            count += 1
        test_board.coordinate = copy.deepcopy(self.coordinate)
        if not test_board.down():
            count += 1
        test_board.coordinate = copy.deepcopy(self.coordinate)
        if not test_board.left():
            count += 1
        test_board.coordinate = copy.deepcopy(self.coordinate)
        if not test_board.right():
            count += 1
        if count == 4:
            return True

    def up(self):
        stable = True
        save = copy.deepcopy(self.coordinate)
        for x in range(4):
            empty_phase = False
            for y in range(4):
                if self.coordinate[x][y] is None:
                    empty_phase = True
                elif empty_phase:
                    stable = False

        for x in range(4):
            old_list = list()
            new_list = list()

            for y in range(4):
                if self.coordinate[x][y] is not None:
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
            return False

        self.append_save(save)
        self.spawn()
        self.render()

        return True

    def down(self):
        stable = True
        save = copy.deepcopy(self.coordinate)
        for x in range(4):
            empty_phase = False
            for y in range(3, -1, -1):
                if self.coordinate[x][y] is None:
                    empty_phase = True
                elif empty_phase:
                    stable = False

        for x in range(4):
            old_list = list()
            new_list = list()

            for y in range(3, -1, -1):
                if self.coordinate[x][y] is not None:
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
            return False

        self.append_save(save)
        self.spawn()
        self.render()

        return True

    def left(self):
        stable = True
        save = copy.deepcopy(self.coordinate)
        for y in range(4):
            empty_phase = False
            for x in range(4):
                if self.coordinate[x][y] is None:
                    empty_phase = True
                elif empty_phase:
                    stable = False

        for y in range(4):
            old_list = list()
            new_list = list()

            for x in range(4):
                if self.coordinate[x][y] is not None:
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
            return False

        self.append_save(save)
        self.spawn()
        self.render()

        return True

    def right(self):
        stable = True
        save = copy.deepcopy(self.coordinate)
        for y in range(4):
            empty_phase = False
            for x in range(3, -1, -1):
                if self.coordinate[x][y] is None:
                    empty_phase = True
                elif empty_phase:
                    stable = False

        for y in range(4):
            old_list = list()
            new_list = list()

            for x in range(3, -1, -1):
                if self.coordinate[x][y] is not None:
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
            return False

        self.append_save(save)
        self.spawn()
        self.render()

        return True

    def load(self):
        if self.save:
            self.coordinate = self.save.pop(-1)
            self.render()


def main():
    pygame.init()
    pygame.display.set_icon(pygame.image.load('icon.png'))
    pygame.display.set_caption('2048')
    screen = pygame.display.set_mode((425, 425))
    board = Board(screen)

    game_over = False
    signal = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if game_over and event.key == pygame.K_SPACE:
                    board = Board(screen)
                    game_over = False
                elif event.key == pygame.K_UP:
                    if board.up() and board.check():
                        signal = True
                elif event.key == pygame.K_DOWN:
                    if board.down() and board.check():
                        signal = True
                elif event.key == pygame.K_LEFT:
                    if board.left() and board.check():
                        signal = True
                elif event.key == pygame.K_RIGHT:
                    if board.right() and board.check():
                        signal = True
                elif event.key == pygame.K_r:
                    board.load()

        if signal:
            signal = False
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