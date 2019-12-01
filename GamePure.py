from STATE import State
import random
import pygame
import copy
import time


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
        self.board_init()
        path = self.solver_1()
        counter = 0
        # 游戏主循环
        while True:
            # 延时32毫秒,相当于FPS=30
            pygame.time.delay(200)
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
            if counter + 1 > len(path):
                time.sleep(60)
            draw_temp = path[counter]
            counter = counter + 1

            # 生成绘图所需要的块
            for y_id in range(3):
                for x_id in range(3):
                    # i = self.map[y][x]
                    i = draw_temp[y_id][x_id]
                    if i == 0:  # 0号图块不用绘制
                        continue
                    dx = (i % 3) * 166  # 计算绘图偏移量
                    dy = (int(i / 3)) * 166
                    self.s.blit(self.img, (x_id * 166, y_id * 166), (dx, dy, 166, 166))
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
        s = pygame.display.set_mode((1100, 600))
        # 随机地图
        self.rand_map()
        # self.map = [
        #     [7, 5, 1], [4, 8, 3], [2, 6, 0]
        # ]
        self.map = [
            [2, 5, 1], [7, 4, 3], [6, 0, 8]
        ]
        return s

    # 游戏的单击事件
    def click(self, x, y):
        if y - 1 >= 0 and self.map[y - 1][x] == 0:
            self.map[y][x], self.map[y - 1][x] = self.map[y - 1][x], self.map[y][x]
        elif y + 1 <= 2 and self.map[y + 1][x] == 0:
            self.map[y][x], self.map[y + 1][x] = self.map[y + 1][x], self.map[y][x]
        elif x - 1 >= 0 and self.map[y][x - 1] == 0:
            self.map[y][x], self.map[y][x - 1] = self.map[y][x - 1], self.map[y][x]
        elif x + 1 <= 2 and self.map[y][x + 1] == 0:
            self.map[y][x], self.map[y][x + 1] = self.map[y][x + 1], self.map[y][x]

    # 打乱地图
    def rand_map(self):
        for i in range(1000):
            x = random.randint(0, 2)
            y = random.randint(0, 2)
            self.click(x, y)

    def solver_1(self):
        temp_init = convert_zero_to_blank(copy.deepcopy(self.map))
        temp_win = convert_zero_to_blank(copy.deepcopy(self.win_map))
        state = State(temp_init, temp_win)
        path = state.solveProblem(temp_win)
        route = []
        # path的路径是相反的，记得要倒叙遍历
        for mat in reversed(path):
            route.append(convert_blank_to_zero(mat))
        return route


if __name__ == '__main__':
    # # 图片resize
    # imagePath = './emoji_2.jpeg'
    # img_PIL = Image.open(imagePath)
    # img_PIL = img_PIL.resize((500, 500))
    # img_PIL.save('test.jpeg')
    myGame = GameBoard('./test.jpeg')
    myGame.main()
