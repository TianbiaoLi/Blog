# python 3.8

import matplotlib.pyplot as plt
import math
import random
import numpy as np
import time

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


# 查看要处理函数
def plot_obj_func():
    """y = 10 * math.sin(5 * x) + 7 * math.cos(4 * x)"""
    X1 = [i / float(10) for i in range(0, 100, 1)]  # 自变量取值范围是0-10，因此以精度为0.1生成100个点，画图用
    Y1 = [10 * math.sin(5 * x) + 7 * math.cos(4 * x) for x in X1]  # 100个点对应的y值，画图用
    plt.plot(X1, Y1)  # 生成函数图像
    plt.title("所求函数图像")
    plt.show()  # 画出（展示）图像


# 生成size个范围在（start，end），小数位（精度）为bit的个体
def create_num(start, end, bit, size):
    listx = []  # 空列表，用来存放后面生成的x值

    # 产生规定范围内的小数集作为个体
    for i in range(size):  # 循环size次
        listx.append(
            round(random.uniform(start, end), bit))  # random.uniform()生成范围在[start,end]的浮点数，因为只要两位小数，通过round()函数设置保留小数位

    return listx  # 执行该函数之后，返回装有所有生成的x值的列表


# 计算适应度
def fitness(x):
    Y = [10 * math.sin(5 * i) + 7 * math.cos(4 * i) for i in x]  # 适应度即自变量对应的函数值，返回含有所有x对应的函数值的列表
    return Y


# 查看当前种群落点情况
def plot_currnt_individual(current_x, current_y):
    X1 = [i / float(10) for i in range(0, 100, 1)]
    Y1 = [10 * math.sin(5 * x) + 7 * math.cos(4 * x) for x in X1]
    plt.plot(X1, Y1)
    plt.scatter(current_x, current_y, c='r', s=5)  # 生成散点图，每个点就是要展示的个体
    plt.title("当前种群分布")
    plt.show()


# 淘汰
def calc_fit_value(value_y, mini):
    fit_value = []  # 存放经过淘汰后的个体

    c_min = mini  # 淘汰适应度小于mini的值，更改c_min会改变淘汰的下限。加大淘汰下限可以加快收敛，但过大可能影响全局最优的搜索

    for value in value_y:
        if value > c_min:
            temp = value
        else:
            temp = 0.
        fit_value.append(temp)
    # fit_value保存的是活下来的值
    return fit_value  # 返回经过淘汰之后种群的适应度情况，适应度变为0意味着被淘汰


# 找出当前最优解对应的x、y
def find_best(x, y):
    value_y = max(y)  # 找出y列表中的最大值
    value_x = x[y.index(value_y)]  # index()返回数值所在列表对应的索引值，因为x,y一一对应，因此其索引值也对应，通过y的索引值就能找到相应的x的值
    return value_x, value_y


# 轮盘赌选个体
def selection(now_x, now_value):
    value_rate = []

    # 适应度总和
    total_fit = sum(now_value)

    # 归一化，使概率总和为1
    for i in range(len(now_value)):
        value_rate.append(now_value[i] / total_fit)
    value_rate = np.cumsum(value_rate)

    # 产生新种群个体的个数
    x_len = len(now_x)

    # 轮盘赌每次的概率值
    ms = sorted([random.random() for i in range(x_len)])

    # 轮盘赌选出个体
    fitin = 0
    newin = 0
    new_gen = now_x
    # 转轮盘选择法
    while newin < x_len:
        # 如果这个概率大于随机出来的那个概率，就选这个
        if (ms[newin] < value_rate[fitin]):
            new_gen[newin] = now_x[fitin]
            newin = newin + 1
        else:
            fitin = fitin + 1
    x = new_gen


# 编码
def code(listx, end, bit, size):
    # 计算所需染色体长度
    len_gen = len(bin(end * 10 ** bit)) - 2

    # 将小数转化为相应的染色体编码
    gene = [round(100 * x) for x in listx]
    for i in range(size):
        gene[i] = bin(gene[i])[2:].rjust(len_gen, '0')  # 长度不足lens的，左边补0
    return gene


# 杂交
def crossover(pop, pc):
    # 一定概率杂交，主要是杂交种群种相邻的两个个体
    pop_len = len(pop)
    i = 0
    while i < pop_len:
        # 随机看看达到杂交概率没
        if (random.random() < pc):
            # 随机选取两个个体进行杂交
            rand1 = random.randint(0, len(pop) - 1)
            rand2 = random.randint(0, len(pop) - 1)

            # 随机选取杂交点，然后交换数组
            cpoint = random.randint(1, len(pop[0]) - 1)

            out1 = pop[rand1][0:cpoint]
            out2 = pop[rand1][cpoint:]
            out3 = pop[rand2][0:cpoint]
            out4 = pop[rand2][cpoint:]

            pop[i] = out1 + out4
            pop[i + 1] = out2 + out3
        i += 2


# 基因突变
def mutation(pop, pm):
    px = len(pop)
    py = len(pop[0])
    # py = 10
    # 每条染色体随便选一个杂交
    for i in range(px):
        if (random.random() < pm):
            mpoint = random.randint(0, py - 1)
            if (pop[i][mpoint] == 1):
                pop[i] = pop[i][:mpoint] + '0' + pop[i][mpoint + 1:]
                # pop[i][mpoint] = 0
            else:
                # pop[i][mpoint] = 1
                pop[i] = pop[i][:mpoint] + '1' + pop[i][mpoint + 1:]


# 解码
def decode(ones, bit):
    tens = []
    for i in range(len(ones)):
        ten = int(ones[i], 2)
        tens.append(ten)
    for i in range(len(ones)):
        tens[i] = tens[i] / 10 ** bit
    return tens


# 查看迭代过程中结果变化
def plot_iter_curve(iter, results):
    X = [i for i in range(iter)]
    Y = [results[i] for i in range(iter)]
    plt.plot(X, Y)
    plt.title("各代最优个体")
    plt.show()


# 主函数
def main():
    print('y = 10 * sin(5 * x) + 7 * cos(4 * x)')

    # 查看要处理的函数
    plot_obj_func()

    # 设置初始参数
    size = 500  # 种群数量
    start = 0  # 变量最小值
    end = 10  # 变量最大值
    bit = 2  # 变量精度
    iter = 500  # 演化代数
    pc = 0.6  # 杂交概率
    pm = 0.01  # 变异概率
    mini = 0  # 淘汰环节阈值（越大淘汰率越高）
    results = []  # 存储每一代的最优解，N个二元组
    # 记录每代最优个体
    best_x = []
    best_y = []
    x = create_num(start, end, bit, size)

    # 进行迭代
    for i in range(iter):
        y = fitness(x)  # 计算适应度

        # 每隔100代查看种群分布情况
        # plot_currnt_individual(x,y,i)

        fit_value = calc_fit_value(y, mini)  # 将个体适应度不好的（值小于某阈值的）归0，即在后续去掉该个体
        now_best_x, now_best_y = find_best(x, fit_value)  # 记录本代最优个体信息
        best_x.append(now_best_x)
        best_y.append(now_best_y)

        selection(x, fit_value)  # 选择新个体，更新x
        gene = code(x, end, bit, size)  # 获得个体(x)的染色体表示
        crossover(gene, pc)  # 交叉
        mutation(gene, pm)  # 变异
        x = decode(gene, bit)  # 获得新一代的种群
    plot_currnt_individual(x, fitness(x))  # 查看最终种群分布
    plot_iter_curve(iter, best_y)
    print('最优解为：\nx=', best_x[best_y.index(max(best_y))], 'y=', round(max(best_y), 3))

start_time = time.time()  # 记录程序开始运行时间
main()
end_time = time.time()  # 记录程序结束运行时间
print('运行时间：%f 秒' % (end_time - start_time))
