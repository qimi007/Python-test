#coding=utf-8

import pygame
import time

#程序从这里开始执行
if __name__ == "__main__":
    # print("hello world")

    #创建一个窗口
    screen = pygame.display.set_mode((480,890) ,0 , 0)

    #加载一张图片
    bgFile = '../res/images/background.png'
    bgImage = pygame.image.load(bgFile).convert()

    #大循环
    while True:
        screen.blit(bgImage , (0 , 0))


        pygame.display.update()

        time.sleep(0.01)

