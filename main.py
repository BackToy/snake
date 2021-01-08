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
    K_LEFT, K_a, K_RIGHT, K_d, K_ESCAPE, KEYUP
import random
import os

WIDTH = 960  # 窗体宽度
HEIGHT = 640  # 窗体高度
SIZE = 40  # 方格大小
NUMX = int(WIDTH / SIZE) - 1  # x、y轴方格子数-1
NUMY = int(HEIGHT / SIZE) - 1
TARGET = (random.randint(0, NUMX), random.randint(0, NUMY))  # 目标坐标
isEat = True  # 第一次生成目标也进行蛇身检测
isFail = False
isPause = False
LINEWIDTH = 1  # 线宽
FPS = 30  # 帧率
SPEED = 5  # 蛇的移动速度，小于FPS为好
TMPFRAME = 1  # 帧数计数器
SCORE = 0  # 得分
SCORE_MAX = 0  # 历史最高得分
FILE_SCORE = "./score.txt"

CBACK = (0, 0, 0)  # 背景色
CLINE = (255, 255, 255)  # 线条颜色
CSNAKE = (0, 245, 0)  # 蛇的颜色
CTARGET = (255, 0, 0)  # 目标颜色
CBLOCK = (50, 40, 60)  # 障碍物颜色
BLOCK1 = [(3, 9), (4, 9), (5, 9), (6, 9)]
POSITION = [(1, 3), (1, 4), (1, 5)]  # 蛇的身体坐标，列表中嵌套列表
DIRECTION = (1, 0)  # 方向，x方向变化量、y方向变化量
isMove = False


def drawgrid(SIZE, WIDTH, HEIGHT):
    """绘制网格
    参数
    ----------
    SIZE: 起点和步长
    WIDTH: 区域宽度
    HEIGHT: 区域高度
    """
    for x in range(SIZE, WIDTH, SIZE):
        pygame.draw.line(screen, CLINE, (x, 0), (x, HEIGHT), LINEWIDTH)
    for y in range(SIZE, HEIGHT, SIZE):
        pygame.draw.line(screen, CLINE, (0, y), (WIDTH, y), LINEWIDTH)


def savedata(filepath, data):
    """向文件里存储数据
    参数
    ----------
    filepath: 文件路径
    data: 要存储的数据
    """
    if os.path.exists(filepath):
        with open(filepath, "w") as f:
            try:
                f.write(str(data))
            except Exception as m:
                print("Warning： ", m, "， 存储最高得分失败")


def showStartScreen():
    """展示开场动画
    """
    titleFont = pygame.font.Font(None, 100)
    titleSurf1 = titleFont.render('Kearney!', True, CSNAKE, CTARGET)
    titleSurf2 = titleFont.render('Kearney!', True, CBACK)

    pressKeySurf = font.render('Press Any key to play.', True, CLINE)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WIDTH / 3, HEIGHT / 5)

    degrees1 = 0
    degrees2 = 0
    while True:
        screen.fill(CBACK)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WIDTH / 2, HEIGHT / 2)
        screen.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WIDTH / 2, HEIGHT / 2)
        screen.blit(rotatedSurf2, rotatedRect2)

        screen.blit(pressKeySurf, pressKeyRect)

        keyUpEvents = pygame.event.get(KEYUP)
        if len(keyUpEvents) > 0:  # 按下任意键退出
            pygame.event.get()  # 清空时间队列
            return
        pygame.display.update()
        clock.tick(FPS)
        degrees1 += 3  # rotate by 3 degrees each frame
        degrees2 += 7  # rotate by 7 degrees each frame


def terminate():
    """保存最高的分，退出程序
    """
    savedata(FILE_SCORE, SCORE_MAX)
    pygame.quit()
    exit(0)


def drawblock(screen, block, size, color):
    """绘制障碍物"""
    for i in range(len(block)):
        pygame.draw.rect(
            screen, color,
            (block[i][0] * size + 1, block[i][1] * size + 1, size, size), 0)


def draw():
    """绘制网格、障碍物、蛇、目标"""
    screen.fill(CBACK)  # 清空画面为背景色
    drawgrid(SIZE, WIDTH, HEIGHT)  # 绘制网格
    drawblock(screen, BLOCK1, SIZE, CBLOCK)  # 绘制障碍物
    for i in range(len(POSITION)):  # 绘制蛇
        pygame.draw.rect(screen, CSNAKE,
                         (POSITION[i][0] * SIZE + 1, POSITION[i][1] * SIZE + 1,
                          SIZE - 1, SIZE - 1), 0)
    # # 绘制目标
    pygame.draw.rect(
        screen, CTARGET,
        (TARGET[0] * SIZE + 1, TARGET[1] * SIZE + 1, SIZE - 1, SIZE - 1), 0)


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

MCRASH = "./src/sound/crash.ogg"  # 音频
MHIT = "./src/sound/gobble.ogg"  # 游戏失败音频

try:  # 初始化音频模块并载入音频文件
    pygame.mixer.init()
    MHIT = pygame.mixer.Sound(MHIT)
    MCRASH = pygame.mixer.Sound(MCRASH)
    global isload
    isMload = True
except Exception:
    print("温馨提示：请正确配置音频文件", Exception)

showStartScreen()

while True:
    for event in pygame.event.get():  # 获取键盘输入
        if event.type == pygame.QUIT:  # 右上角x 退出程序
            terminate()
        if event.type == pygame.KEYDOWN:  # 键盘事件，获取方向
            if event.key == K_SPACE:  # 暂停/重新开始
                isPause = not isPause  # 暂停
                if isFail:  # 失败了重新开始
                    POSITION = [(1, 3), (1, 4), (1, 5)]
                    DIRECTION = (1, 0)
                    SCORE = 0
                    while TARGET in POSITION or TARGET in BLOCK1:
                        TARGET = (random.randint(0, NUMX),
                                  random.randint(0, NUMY))
                    isFail = False
            elif event.key == K_ESCAPE:  # 键盘左上角Esc 退出程序
                terminate()
            elif event.key in (K_UP, K_w) and DIRECTION != (0, 1) and isMove:
                DIRECTION = (0, -1)
                isMove = False
            elif event.key in (K_DOWN,
                               K_s) and DIRECTION != (0, -1) and isMove:
                DIRECTION = (0, 1)
                isMove = False
            elif event.key in (K_LEFT, K_a) and DIRECTION != (1, 0) and isMove:
                DIRECTION = (-1, 0)
                isMove = False
            elif event.key in (K_RIGHT,
                               K_d) and DIRECTION != (-1, 0) and isMove:
                DIRECTION = (1, 0)
                isMove = False
    if not isPause:
        draw()
        if TMPFRAME % SPEED == 0 and not isFail:  # 修改蛇的位置、蛇与目标碰撞检测
            POSHEAD = len(POSITION) - 1  # 蛇头的位置
            nextPos = (POSITION[POSHEAD][0] + DIRECTION[0],
                       POSITION[POSHEAD][1] + DIRECTION[1])  # 蛇头的下一个位置
            POSITION.append(nextPos)  # 添加移动后的新蛇头
            # 边界检测
            if nextPos[0] < 0 or nextPos[0] > NUMX or nextPos[
                    1] < 0 or nextPos[1] > NUMY:
                isFail = True
                isPause = True
                MCRASH.play()
            # 障碍物碰撞检测
            if nextPos in BLOCK1:
                isFail = True
                isPause = True
                MCRASH.play()
            # 目标碰撞检测
            if nextPos == TARGET:
                while TARGET in POSITION or TARGET in BLOCK1:  # 生成新目标
                    TARGET = (random.randint(0, NUMX), random.randint(0, NUMY))
                SCORE += 1  # 分数加一
                MHIT.play()
                if SCORE > SCORE_MAX:
                    SCORE_MAX = SCORE
            else:  # 没吃到
                del POSITION[0]  # 删除旧蛇尾
            # 咬蛇自尽判断
            tmpHead = POSITION.pop()  # 蛇头
            if tmpHead in POSITION:
                isFail = True  # 咬到自己啦，结束
                isPause = True
            else:
                POSITION.append(tmpHead)
            isMove = True
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
