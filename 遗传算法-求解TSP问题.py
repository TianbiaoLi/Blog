import matplotlib.pyplot as plt
import math
import random
import numpy as np
import time

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


# 生成节点坐标
def create_coordinate(port_num, x_range, y_range):
    x = []
    y = []
    for i in range(port_num):
        x1 = random.randint(0, x_range)
        y1 = random.randint(0, y_range)
        x.append(x1)
        y.append(y1)
    return x, y


# 生成种群基因
def creat_gene(port_num, size):
    all_point = [x for x in range(port_num)]
    allin = []
    for i in range(size):
        point_all = all_point[:]
        d = []
        for j in range(len(point_all)):
            c = len(point_all)
            b = random.randint(0, c - 1)
            a = point_all.pop(b)
            d.append(a)
        allin.append(d)
    return allin


# 展示路线图
def way(gene, x, y):
    xx = []
    yy = []
    for i in gene:
        xx.append(x[i])
        yy.append(y[i])
    plt.scatter(xx, yy, c='r', s=15)  # 生成散点图，每个点就是要展示的个体

    xx.append(xx[0])
    yy.append(yy[0])
    plt.plot(xx, yy)  # 生成函数图像
    plt.title("路线图")
    plt.show()  # 画出（展示）图像


# 计算适应度
def fitness(gene, x, y):
    fit = []
    for i in range(len(gene)):
        one_gene = gene[i]
        xx = []
        yy = []
        for j in one_gene:
            xx.append(x[j])
            yy.append(y[j])
        distence = 0
        for k in range(len(xx) - 1):
            dis = math.sqrt(pow((xx[k] - xx[k + 1]), 2) + pow((yy[k] - yy[k + 1]), 2))
            distence += dis
        distence = round(distence, 3)
        fit.append(distence)
    return fit


# 找出最优解
def best(gene, fit):
    value_y = min(fit)  # 找出y列表中的最小值
    value_x = gene[fit.index(value_y)]  # index()返回数值所在列表对应的索引值
    return value_x, value_y


# 轮盘赌选个体
def selection(gene, fit):
    value_rate = []
    fit_reciprocal = [1 / i for i in fit]  # 取倒数之后放大100倍，避免取倒之后相差过小

    # 适应度总和
    total_fit = sum(fit_reciprocal)

    # 归一化，使概率总和为1
    for i in range(len(fit_reciprocal)):
        value_rate.append(fit_reciprocal[i] / total_fit)
    value_rate = np.cumsum(value_rate)

    # 产生新种群个体的个数
    x_len = len(gene)

    # 轮盘赌每次的概率值
    ms = sorted([random.random() for i in range(x_len)])

    # 轮盘赌选出个体
    fitin = 0
    newin = 0
    new_gene = gene[:]
    # 转轮盘选择法
    while newin < x_len:
        # 如果这个概率大于随机出来的那个概率，就选这个
        if (ms[newin] < value_rate[fitin]):
            new_gene[newin] = gene[fitin]
            newin = newin + 1
        else:
            fitin = fitin + 1
    return new_gene


# 杂交
def crossover(gene, pc):
    # 一定概率杂交，主要是杂交种群种相邻的两个个体
    pop = gene[:]
    pop_len = len(pop)
    i = 0
    while i < pop_len:
        # 随机看看达到杂交概率没
        if (random.random() < pc):
            # 随机选取两个个体进行杂交
            rand1 = random.randint(0, len(pop) - 1)
            rand2 = random.randint(0, len(pop) - 1)

            # 随机选取杂交点
            cpoint = random.randint(1, len(gene[0]) - 1)

            # 路线不重复，因此
            out1 = gene[rand1]
            out2 = gene[rand2]

            part1 = out1[0:cpoint]
            part2 = out1[cpoint:]

            if out1 == out2:
                new1 = out1
                new2 = out2
            else:
                new11 = [i for i in out2 if i not in part1]
                new22 = [i for i in out2 if i not in part2]

                new1 = part1 + new11
                new2 = new22 + part2

            pop[i] = new1
            pop[i + 1] = new2
        i += 2
    return pop


# 基因突变(交换两个基因的位置)
def mutation(gene, pm):
    pop = gene[:]
    px = len(pop)
    py = len(pop[0])
    # py = 10
    # 每条染色体随便选一个杂交
    for i in range(px):
        if (random.random() < pm):
            mpoint1 = random.randint(0, py - 1)
            mpoint2 = random.randint(0, py - 1)
            a = pop[i][mpoint1]
            b = pop[i][mpoint2]
            pop[i][mpoint1] = b
            pop[i][mpoint2] = a
    return pop


# 查看迭代过程中结果变化
def plot_iter_curve(iter, results):
    X = [i for i in range(iter)]
    Y = [results[i] for i in range(iter)]
    plt.plot(X, Y)
    plt.title("各代最优解")
    plt.show()


# 主函数
def main():
    # 设置初始参数
    port_num = 10  # 节点的个数
    size = 500  # 种群个体数量
    iter = 200  # 演化代数
    pc = 0.8  # 杂交概率
    pm = 0.05  # 变异概率
    x_range = 500  # 节点所在范围
    y_range = 500

    # 生成节点坐标（随机生成或自定义）
    x = [330, 481, 405, 333, 261, 415, 207, 196, 170, 112]
    y = [339, 265, 286, 449, 105, 97, 481, 393, 206, 270]
    # x,y = create_coordinate(port_num, x_range, y_range)

    # 查看节点位置
    # plt.scatter(x,y, c='r', s=15) #生成散点图，每个点就是要展示的个体
    # plt.title("节点位置")
    # plt.show() #画出图像

    # print('x=',x)
    # print('y=',y)

    # 生成种群基因
    gene = creat_gene(port_num, size)

    # 记录每代最优个体
    best_x = []
    best_y = []

    # 进行迭代
    for i in range(iter):
        fit = fitness(gene, x, y)  # 计算适应度

        best_gene, best_fit = best(gene, fit)  # 找出当代最优解
        best_x.append(best_gene)
        best_y.append(best_fit)

        gene = selection(gene, fit)  # 选择新个体，更新基因
        gene = crossover(gene, pc)  # 杂交
        gene = mutation(gene, pm)  # 变异

    # 找出最优结果
    most_best_fit = min(best_y)
    most_best_gene = best_x[best_y.index(most_best_fit)]

    way(most_best_gene, x, y)  # 查看最终路径
    plot_iter_curve(iter, best_y)  # 查看各代最优解
    print('最优解为：\n路线:', most_best_gene, '\nD=', min(best_y), '米')

#多次运行，跑测试
def run_test(test_num):
    for test in range(test_num):
        print('第',test+1,'轮测试结果如下:')
        start_time = time.time()  # 记录程序开始运行时间
        main()
        end_time = time.time()  # 记录程序结束运行时间
        print('运行时间：%f 秒' % (end_time - start_time))
        print('————————————————————————————————————————————')

#设置进行几轮测试
run_test(3)