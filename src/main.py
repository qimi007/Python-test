# coding=utf-8

import pygame
import time
import sys
import os
import random
from pygame.locals import *


# 对png图片处理


CMD = r'C:\Program Files (x86)\ImageMagick-6.2.7-Q16\convert.exe'
SOURCE_PATH = r'E:\WorkSpace\Python\Python-test\res\images'


def doStrip(path):
    data = {};
    print(path)
    for root, dirs, files in os.walk(path):
        for file in files:
            name = file.lower();
            if name.find('.png') != -1:
                path = os.path.join(root, file)
                print(path)
                os.system('"{0}" {1} -strip {1}'.format(CMD, path, path));


# 创建一个炮弹类，包括大炮和子弹
class Bullet(object):

    def __init__(self, feature, type, x, y):
        # 位置
        self.x = x
        self.y = y
        self.feature = feature
        self.image = self.loadFeature()
        self.size = self.image.get_size()
        self.type = type

    def __del__(self):
        print("the bullet is over")

    # 加载炮弹
    def loadFeature(self):
        return pygame.image.load(self.feature).convert_alpha()


    # 绘制炮弹
    def drawBullet(self, screen):
        screen.blit(self.image , (self.x, self.y))

    # 移动炮弹
    def moveBullet(self, screen, direct, speed):

        if direct == 'up':
            if self.y > 0 and self.y - speed < 0:
                self.y = -1
                self.drawBullet(screen)
            elif self.y <= 0:
                print("the bullet is more than edge")
                return -1
            else:
                self.y -= speed
                self.drawBullet(screen)
        else:
            # 子弹未接触到边缘
            # 子弹刚好接触到边缘
            if self.y + self.size[1] + speed <= screen.get_height():
                self.y += speed
                self.drawBullet(screen)
            # 子弹超过边缘
            elif self.y + self.size[1] >= screen.get_height():
                return -1
            # 子弹在边缘中
            else:
                self.y += speed
                self.drawBullet(screen)

        return 0
# 创建一个战斗机类
class Fighter(object):

    def __init__(self, feature, type, screen, x, y):
        # 战斗机类型是，敌机还是军机
        self.type = type
        # 战斗机样子
        self.feature = feature
        self.image = self.loadFighter()
        # 绘制场
        self.screen = screen
        # 位置
        self.x = x
        self.y = y
        # 移动速度
        self.speed = 5
        # 战斗机size(width ,height)
        self.size = self.image.get_size()
        # 炮弹
        self.bullet = []

    # 加载战斗机
    def loadFighter(self):
        return pygame.image.load(self.feature).convert_alpha()

    #移动战斗机
    def moveFighter(self , direct, speed):
        if direct == 'left':
            if self.x - speed <= 0:
                self.x = 0
                return -1
            else:
                self.x -= speed
        elif direct == 'right':
            if self.x + speed + self.size[0] >= self.screen.get_width():
                self.x = self.screen.get_width()- self.size[0]
                return -1
            else:
                self.x += speed
        elif direct == 'up':
            pass
        elif direct == 'down':
            pass

        return 0

    #绘制战斗机
    def drawFighter(self):
        self.screen.blit(self.image, (self.x, self.y))




# 敌机类
class EnemyFighter(Fighter):

    def __init__(self, feature, screen, x, y):
        self.edge = "left"
        Fighter.__init__(self, feature, 'enemy', screen, x, y)

    def __del__(self):
        print("EnemyFighter is over ...")


    # 自动移动
    def move(self):

        if self.edge == 'right':
             tmp = self.moveFighter('left', 10)
             if tmp == -1:
                 self.edge = 'left'
        else:
            tmp = self.edge = self.moveFighter('right', 10)
            if tmp == -1:
                self.edge = 'right'


# 程序从这里开始执行
if __name__ == "__main__":
    # print("hello world")
    # 处理png
    # doStrip(SOURCE_PATH)
    # sys.exit()
    # 创建一个窗口
    screen = pygame.display.set_mode((480, 700), 0, 0)
    # print(screen.get_size())

    # 加载一张图片
    bgFile = '../res/images/background.png'
    bgImage = pygame.image.load(bgFile).convert()
    # print(bgImage.get_width())

    #创建一个玩家
    player = Fighter('../res/images/me1.png', 'player', screen, 189, 570)
    # print(player.image.get_width())
    # 创建一个敌机
    enemy = EnemyFighter('../res/images/enemy1.png', screen, 0, 0)

    # 大循环
    while True:
        screen.blit(bgImage, (0, 0))

        for event in pygame.event.get():
            if event.type == QUIT:
                # print("quit")
                pygame.quit()
                sys.exit(-2)

            elif event.type == KEYDOWN:
                # print("detect key down")
                if event.key == K_a or event.key == K_LEFT:
                    print("left")
                    player.moveFighter('left', player.speed)
                elif event.key == K_d or event.key == K_RIGHT:
                    print("right")
                    player.moveFighter('right', player.speed)
                elif event.key == K_SPACE:
                    print("space")
                    player.bullet.append(Bullet('../res/images/bullet1.png', 'player',player.x+51 ,player.y-5))
                elif event.key == K_z:
                    print(player.bullet)
                    print(enemy.bullet)

        # 绘制子弹
        for tmp in player.bullet:
            # tmp.drawBullet(player.screen)
            # 先判断子弹是否存在
            if hasattr(tmp ,"moveBullet"):
               if tmp.moveBullet(screen, 'up', 5) == -1:
                   print("the bullet need delete")
                   player.bullet.remove(tmp)
                   del tmp
            else:
                # 不存在就删除
                print("bullet is not exist ...")
                player.bullet.remove(tmp)


        for tmp in enemy.bullet:
            # tmp.drawBullet(player.screen)
            # 先判断子弹是否存在
            if hasattr(tmp ,"moveBullet"):
               if tmp.moveBullet(screen, 'down', 5) == -1:
                   print("the bullet need delete")
                   enemy.bullet.remove(tmp)
                   del tmp
            else:
                # 不存在就删除
                print("bullet is not exist ...")
                enemy.bullet.remove(tmp)





        # 敌机移动
        tmp = random.randint(1, 100)
        if tmp in [30, 50, 70]:
            enemy.move()
        if tmp in [10, 90]:
            enemy.bullet.append(Bullet('../res/images/bullet2.png', 'enemy', enemy.x + 29, enemy.y + 45))

        #绘制玩家
        player.drawFighter()
        enemy.drawFighter()
        pygame.display.update()

        time.sleep(0.01)
