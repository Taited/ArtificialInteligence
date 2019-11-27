from PIL import Image
from STATE import State
import random
import pygame
import copy


# 将矩阵中的空格字符替换成数字0
def convert_blank_to_zero(the_mat):
    mat = copy.deepcopy(the_mat)
    for i in range(3):
        for j in range(3):
            if mat[i][j] == ' ':
                mat[i][j] = 0
    return mat


# 将矩阵中的空格字符替换成数字0
def convert_zero_to_blank(the_mat):
    mat = copy.deepcopy(the_mat)
    for i in range(3):
        for j in range(3):
            if mat[i][j] == 8:
                mat[i][j] = ' '
    return mat


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

    # 加载图片
    def __init__(self, img_path):
        self.img_path = img_path
        self.map = self.init_map
        self.img = pygame.image.load(self.img_path)
        # 初始化图版
        self.s = self.board_init()

    def main(self):
        # s = self.board_init()
        # self.draw_button(s)
        # path = self.solver_1(state)
        counter = 0
        # 游戏主循环
        while True:
            # 延时32毫秒,相当于FPS=30
            pygame.time.delay(32)
            for event in pygame.event.get():
                # 窗口的关闭事件
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:  # 鼠标单击事件
                    if pygame.mouse.get_pressed() == (1, 0, 0):  # 鼠标左键按下
                        mx, my = pygame.mouse.get_pos()  # 获得当前鼠标坐标
                        if mx < 498 and my < 498:  # 判断鼠标是否在操作范围内
                            x = int(mx / 166)  # 计算鼠标点到了哪个图块
                            y = int(my / 166)
                            self.click(x, y)  # 调用单击事件
                            if self.map == self.win_map:  # 如果当前地图情况和胜利情况相同,就print胜利
                                print("胜利了！")
            # 背景色填充成灰色
            self.s.fill((88, 88, 88))
            # 绘图
            for y in range(3):
                for x in range(3):
                    i = self.map[y][x]
                    if i == 8:  # 8号图块不用绘制
                        continue
                    dx = (i % 3) * 166  # 计算绘图偏移量
                    dy = (int(i / 3)) * 166
                    self.s.blit(self.img, (x * 166, y * 166), (dx, dy, 166, 166))
            # 画参考图片
            self.s.blit(self.img, (600, 0))
            # 刷新界面
            pygame.display.flip()

    def board_init(self):
        # 初始化
        pygame.init()
        # 窗口标题
        pygame.display.set_caption('拼图游戏')
        # 窗口大小
        s = pygame.display.set_mode((1100, 500))
        # 随机地图
        self.rand_map()
        return s

    # 游戏的单击事件
    def click(self, x, y):
        if y - 1 >= 0 and self.map[y - 1][x] == 8:
            self.map[y][x], self.map[y - 1][x] = self.map[y - 1][x], self.map[y][x]
        elif y + 1 <= 2 and self.map[y + 1][x] == 8:
            self.map[y][x], self.map[y + 1][x] = self.map[y + 1][x], self.map[y][x]
        elif x - 1 >= 0 and self.map[y][x - 1] == 8:
            self.map[y][x], self.map[y][x - 1] = self.map[y][x - 1], self.map[y][x]
        elif x + 1 <= 2 and self.map[y][x + 1] == 8:
            self.map[y][x], self.map[y][x + 1] = self.map[y][x + 1], self.map[y][x]

    # 打乱地图
    def rand_map(self):
        for i in range(1000):
            x = random.randint(0, 2)
            y = random.randint(0, 2)
            self.click(x, y)

    def draw_button(self, s):
        qwq = 1
        return qwq

    def get_init_map(self):
        return self.init_map

    def get_win_map(self):
        return self.win_map


def instantiating(init_map, win_map):
    temp_init = convert_zero_to_blank(init_map)
    temp_win = convert_zero_to_blank(win_map)
    state = State(temp_init, temp_win)
    path = state.solveProblem(temp_win)
    temp_init = convert_blank_to_zero(init_map)
    temp_win = convert_blank_to_zero(win_map)
    return path


if __name__ == '__main__':
    # # 图片resize
    # imagePath = './emoji_2.jpeg'
    # img_PIL = Image.open(imagePath)
    # img_PIL = img_PIL.resize((500, 500))
    # img_PIL.save('test.jpeg')
    myGame = GameBoard('./test.jpeg')
    path = instantiating(myGame.get_init_map(), myGame.get_win_map())
    # route = []
    # for mat in path:
    #     route.append(mat.state)
    myGame.main()
