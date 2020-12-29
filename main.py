#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :  main.py
@Time    :  2020/12/28 15:38:03
@Author  :  Kearney
@Version :  0.0.0
@Contact :  191615342@qq.com
@License :  GPL 3.0
@Desc    :  贪吃蛇，基于python3-pygame
'''
import pygame
from pygame.locals import K_SPACE, K_UP, K_w, K_DOWN, K_s,\
    K_LEFT, K_a, K_RIGHT, K_d, K_ESCAPE

WIDTH = 960
HEIGHT = 640
SIZE = 40
LINEWIDTH = 1
FPS = 30

CBACK = (153, 255, 0)
CLINE = (0, 0, 255)
CSNAKE = (245, 245, 220)
CTARGET = (255, 0, 0)
POSITION = [[10, 5]]
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

if WIDTH % 40 == 0 and HEIGHT % 40 == 0:
    pass
else:
    print("Size not proper")

while True:
    screen.fill(CBACK)  # 清空画面为背景色

    # 绘制网格
    for x in range(SIZE, WIDTH, SIZE):
        pygame.draw.line(screen, CLINE, (x, 0), (x, HEIGHT), LINEWIDTH)
    for y in range(SIZE, HEIGHT, SIZE):
        pygame.draw.line(screen, CLINE, (0, y), (WIDTH, y), LINEWIDTH)

    # 绘制蛇头
    pygame.draw.rect(screen, CSNAKE,
                     (POSITION[0][0] * SIZE + 1, POSITION[0][1] * SIZE + 1,
                      SIZE - 1, SIZE - 1), 0)

    # 获取键盘输入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 右上角x 退出程序
            pygame.quit()
            exit(0)
        if event.type == pygame.KEYDOWN:  # 键盘事件
            if pygame.key.get_pressed()[K_SPACE]:
                print("space")
            elif pygame.key.get_pressed()[K_ESCAPE]:  # 键盘左上角Esc 退出程序
                print("esq")
                pygame.quit()
                exit(0)
            elif pygame.key.get_pressed()[K_UP] or pygame.key.get_pressed(
            )[K_w]:
                print("up")
                POSITION[0][1] -= 1
            elif pygame.key.get_pressed()[K_DOWN] or pygame.key.get_pressed(
            )[K_s]:
                print("down")
                POSITION[0][1] += 1
            elif pygame.key.get_pressed()[K_LEFT] or pygame.key.get_pressed(
            )[K_a]:
                print("left")
                POSITION[0][0] -= 1
            elif pygame.key.get_pressed()[K_RIGHT] or pygame.key.get_pressed(
            )[K_d]:
                print("Right")
                POSITION[0][0] += 1

    clock.tick(FPS)  # 以每秒30帧的速率进行绘制
    pygame.display.update()  # 更新画面
