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
import random
import os

WIDTH = 960  # 窗体宽度
HEIGHT = 640  # 窗体高度
SIZE = 80  # 方格大小
NUMX = int(WIDTH / SIZE) - 1  # x、y轴方格子数-1
NUMY = int(HEIGHT / SIZE) - 1
TARGET = [random.randint(0, NUMX), random.randint(0, NUMY)]  # 目标坐标
isEat = False
isFail = False
isPause = False
LINEWIDTH = 1  # 线宽
FPS = 30  # 帧率
SPEED = FPS / 3  # 蛇的移动速度，小于FPS为好
TMPFRAME = 1  # 帧数计数器
SCORE = 0  # 得分
SCORE_MAX = 0  # 历史最高得分
FILE_SCORE = "./score.txt"

CBACK = (153, 255, 0)  # 背景色
CLINE = (0, 0, 255)  # 线条颜色
CSNAKE = (245, 245, 220)  # 蛇的颜色
CTARGET = (255, 0, 0)  # 目标颜色
POSITION = [[1, 3], [1, 4], [1, 5]]  # 蛇的身体坐标，列表中嵌套列表
DIRECTION = 3  # 方向，0～3 上下左右


def savedata(filepath, data):
    """
    向文件里存储数据
    """
    if os.path.exists(filepath):
        with open(filepath, "w") as f:
            try:
                f.write(str(data))
            except Exception as m:
                print("Warning： ", m, "， 存储最高得分失败")


if os.path.exists(FILE_SCORE):
    with open(FILE_SCORE, "r") as f:
        try:
            SCORE_MAX = int(f.read())
        except Exception as m:
            print("Warning： ", m, "， 历史的得分不存在")
            SCORE_MAX = 0
else:
    os.mknod(FILE_SCORE)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 30)  # 得分字体，内置，不支持中文
fontBig = pygame.font.Font(None, 70)

while True:
    screen.fill(CBACK)  # 清空画面为背景色

    if isEat:  # 被吃掉之后随机生成目标
        while True:
            try:
                POSITION.index(TARGET)  # 在队列里返回下标，不在则抛出异常
                TARGET[0] = random.randint(1, 3)
                TARGET[1] = random.randint(1, 6)
            except (Exception):
                break
        isEat = False

    # 绘制网格
    for x in range(SIZE, WIDTH, SIZE):
        pygame.draw.line(screen, CLINE, (x, 0), (x, HEIGHT), LINEWIDTH)
    for y in range(SIZE, HEIGHT, SIZE):
        pygame.draw.line(screen, CLINE, (0, y), (WIDTH, y), LINEWIDTH)

    # 绘制蛇 和 目标
    tmp_len = len(POSITION)
    POSHEAD = tmp_len - 2  # 现在蛇头位于数组的第（tmp_len-1）个位置
    for i in range(tmp_len):
        pygame.draw.rect(screen, CSNAKE,
                         (POSITION[i][0] * SIZE + 1, POSITION[i][1] * SIZE + 1,
                          SIZE - 1, SIZE - 1), 0)
    pygame.draw.rect(
        screen, CTARGET,
        (TARGET[0] * SIZE + 1, TARGET[1] * SIZE + 1, SIZE - 1, SIZE - 1), 0)

    # 咬蛇自尽判断
    try:
        tmp = copy.deepcopy(POSITION)
        tmpHead = tmp.pop()  # 蛇头
        tmp.index(tmpHead)  # 蛇头在蛇身里返回下标，不在则抛出异常
        isFail = True  # 咬到自己啦，结束
        isPause = True
    except (Exception):
        pass  # 没咬到自己

    # 获取键盘输入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 右上角x 退出程序
            pygame.quit()
            exit(0)
        if event.type == pygame.KEYDOWN:  # 键盘事件，获取方向
            if event.key == K_SPACE:
                isPause = not isPause  # 暂停
                if isFail:  # 失败了重新开始
                    POSITION = [[1, 3], [1, 4], [1, 5]]
                    DIRECTION = 3
                    SCORE = 0
                    while True:
                        try:
                            POSITION.index(TARGET)  # 在队列里返回下标，不在则抛出异常
                            TARGET[0] = random.randint(1, 3)
                            TARGET[1] = random.randint(1, 6)
                        except (Exception):
                            break
                    isFail = False

            elif event.key == K_ESCAPE:  # 键盘左上角Esc 退出程序
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
    if not isPause:
        if TMPFRAME % SPEED == 0 and not isFail:  # 修改蛇的位置、蛇与目标碰撞检测
            del POSITION[0]  # 删除旧蛇尾，现在蛇头位于数组的第（tmp_len-2）个位置
            tmp = copy.deepcopy(POSITION)  # 深拷贝
            if DIRECTION == 0:
                tmp[POSHEAD][1] -= 1  # 蛇头位置变化
            elif DIRECTION == 1:
                tmp[POSHEAD][1] += 1  # 蛇头位置变化
            elif DIRECTION == 2:
                tmp[POSHEAD][0] -= 1  # 蛇头位置变化
            elif DIRECTION == 3:
                tmp[POSHEAD][0] += 1  # 蛇头位置变化
            # 目标碰撞检测
            if tmp[POSHEAD][0] == TARGET[0] and tmp[POSHEAD][1] == TARGET[1]:
                isEat = True
                SCORE += 1  # 分数加一
                if SCORE > SCORE_MAX:
                    SCORE_MAX = SCORE
                    savedata(FILE_SCORE, SCORE_MAX)

            # 边框碰撞检测
            if tmp[POSHEAD][0] < 0 or tmp[POSHEAD][0] > NUMX or tmp[POSHEAD][
                    1] < 0 or tmp[POSHEAD][1] > NUMY:
                isFail = True
                isPause = True
            POSITION.append(tmp.pop())  # 添加移动后的新坐标
            if isEat:  # 吃掉目标后添加新蛇头坐标
                tmp = copy.deepcopy(POSITION)
                POSHEAD = len(POSITION) - 1
                if DIRECTION == 0:
                    tmp[POSHEAD][1] -= 1
                elif DIRECTION == 1:
                    tmp[POSHEAD][1] += 1
                elif DIRECTION == 2:
                    tmp[POSHEAD][0] -= 1
                elif DIRECTION == 3:
                    tmp[POSHEAD][0] += 1
                POSITION.append(tmp.pop())

            TMPFRAME = 1  # 重置，防止溢出
        TMPFRAME += 1

    if isFail:  # 显示Game Over
        screen.blit(fontBig.render("Game Over", True, CLINE),
                    (WIDTH / 3, HEIGHT / 2))
    # 显示分数
    tmpstr = "Score: " + str(SCORE) + "    Max Score: " + str(SCORE_MAX)
    imgText = font.render(tmpstr, True, CLINE)
    screen.blit(imgText, (0, 0))

    clock.tick(FPS)  # 以每秒30帧的速率进行绘制
    pygame.display.update()  # 更新画面
