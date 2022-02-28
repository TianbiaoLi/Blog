import pandas as pd
import numpy as np

#读取数据

# 文件绝对路径
# path = 'C:/Users/litianbiao/Desktop/选址/单节点重心法.xlsx'
# data = pd.DataFrame(pd.read_excel(path))

# 文件相对路径
data = pd.DataFrame(pd.read_excel('单节点重心法.xlsx'))

point_volume = list(data['运输量'])
point_sita = list(data['费率'])
point_x = list(data['x'])
point_y = list(data['y'])

#计算初始中心
def first_center(point_volume, point_sita, point_x, point_y):
    x0 = sum(np.multiply(np.multiply(point_volume, point_sita),point_x))/sum(np.multiply(point_volume, point_sita))
    y0 = sum(np.multiply(np.multiply(point_volume, point_sita),point_y))/sum(np.multiply(point_volume, point_sita))
    return x0,y0

#计算中心点到各点距离
def center_distence(x, y, point_x, point_y):
    D = []
    for i in range(len(point_x)):
        D.append(pow(pow(x-point_x[i],2)+pow(y-point_y[i],2),0.5))
    return D

#计算新中心点
def new_center(point_volume, point_sita, point_x, point_y, D):
    x_new = sum(np.divide(np.multiply(np.multiply(point_volume, point_sita),point_x),D))/sum(np.divide(np.multiply(point_volume, point_sita),D))
    y_new = sum(np.divide(np.multiply(np.multiply(point_volume, point_sita),point_y),D))/sum(np.divide(np.multiply(point_volume, point_sita),D))
    return x_new,y_new

zuobiao = [] # 记录中心坐标变化
#（1）计算初始中心点
x0,y0 = first_center(point_volume, point_sita, point_x, point_y)
zuobiao.append([x0,y0])

# （2）计算中心点到各点距离
D = center_distence(x0, y0, point_x, point_y)
# （3）修正中心坐标值
x_new, y_new = new_center(point_volume, point_sita, point_x, point_y, D)
zuobiao.append([x_new, y_new])

#两次迭代x坐标精度<0.01则停止迭代
while abs(zuobiao[len(zuobiao)-1][0] - zuobiao[len(zuobiao)-2][0]) > 0.01:
	#重复（2）计算中心点到各点距离
	D = center_distence(x_new, y_new, point_x, point_y)
	#重复（3）修正中心坐标值
	x_new,y_new = new_center(point_volume, point_sita, point_x, point_y, D)
	zuobiao.append([x_new, y_new])

#输出迭代过程
print('节点迭代记录：\n' , zuobiao)
print('最终重心坐标为：\n [%.2f,' % zuobiao[-1][0], '%.2f]' % zuobiao[-1][-1])