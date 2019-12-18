import random
import pygame
import time
from PIL import Image
from STATE2 import State2
from Astar import *
from BFS import *


# 将矩阵中的空格字符替换成数字0
def convert_blank_to_zero(mat):
    for i in range(3):
        for j in range(3):
            if mat[i][j] == ' ':
                mat[i][j] = 0
    return mat


# 将矩阵中的空格字符替换成数字0
def convert_zero_to_blank(the_mat):
    for i in range(3):
        for j in range(3):
            if the_mat[i][j] == 0:
                the_mat[i][j] = ' '
    return the_mat


# 判断是否有解
def hasSolve(target, origate):
    targetVer = getreVersNum(target)
    orinateVer = getreVersNum(origate)
    if (targetVer % 2 != orinateVer % 2):
        return False
    else:
        return True


# 获取逆序数
def getreVersNum(state):
    sum = 0
    for i in range(0, len(state)):
        if (state[i] == 0):
            continue
        else:
            for j in range(0, i):
                if (state[j] > state[i]):
                    sum += 1
    return sum


# 将矩阵拉成一维的
def transistion(matix):
    temp = []
    for i in range(3):
        for j in range(3):
            if matix[i][j] == ' ':
                temp.append(0)
            else:
                temp.append(matix[i][j])
    return temp


class GameBoard:
    # 绘图地图
    init_map = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8]
    ]
    # 判断胜利的地图
    win_map = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8]
    ]
    # 图片的长宽
    map_width = 450
    # 切块的长款
    block_width = 150

    # 加载图片
    def __init__(self, img_path):
        self.img_path = img_path
        # 初始化左中右三张地图
        self.map_left = self.init_map
        self.map_middle = self.map_left
        self.map_right = self.map_left
        # 载入图片
        self.img = pygame.image.load(self.img_path)
        # 初始化图版
        self.s = self.board_init()

    def main(self):
        self.board_init()
        path_left, run_time_left = self.solver_1(self.map_left)
        path_right, run_time_right = self.solver_2(self.map_right)
        path_middle, run_time_middle = self.solver_3(self.map_middle)
        counter_left = 0
        counter_middle = 0
        counter_right = 0
        mouse_state = 'Start'
        # 游戏主循环
        while True:
            # 延时32毫秒,相当于FPS=30
            pygame.time.delay(400)
            for event in pygame.event.get():
                # 窗口的关闭事件
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:  # 鼠标单击事件
                    if pygame.mouse.get_pressed() == (1, 0, 0):  # 鼠标左键按下
                        mx, my = pygame.mouse.get_pos()  # 获得当前鼠标坐标
                        mouse_state = self.click_button(mx, my)
            print(mouse_state)

            # TODO 用于添加一个模块，可以通过点击对图片进行刷新重来
            if (not mouse_state) or mouse_state == 'NULL':
                qwq = 1
            elif mouse_state == 'Pause':
                qwq = 1
            elif mouse_state == 'Start':
                if self.map_left != self.win_map:
                    if counter_left + 1 < len(path_left):
                        counter_left = counter_left + 1
                if self.map_middle != self.win_map:
                    if counter_middle + 1 < len(path_middle):
                        counter_middle = counter_middle + 1
                if self.map_right != self.win_map:
                    if counter_right + 1 < len(path_right):
                        counter_right = counter_right + 1
            elif mouse_state == 'ReInit':
                self.board_init()
                path_left, run_time_left = self.solver_1(self.map_left)
                path_right, run_time_middle = self.solver_2(self.map_right)
                path_middle, run_time_right = self.solver_3(self.map_middle)
                counter_left = 0
                counter_middle = 0
                counter_right = 0

            # 更新绘图状态
            draw_temp_left = path_left[counter_left]
            draw_temp_middle = path_middle[counter_middle]
            draw_temp_right = path_right[counter_right]

            # 背景色填充成白色
            self.s.fill((255, 255, 255))

            # 生成左侧绘图所需要的块
            for y_id in range(3):
                for x_id in range(3):
                    i = draw_temp_left[y_id][x_id]
                    if i == 0:  # 0号图块不用绘制
                        continue
                    dx = (i % 3) * self.block_width  # 计算绘图偏移量
                    dy = (int(i / 3)) * self.block_width
                    self.s.blit(self.img, (x_id * self.block_width, y_id * self.block_width),
                                (dx, dy, self.block_width, self.block_width))

            # 生成中间绘图所需要的块
            for y_id in range(3):
                for x_id in range(3):
                    i = draw_temp_middle[y_id][x_id]
                    if i == 0:  # 0号图块不用绘制
                        continue
                    dx = (i % 3) * self.block_width  # 计算绘图偏移量
                    dy = (int(i / 3)) * self.block_width
                    self.s.blit(self.img, (x_id * self.block_width + 3*self.block_width, y_id * self.block_width),
                                (dx, dy, self.block_width, self.block_width))

            # 生成右侧绘图所需要的块
            for y_id in range(3):
                for x_id in range(3):
                    i = draw_temp_right[y_id][x_id]
                    if i == 0:  # 0号图块不用绘制
                        continue
                    dx = (i % 3) * self.block_width  # 计算绘图偏移量
                    dy = (int(i / 3)) * self.block_width
                    self.s.blit(self.img, (x_id * self.block_width + 6*self.block_width, y_id * self.block_width),
                                (dx, dy, self.block_width, self.block_width))

            # 画分割的直线
            for i in range(11):  # 纵向
                pygame.draw.line(self.s, (0, 0, 0), (self.block_width*i, 0), (self.block_width*i, self.map_width), 2)
            for i in range(4):  # 横向
                pygame.draw.line(self.s, (0, 0, 0), (0, self.block_width*i), (self.map_width*3, self.block_width*i), 2)

            # 绘制供给点击的矩形框
            # 开始按钮的绘制
            pygame.draw.rect(self.s, (88, 88, 88),
                             (self.block_width, self.map_width + 50, self.block_width, 50), 0)
            font = pygame.font.SysFont('microsoft Yahei', 60)
            surface = font.render('Start', True, (255, 200, 10))
            self.s.blit(surface, (self.block_width+24, self.map_width + 55))
            # 暂停按钮的绘制
            pygame.draw.rect(self.s, (88, 88, 88),
                             (self.block_width + self.map_width, self.map_width + 50, self.block_width, 50), 0)
            font = pygame.font.SysFont('microsoft Yahei', 60)
            surface = font.render('Pause', True, (255, 200, 10))
            self.s.blit(surface, (self.map_width + self.block_width+18, self.map_width + 55))
            # 刷新按钮的绘制
            pygame.draw.rect(self.s, (88, 88, 88),
                             (2*self.map_width + self.block_width, self.map_width + 50, self.block_width, 50), 0)
            font = pygame.font.SysFont('microsoft Yahei', 60)
            surface = font.render('ReInit', True, (255, 200, 10))
            self.s.blit(surface, (2*self.map_width + self.block_width+18, self.map_width + 55))

            # 刷新界面
            pygame.display.flip()

    def board_init(self):
        # 初始化
        pygame.init()
        # 窗口标题
        pygame.display.set_caption('拼图游戏')
        # 窗口大小
        s = pygame.display.set_mode((self.map_width*3, self.map_width+100))
        # 随机地图
        self.rand_map()
        # self.map_right = [
        #     [7, 5, 1], [4, 8, 3], [2, 6, 0]
        # ]
        # self.map_left = [
        #     [2, 5, 1], [7, 4, 3], [6, 0, 8]
        # ]
        # self.map_middle = self.map_left
        # self.map_right = self.map_left
        return s

    # 游戏的单击事件
    def click_button(self, x, y):
        if self.map_width + 50 <= y <= self.map_width + 100:
            if self.block_width <= x <= 2*self.block_width:
                state = 'Start'
            elif self.block_width + self.map_width <= x <= 2*self.block_width + self.map_width:
                state = 'Pause'
            elif 2*self.map_width + self.block_width <= x <= 2*self.map_width + 2*self.block_width:
                state = 'ReInit'
            else:
                state = 'NULL'
        return state

    def click_map(self, x, y):
        if y - 1 >= 0 and self.map_left[y - 1][x] == 0:
            self.map_left[y][x], self.map_left[y - 1][x] = self.map_left[y - 1][x], self.map_left[y][x]
            self.map_middle[y][x], self.map_middle[y - 1][x] = self.map_middle[y - 1][x], self.map_middle[y][x]
            self.map_right[y][x], self.map_right[y - 1][x] = self.map_right[y - 1][x], self.map_right[y][x]
        elif y + 1 <= 2 and self.map_left[y + 1][x] == 0:
            self.map_left[y][x], self.map_left[y + 1][x] = self.map_left[y + 1][x], self.map_left[y][x]
            self.map_middle[y][x], self.map_middle[y + 1][x] = self.map_middle[y + 1][x], self.map_middle[y][x]
            self.map_right[y][x], self.map_right[y + 1][x] = self.map_right[y + 1][x], self.map_right[y][x]
        elif x - 1 >= 0 and self.map_left[y][x - 1] == 0:
            self.map_left[y][x], self.map_left[y][x - 1] = self.map_left[y][x - 1], self.map_left[y][x]
            self.map_middle[y][x], self.map_middle[y][x - 1] = self.map_middle[y][x - 1], self.map_middle[y][x]
            self.map_right[y][x], self.map_right[y][x - 1] = self.map_right[y][x - 1], self.map_right[y][x]
        elif x + 1 <= 2 and self.map_right[y][x + 1] == 0:
            self.map_left[y][x], self.map_left[y][x + 1] = self.map_left[y][x + 1], self.map_left[y][x]
            self.map_middle[y][x], self.map_middle[y][x + 1] = self.map_middle[y][x + 1], self.map_middle[y][x]
            self.map_right[y][x], self.map_right[y][x + 1] = self.map_right[y][x + 1], self.map_right[y][x]

    # 打乱地图
    def rand_map(self):
        for i in range(30):
            x = random.randint(0, 2)
            y = random.randint(0, 2)
            self.click_map(x, y)

    def solver_1(self, the_map):
        temp_init = convert_zero_to_blank(copy.deepcopy(the_map))
        temp_win = convert_zero_to_blank(copy.deepcopy(self.win_map))
        stateList = transistion(temp_win)
        state = State2(temp_init, temp_win, stateList=stateList)
        path = state.solveProblem(temp_win)
        route = []
        # path的最后一个元素为程序求解的运行时间
        run_time = path.pop()
        # path的路径是相反的，记得要倒叙遍历
        for mat in reversed(path):
            route.append(convert_blank_to_zero(mat))
        return route, run_time

    def solver_2(self, the_map):
        temp_init = convert_zero_to_blank(copy.deepcopy(the_map))
        temp_win = convert_zero_to_blank(copy.deepcopy(self.win_map))
        ManhattanList = [[0, 1, 2, 1, 2, 3, 2, 3, 4], [1, 0, 1, 2, 1, 2, 3, 2, 3], [2, 1, 0, 3, 2, 1, 4, 3, 2],
                         [1, 2, 3, 0, 1, 2, 1, 2, 3], [2, 1, 2, 1, 0, 1, 2, 1, 2], [3, 2, 1, 2, 1, 0, 3, 2, 1],
                         [2, 3, 4, 1, 2, 3, 0, 1, 2], [3, 2, 3, 2, 1, 2, 1, 0, 1], [4, 3, 2, 3, 2, 1, 2, 1, 0]]
        stateList = transistion(temp_win)
        state = Astar(temp_init, temp_win, stateList=stateList, Manhattan=ManhattanList)
        path = state.solveproblemByAstar(temp_win)
        route = []
        # path的最后一个元素为程序求解的运行时间
        run_time = path.pop()
        # path的路径是相反的，记得要倒叙遍历
        for mat in reversed(path):
            route.append(convert_blank_to_zero(mat))
        return route, run_time

    def solver_3(self, the_map):
        temp_init = convert_zero_to_blank(copy.deepcopy(the_map))
        temp_win = convert_zero_to_blank(copy.deepcopy(self.win_map))
        stateList = transistion(temp_win)
        state = BFS(temp_init, temp_win, stateList=stateList)
        path = state.solveProblemByBFS(temp_win)
        route = []
        # path的最后一个元素为程序求解的运行时间
        run_time = path.pop()
        # path的路径是相反的，记得要倒叙遍历
        for mat in reversed(path):
            route.append(convert_blank_to_zero(mat))
        return route, run_time


if __name__ == '__main__':
    # # 图片resize
    imagePath = './emoji_2.jpeg'
    img_PIL = Image.open(imagePath)
    img_PIL = img_PIL.resize((450, 450))
    img_PIL.save('test.jpeg')
    myGame = GameBoard('./test.jpeg')
    myGame.main()
