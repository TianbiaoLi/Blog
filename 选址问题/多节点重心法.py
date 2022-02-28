from unittest.mock import patch
import pandas as pd
import numpy as np

#读取数据

# 文件绝对路径
# path = 'C:/Users/litianbiao/Desktop/选址/多节点重心法.xlsx'
# data = pd.DataFrame(pd.read_excel(path))

# 文件相对路径
data = pd.DataFrame(pd.read_excel('多节点重心法.xlsx'))

volume_list = list(data['需求量'])
x_list = list(data['x'])
y_list = list(data['y'])


# 计算中心点到各点距离
def center_distence(x, y, x_list, y_list):
	D = []
	for i in range(len(x_list)):
		D.append(pow(pow(x - x_list[i], 2) + pow(y - y_list[i], 2), 0.5))
	return D

#对单组使用单重心法得到重心坐标
def single_point(volume_list, x_list, y_list):
	# 计算初始中心
	def first_center(volume_list, x_list, y_list):
		x0 = sum(np.multiply(volume_list, x_list)) / sum(volume_list)
		y0 = sum(np.multiply(volume_list, y_list)) / sum(volume_list)
		return x0, y0

	# # 计算中心点到各点距离
	# def center_distence(x, y, x_list, y_list):
	# 	D = []
	# 	for i in range(len(x_list)):
	# 		D.append(pow(pow(x - x_list[i], 2) + pow(y - y_list[i], 2), 0.5))
	# 	return D

	# 计算新中心点
	def new_center(volume_list, x_list, y_list, D):
		x_new = sum(np.divide(np.multiply(volume_list, x_list), D)) / sum(np.divide(volume_list, D))
		y_new = sum(np.divide(np.multiply(volume_list, y_list), D)) / sum(np.divide(volume_list, D))
		return x_new, y_new

	zuobiao = []
	# （1）计算初始中心点
	x0, y0 = first_center(volume_list, x_list, y_list)
	zuobiao.append([x0, y0])

	# （2）计算中心点到各点距离
	D = center_distence(x0, y0, x_list, y_list)

	# （3）修正中心坐标值
	x_new, y_new = new_center(volume_list, x_list, y_list, D)
	zuobiao.append([x_new, y_new])

	#循环计算重心，直到两次迭代精度差<0.01
	while abs(zuobiao[len(zuobiao) - 1][0] - zuobiao[len(zuobiao) - 2][0]) > 0.01:
		# 重复（2）计算中心点到各点距离
		D = center_distence(x_new, y_new, x_list, y_list)
		# 重复（3）修正中心坐标值
		x_new, y_new = new_center(volume_list, x_list, y_list, D)
		zuobiao.append([x_new, y_new])

	#返回重心坐标
	return zuobiao[len(zuobiao)-1]

#对数据进行初步分组
volume_list1 = volume_list[:5]
volume_list2 = volume_list[5:]
x_list1 = x_list[:5]
x_list2 = x_list[5:]
y_list1 = y_list[:5]
y_list2 = y_list[5:]


# 得到分别的重心
P1 = single_point(volume_list1, x_list1, y_list1)
P2 = single_point(volume_list2, x_list2, y_list2)


zuobiao = [] # 记录中心坐标变化
zuobiao.append(P1)
zuobiao.append(P2)

# 计算运输费用
def trans_cost(x, y, volume_list, x_list, y_list):
	D = center_distence(x, y, x_list, y_list)
	return np.multiply(volume_list, D)

while True :
	# # 得到分别的重心
	# P1 = single_point(point_volume1, x_list1, y_list1)
	# P2 = single_point(point_volume2, x_list2, y_list2)
	# print(P1, P2)

	# # 计算运输费用
	# def trans_cost(x, y, volume_list, x_list, y_list):
	# 	D = center_distence(x, y, x_list, y_list)
	# 	return np.multiply(volume_list, D)

	#计算运输费用
	C1 = trans_cost(P1[0], P1[1], volume_list, x_list, y_list)
	C2 = trans_cost(P2[0], P2[1], volume_list, x_list, y_list)

	#重新分组
	x_list1 = []
	x_list2 = []
	y_list1 = []
	y_list2 = []
	volume_list1 = []
	volume_list2 = []
	group1 = []
	group2 = []
	for i in range(len(x_list)):
		if C1[i] < C2[i]:
			x_list1.append(x_list[i])
			y_list1.append(y_list[i])
			volume_list1.append(volume_list[i])
			group1.append(i + 1)
		else:
			x_list2.append(x_list[i])
			y_list2.append(y_list[i])
			volume_list2.append(volume_list[i])
			group2.append(i + 1)

	# 得到分别的重心
	P1 = single_point(volume_list1, x_list1, y_list1)
	P2 = single_point(volume_list2, x_list2, y_list2)

	# zuobiao = []  # 记录中心坐标变化
	zuobiao.append(P1)
	zuobiao.append(P2)

	if abs(zuobiao[-1][0] - zuobiao[-3][0]) < 0.01 :
		break

#计算最终成本
C1 = sum(trans_cost(P1[0], P1[1], volume_list, x_list, y_list))
C2 = sum(trans_cost(P2[0], P2[1], volume_list, x_list, y_list))

#输出迭代过程
print('节点迭代记录：\n' , zuobiao,'\n----------------------------')
print('第一个配送点坐标为：\n P1:[%.2f,' % zuobiao[-2][0], '%.2f]' % zuobiao[-2][-1])
print('服务节点有：',group1)
print('----------------------------')
print('第二个配送点坐标为：\n P1:[%.2f,' % zuobiao[-1][0], '%.2f]' % zuobiao[-1][-1])
print('服务节点有：',group2)
print('----------------------------')
print('送货运输费用为：%.3f' % (C1+C2))
