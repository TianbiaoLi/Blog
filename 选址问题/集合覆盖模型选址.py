import pulp      # 导入 pulp 库

# 1.建立优化问题 SetCoverLP: 求最小值(LpMinimize)
SetCoverLP = pulp.LpProblem("Select_warehouse", sense=pulp.LpMinimize)  # 定义问题，求最小值
# 2. 建立变量
zones = list(range(7))  #  定义各区域[0,1,2,3,4,5,6]
x = pulp.LpVariable.dicts("A", zones, cat="Binary")  # 字典形式定义A_0~A_7,7个 0/1 变量，代表是否在该区域设配送点
# 3. 设置目标函数
SetCoverLP += pulp.lpSum([x[j] for j in range(7)])  # 目标函数为设置配送点的总个数
# 4. 施加约束
distences = [[0, 20, 15, 10000, 10000, 10000, 10000],
            [20, 0, 20, 15, 10000, 10000, 10000],
            [15, 20, 0, 30, 35, 10000, 40],
            [10000, 15, 30, 0, 25, 25, 10000],
            [10000, 10000, 35, 25, 0, 35, 25],
            [10000, 10000, 10000, 25, 35, 0, 30],
            [10000, 10000, 40, 10000, 25, 30, 0]]  # 距离矩阵，用于后面判断是否可达
reachable = [] # 可达矩阵
for i in range(len(distences)):
    reach = []
    for j in range(7):
        if distences[i][j] <= 30 :
            reach.append(1)
        else:
            reach.append(0)
    reachable.append(reach)  # 对于相互间距离<30的记为可达，标记为1

for i in range(7):
    SetCoverLP += pulp.lpSum([x[j]*reachable[j][i] for j in range(7)]) >= 1

# 5. 求解
SetCoverLP.solve()
# 6. 打印结果
print(SetCoverLP.name,'求解结果：')
temple = "区域 %(zone)d 的决策是：%(status)s"  # 格式化输出
if pulp.LpStatus[SetCoverLP.status] == "Optimal":  # 获得最优解
    for i in range(7):
        output = {'zone': i+1,  # 与问题中区域 1~7 一致
                    'status': '建站' if x[i].varValue else '--'}
        print(temple % output)
    print("需要建立 {} 个消防站。".format(pulp.value(SetCoverLP.objective)))