import sys
import time

import pygame
import struct
from threading import Thread

import pygame.gfxdraw
import requests
from pygame.rect import Rect


SERV = ('http://127.0.0.1:8090/player/field_of_view')


class Requester(Thread):
    PL_FORMAT = 'ihh'

    def __init__(self, _map):
        super(Requester, self).__init__()
        self.setDaemon(True)
        self._map = _map
        self._pl_size = struct.calcsize(self.PL_FORMAT)
        self.start()
        print >> sys.stderr, "started"

    def run(self):
        while True:
            f_view = self._map.get_fov_rect()
            fov = f_view.topleft + f_view.bottomright
            buff = struct.pack('hhhh', *fov)
            print >> sys.stderr, "getting players"
            resp = requests.post(SERV, data=buff)
            cont = resp.content
            players = []

            for i in xrange(0, len(cont), self._pl_size):
                buff = struct.unpack('ihh', cont[i: i + self._pl_size])
                players.append(buff)
            print >> sys.stderr, "players len", len(players)
            context = Context()
            context.players = players
            self._map.set_context(context)
            time.sleep(0.01)


class Context(object):
    def __init__(self):
        self.players = []


class Map(object):
    def __init__(self, size):
        self.size = size
        self.myfont = pygame.font.SysFont("None", 11)

        self.pl_color = (0, 200, 145)
        self.fov_color = (254, 200, 0, 100)

        self.context = Context()
        self.n_context = None

        self.view_x, self.view_y = (0, 0)
        self.fov_rect = Rect(0, 0, 32, 32)

        self.fov_surf = pygame.Surface((self.fov_rect.w * 10, self.fov_rect.h * 10), pygame.SRCALPHA, 32)
        self.fov_surf.fill(self.fov_color, (0, 0, self.fov_rect.w * 10, self.fov_rect.h * 10))

    def set_context(self, context):
        """
        Called from thread
        :param context:
        :return:
        """
        self.n_context = context

    def update_context(self):
        if self.n_context and self.n_context is not self.context:
            self.context = self.n_context

    def get_fov_rect(self):
        return self.fov_rect

    def move_fov_down(self):
        self.fov_rect.y += 1
        self.fov_rect.y = min(512 - 32, self.fov_rect.y)
        if self.fov_rect.y > 15 and self.view_y < 512 - 49:
            self.view_y += 1

    def mov_fov_up(self):
        self.fov_rect.y -= 1
        self.fov_rect.y = max(0, self.fov_rect.y)
        if self.fov_rect.y < self.view_y and self.view_y > 0:
            self.view_y -= 1

    def mov_fov_right(self):
        self.fov_rect.x += 1
        self.fov_rect.x = min(512 - 32, self.fov_rect.x)
        if self.fov_rect.x > 15 and self.view_x < 512 - 49:
            self.view_x += 1

    def mov_fov_left(self):
        self.fov_rect.x -= 1
        self.fov_rect.x = max(0, self.fov_rect.x)
        if self.fov_rect.x < self.view_x and self.view_x > 0:
            self.view_x -= 1

    def draw(self, surf):
        for i in xrange(51):
            view_x_idx = str(self.view_x + i)
            view_y_idx = str(self.view_y + i)

            image_str_x = self.myfont.render(view_x_idx, 0, (0, 0, 0))
            image_str_y = self.myfont.render(view_y_idx, 0, (0, 0, 0))

            surf.blit(image_str_x, (10 + i * 10, 0))
            surf.blit(image_str_y, (0, 10 + i * 10))

            pygame.gfxdraw.hline(surf, 10, 511, i * 10 + 10, (0, 0, 0))
            pygame.gfxdraw.vline(surf, i * 10 + 10, 10, 511, (0, 0, 0))

        # pygame.draw.rect(surf, self.fov_color, self.fov_rect)
        surf.blit(self.fov_surf, ((self.fov_rect.x - self.view_x) * 10 + 10, (self.fov_rect.y - self.view_y) * 10 + 10))

        for pl in self.context.players:
            _, x, y = pl
            pygame.draw.rect(surf, self.pl_color, (10 + x * 10, 10 + y * 10, 10, 10))

        self.update_context()
        # pygame.gfxdraw.rectangle(surf, (10, 10, 100, 100), (0, 0, 0))


def main():
    pygame.init()

    screen = pygame.display.set_mode((800, 800), 0, 32)
    pygame.display.set_caption("Game")

    bgColor = (255, 255, 255)
    # fontImage = myFont.render(helloText, 0, (fontColor))
    mainLoop = True
    map = Map(0)
    Requester(map)

    pygame.key.set_repeat(30,30)

    while mainLoop:

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    map.mov_fov_up()

                elif event.key == pygame.K_DOWN:
                    map.move_fov_down()

                elif event.key == pygame.K_RIGHT:
                    map.mov_fov_right()

                elif event.key == pygame.K_LEFT:
                    map.mov_fov_left()

            elif event.type == pygame.QUIT:
                mainLoop = False
        screen.fill(bgColor)
        s = pygame.Surface((501, 501), pygame.SRCALPHA, 32)
        map.draw(s)

        screen.blit(s, (0, 0))
        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()