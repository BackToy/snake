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
import copy
WIDTH = 960  # 窗体宽度
HEIGHT = 640  # 窗体高度
SIZE = 40  # 方格大小
LINEWIDTH = 1  # 线宽
FPS = 30  # 帧率

CBACK = (153, 255, 0)  # 背景色
CLINE = (0, 0, 255)  # 线条颜色
CSNAKE = (245, 245, 220)  # 蛇的颜色
CTARGET = (255, 0, 0)  # 目标颜色
POSITION = [[10, 3], [10, 4], [10, 5]]  # 蛇的身体坐标，列表中嵌套列表
DIRECTION = 3  # 方向，0～3 上下左右

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

if WIDTH % 40 == 0 and HEIGHT % 40 == 0:  # SIZE是否可以被整除
    pass
else:  # 无法整除就结束
    print("Size not proper")
    exit(0)

while True:
    screen.fill(CBACK)  # 清空画面为背景色

    # 绘制网格
    for x in range(SIZE, WIDTH, SIZE):
        pygame.draw.line(screen, CLINE, (x, 0), (x, HEIGHT), LINEWIDTH)
    for y in range(SIZE, HEIGHT, SIZE):
        pygame.draw.line(screen, CLINE, (0, y), (WIDTH, y), LINEWIDTH)

    # 绘制蛇
    tmp_len = len(POSITION)
    POSHEAD = tmp_len - 1  # 蛇头位于数组的第POSHEAD个位置
    for i in range(tmp_len):
        pygame.draw.rect(screen, CSNAKE,
                         (POSITION[i][0] * SIZE + 1, POSITION[i][1] * SIZE + 1,
                          SIZE - 1, SIZE - 1), 0)

    # 获取键盘输入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 右上角x 退出程序
            pygame.quit()
            exit(0)
        if event.type == pygame.KEYDOWN:  # 键盘事件，获取方向
            if event.key == K_SPACE:
                print("space")
            elif event.key == K_ESCAPE:  # 键盘左上角Esc 退出程序
                print("esq")
                pygame.quit()
                exit(0)
            elif event.key in (K_UP, K_w):
                DIRECTION = 0
            elif event.key in (K_DOWN, K_s):
                DIRECTION = 1
            elif event.key in (K_LEFT, K_a):
                DIRECTION = 2
            elif event.key in (K_RIGHT, K_d):
                DIRECTION = 3

    # 修改蛇的位置
    POSITION.reverse()  # 旋转、弹出蛇尾
    POSITION.pop()
    POSITION.reverse()
    tmp = copy.deepcopy(POSITION)  # 深拷贝
    if DIRECTION == 0:
        tmp[POSHEAD - 1][1] -= 1  # 蛇头位置变化
    elif DIRECTION == 1:
        tmp[POSHEAD - 1][1] += 1  # 蛇头位置变化
    elif DIRECTION == 2:
        tmp[POSHEAD - 1][0] -= 1  # 蛇头位置变化
    elif DIRECTION == 3:
        tmp[POSHEAD - 1][0] += 1  # 蛇头位置变化

    POSITION.append(tmp.pop())  # 添加蛇头

    clock.tick(FPS)  # 以每秒30帧的速率进行绘制
    pygame.display.update()  # 更新画面
