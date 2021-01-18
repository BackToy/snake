#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :  main.py
@Time    :  2020/12/28 15:38:03
@Author  :  Kearney
@Version :  0.0.1
@Contact :  191615342@qq.com
@License :  GPL 3.0
@Desc    :  贪吃蛇，基于python3-pygame
'''
import pygame
from pygame.locals import K_SPACE, K_UP, K_w, K_DOWN, K_s,\
    K_LEFT, K_a, K_RIGHT, K_d, K_ESCAPE
import random
import os
import pygame_menu

WIDTH = 960  # 窗体宽度
HEIGHT = 640  # 窗体高度
SIZE = 40  # 方格大小
isEat = True  # 第一次生成目标也进行蛇身检测
isFail = False
isPause = False
LINEWIDTH = 1  # 线宽
FPS = 30  # 帧率
SPEED = 8  # 蛇的移动速度，小于FPS为好
TMPFRAME = 1  # 帧数计数器
SCORE = 0  # 得分
SCORE_MAX = 0  # 历史最高得分
FILE_SCORE = "./score.txt"
isMload = False
CBACK = (0, 0, 0)  # 背景色
CLINE = (255, 255, 255)  # 线条颜色
CSNAKE = (0, 245, 0)  # 蛇的颜色
CTARGET = (255, 0, 0)  # 目标颜色
CBLOCK = (50, 40, 60)  # 障碍物颜色
BLOCK1 = []
isMove = False

ABOUT = [
    'Control: Use W/S/A/D or up/down/left/right',
    'Pause or Begin again: Space',
    'Quit: Esc',
    '',  # new line
    'Author: @Kearney',
    'Email: 191615342@qq.com',
    'web: https://gitee.com/back-toy/snake'
]
NSIZEUP = 2  # 上方空闲区域占用的格子数 >=0
NSIZEEL = 1  # 左右和下方空闲区域占用的格子数 >=0

XSTART = SIZE * NSIZEEL
XEND = WIDTH - SIZE * NSIZEEL
YSTART = SIZE * NSIZEUP
YEND = HEIGHT - SIZE * NSIZEEL

NUMX = int(WIDTH / SIZE) - NSIZEEL * 2  # 存活区域的格子数
NUMY = int(HEIGHT / SIZE) - NSIZEUP


def init():
    global POSITION, DIRECTION, SCORE, TARGET, isFail
    POSITION = [(NSIZEEL + 1, NSIZEUP + 3), (NSIZEEL + 1, NSIZEUP + 4),
                (NSIZEEL + 1, NSIZEUP + 5)]  # 蛇的身体坐标
    DIRECTION = (1, 0)  # 方向，x方向变化量、y方向变化量
    SCORE = 0
    # 目标坐标
    TARGET = (int(random.randint(XSTART, XEND) / SIZE),
              int(random.randint(YSTART, YEND) / SIZE))
    while TARGET in POSITION or TARGET in BLOCK1:
        TARGET = (int(random.randint(XSTART, XEND) / SIZE),
                  int(random.randint(YSTART, YEND) / SIZE))
    isFail = False


def set_speed(value, speed):
    """设置蛇的速度"""
    global SPEED
    if speed == 1:
        SPEED = 8
    elif speed == 2:
        SPEED = 6
    elif speed == 3:
        SPEED = 4


def set_difficulty(value, diff):
    """设置难度"""
    global BLOCK1
    if diff == 1:
        BLOCK1 = []
    elif diff == 2:
        BLOCK1 = [(3, 9), (4, 9), (5, 9), (6, 9)]


def drawgrid(SIZE, XSTART, XEND, YSTART, YEND, LINEWIDTH=1):
    """绘制网格
    参数
    ----------
    SIZE: 格子边长
    XSTART：左边线
    XEND：右边线
    YSTART：上边线
    YEND：下边线
    LINEWIDTH：线宽，默认为1
    """
    pygame.draw.line(screen, CLINE, (XSTART, YSTART), (XSTART, YEND),
                     LINEWIDTH)
    pygame.draw.line(screen, CLINE, (XSTART, YEND), (XEND, YEND), LINEWIDTH)
    pygame.draw.line(screen, CLINE, (XSTART, YSTART), (XEND, YSTART),
                     LINEWIDTH)
    pygame.draw.line(screen, CLINE, (XEND, YSTART), (XEND, YEND), LINEWIDTH)


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


def terminate():
    """保存最高的分，退出程序
    """
    savedata(FILE_SCORE, SCORE_MAX)
    pygame.quit()
    exit(0)


def drawblock(screen, block, size, color):
    """绘制方块"""
    for i in range(len(block)):
        pygame.draw.rect(
            screen, color,
            (block[i][0] * size + 1, block[i][1] * size + 1, size, size), 0)


def draw():
    """绘制网格、障碍物、蛇、目标"""
    screen.fill(CBACK)  # 清空画面为背景色
    drawgrid(SIZE, XSTART, XEND, YSTART, YEND)  # 绘制网格
    drawblock(screen, BLOCK1, SIZE, CBLOCK)  # 绘制障碍物
    drawblock(screen, POSITION, SIZE, CSNAKE)  # 绘制蛇
    # 绘制目标
    pygame.draw.rect(
        screen, CTARGET,
        (TARGET[0] * SIZE + 1, TARGET[1] * SIZE + 1, SIZE - 1, SIZE - 1), 0)


def start_the_game():
    init()
    global isPause, isFail, TMPFRAME, SCORE, SCORE_MAX, POSITION, DIRECTION,\
        TARGET, isMove
    while True:
        for event in pygame.event.get():  # 获取键盘输入
            if event.type == pygame.QUIT:  # 右上角x 退出程序
                terminate()
            if event.type == pygame.KEYDOWN:  # 键盘事件，获取方向
                if event.key == K_SPACE:  # 暂停/重新开始
                    isPause = not isPause  # 暂停
                    if isFail:  # 失败了重新开始
                        init()
                elif event.key == K_ESCAPE:  # 键盘左上角Esc 退出程序
                    terminate()
                elif event.key in (K_UP,
                                   K_w) and DIRECTION != (0, 1) and isMove:
                    DIRECTION = (0, -1)
                    isMove = False
                elif event.key in (K_DOWN,
                                   K_s) and DIRECTION != (0, -1) and isMove:
                    DIRECTION = (0, 1)
                    isMove = False
                elif event.key in (K_LEFT,
                                   K_a) and DIRECTION != (1, 0) and isMove:
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
                if nextPos[0] < NSIZEEL or nextPos[0] > NUMX or nextPos[
                        1] < NSIZEUP or nextPos[1] > NUMY:
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
                        TARGET = (int(random.randint(XSTART, XEND) / SIZE),
                                  int(random.randint(YSTART, YEND) / SIZE))
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


if os.path.exists(FILE_SCORE):
    with open(FILE_SCORE, "r") as f:
        try:
            SCORE_MAX = int(f.read())
        except Exception as m:
            print("Warning： ", m, "， 历史的得分不存在")
            SCORE_MAX = 0
else:
    try:
        os.mknod(FILE_SCORE)  # linux 有效，win无效
    except Exception as m:
        print('第一次尝试创建得分文件失败，错误提示： ', m)
        try:
            with open(FILE_SCORE, "w") as f:
                pass
            # print('第二次尝试创建得分文件成功')
        except Exception as m:
            print('第二次尝试创建得分文件失败，错误提示： ', m)
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 30)  # 得分字体，内置，不支持中文
fontBig = pygame.font.Font(None, 70)
pygame.display.set_caption("贪吃蛇")  # 窗口标题
ico = pygame.image.load("./src/img/snake.ico")
pygame.display.set_icon(ico)  # 图标
MCRASH = "./src/sound/crash.ogg"  # 音频
MHIT = "./src/sound/gobble.ogg"  # 游戏失败音频

try:  # 初始化音频模块并载入音频文件
    pygame.mixer.init()
    MHIT = pygame.mixer.Sound(MHIT)
    MCRASH = pygame.mixer.Sound(MCRASH)
    isMload = True
except Exception as m:
    print("温馨提示：请正确配置音频文件，异常提示： ", m)

# start_the_game()
about_menu = pygame_menu.Menu(height=HEIGHT,
                              width=WIDTH,
                              onclose=pygame_menu.events.DISABLE_CLOSE,
                              theme=pygame_menu.themes.THEME_SOLARIZED,
                              title='About')
for m in ABOUT:
    about_menu.add_label(m, align=pygame_menu.locals.ALIGN_LEFT, font_size=20)
about_menu.add_label('')
about_menu.add_button('Return to menu', pygame_menu.events.BACK)

menu = pygame_menu.Menu(HEIGHT,
                        WIDTH,
                        'Welcome to Snake',
                        theme=pygame_menu.themes.THEME_SOLARIZED)
menu.add_button('Play', start_the_game)

menu.add_selector('Speed :', [('Middle', 2), ('Slow', 1), ('Fast', 3)],
                  onchange=set_speed)
menu.add_selector('Difficulty :', [('Easy', 1), ('Little Hard', 2),
                                   ('Hard', 3)],
                  onchange=set_difficulty)
menu.add_button('About', about_menu)
menu.add_button('Quit', pygame_menu.events.PYGAME_QUIT)
menu.mainloop(screen)
