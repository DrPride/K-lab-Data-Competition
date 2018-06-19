# -*-coding:utf-8 -*-
import os
import numpy as np

##滑窗法要求产生范围

RANGE = 51709
#RANGE = 2000
#最大五万，id的范围

#并无实际意义，表示滑窗法的时间范围
time_range = 7 
#训练集的起始终结点，三者要一起变化
start_date = 8
end_date = 14

matrix_result = np.array([np.zeros(20)])
matrix_count = np.array([np.zeros(time_range+1)])
test_date_range = 23
id_index_dict = {}
result_index = {'avg':1,'vari':2, 'ld_times':3, 'max':4, 
	'min':5, 'constant':6,'ld_sums':7,'Fre_Author':8,'con':9,'person':10,'discover':11,
	'same_city':12,'other':13,'play':14,'good':15,'con_action':16,'retweet':17,'report':18,'decline':19}

#arp表 id => index


def get_user_id(str):
	return np.int(str.split()[0])

def get_days_data(str):
	return np.int(str.split()[1])

def get_page_data(str):
	return np.int(str.split()[2])

def get_activity_type_data(str):
	return np.int(str.split()[5])

def Matrix_intial(RANGE, matrix1, matrix2, Xrange, Yrange, test_date_range):
	#extra_line = np.array(line1)
	#print(matrix,'\t')
	with open('a3d6_chusai_a_train\\user_register_log.txt') as fileHandle1:
		lineIN = fileHandle1.readline()
		#while  line1:	
		for i in range(RANGE):
			days = get_days_data(lineIN)
			if  days > test_date_range:
				lineIN = fileHandle1.readline()
				continue
			line2 = [get_user_id(lineIN)]
			line2.extend(0 for i in range(Xrange))
			extra_line1 = np.array(line2)
			matrix1 = np.append(matrix1, [extra_line1], axis=0)
			line2.extend(0 for i in range(Yrange-Xrange))
			extra_line2 = np.array(line2)
			matrix2 = np.append(matrix2, [extra_line2], axis=0)
			lineIN = fileHandle1.readline()
			if i%10000 == 0:
				print('log reading', '\t', i)
	#排序
	matrix1 = matrix1[matrix1[:,0].argsort()]
	#argsort返回的是下标
	matrix1 = np.delete(matrix1,0,0)
	matrix2 = matrix2[matrix2[:,0].argsort()]
	#argsort返回的是下标
	matrix2 = np.delete(matrix2,0,0)  
	#print(matrix[0].argsort())
	#print(matrix)
	return matrix1, matrix2

#生成字典，用于id和下标的对应
def Dict_intial(matrix, id_index_dict):
	for i in range(matrix.shape[0]):
		dict_extra = {matrix[i][0]:i}
		id_index_dict.update(dict_extra)
	return id_index_dict

def Write_result(page, action, matrix_result, i):
	if page == 0:
		matrix_result[i][result_index['con']] += 1
	elif page == 1:
		matrix_result[i][result_index['person']] += 1
	elif page == 2:
		matrix_result[i][result_index['discover']] += 1
	elif page == 3:
		matrix_result[i][result_index['same_city']] += 1
		#print('\t', get_user_id(LineCur))
	elif page == 4:
		matrix_result[i][result_index['other']] += 1

	if action == 0:
		matrix_result[i][result_index['play']] += 1
	elif action == 1:
		matrix_result[i][result_index['good']] += 1
	elif action == 2:
		matrix_result[i][result_index['con_action']] += 1
	elif action == 3:
		matrix_result[i][result_index['retweet']] += 1
		#print('\t', get_user_id(LineCur))
	elif action == 4:
		matrix_result[i][result_index['report']] += 1
	elif action == 5:
		matrix_result[i][result_index['decline']] += 1



	return matrix_result



def Read_activity(matrix_count, matrix_result, matrix_predict_count, matrix_predict, start_date, end_date, test_date_range):
	with open('a3d6_chusai_a_train\\user_activity_log.txt') as fileHandle2:
		LineCur = fileHandle2.readline()
		count = 1
		while LineCur:
			#for i in range(RANGE):
			#print(id_index_dict[1062323])
			try:
				date = get_days_data(LineCur)
				count += 1
				'''if count%1000000 == 0:
					print(count)
					'''
				if date > test_date_range:
					LineCur = fileHandle2.readline()
					continue
				i = id_index_dict[get_user_id(LineCur)]
				page = get_page_data(LineCur)
				action = get_activity_type_data(LineCur)
				#print(action)
				if date >= start_date and date <= end_date:
					#print('be','\t', date)
					matrix_count[i][date - start_date +1] += 1
					matrix_result = Write_result(page, action, matrix_result, i)
				elif date >= start_date+7 and date <= end_date+7:
					#print('af','\t', date)
					matrix_predict_count[i][date - end_date] += 1
					matrix_predict = Write_result(page, action, matrix_predict, i)
				'''else:
					print(date)
				'''
				if count%100000 == 0:
					print(count)
			#print(matrix_count[i][0],'\t',date,'\t',count)
			#print(type(matrix_count[i][0]),'\t',type(matrix_count[i][get_days_data(LineCur)]))
				LineCur = fileHandle2.readline()
			except Exception as e:
				LineCur = fileHandle2.readline()
				print('error!', date, '\t', count)
				pass
			#count += 1
			#print(LineCur,'\t', count)
			#测试用
			
			#if count > 500:
				#break
			

	return matrix_count,matrix_result,matrix_predict, matrix_predict_count




'''
for x in range(RANGE):
	#for i in range(20):
	if matrix_result[x][result_index['play']]:
		print(x, '\t', matrix_result[x][result_index['play']])
'''	


#print(id_index_dict[173080], matrix_result[id_index_dict[173080]][result_index['same_city']])


### 计算统计值区域

#不包括自身
slice_area = 8

'''
def Write_log(slice_area, matrix_result):
	#avg_mean
	matrix_result[]
'''

def max_days(slice_area, matrix):
	max = 0
	for i in range(1, slice_area):
		#范围选择小心id值
		if matrix[i] > 0 and max < i:
			max = i

	return max

def min_days(slice_area, matrix):
	min = 10000
	for i in range(1, slice_area):
		if matrix[i] > 0 and min > i:
			min = i
			#print(i,'\t',matrix[i])
	if min == 10000:
		return 0
	return min

def constant_days(slice_area, matrix):
	constant = 0
	for i in range(1, slice_area-1):
		if matrix[i] > 0 and matrix[i+1] > 0:
			constant += i
	return constant


def ld_sums_days(slice_area, matrix):
	sums = 0
	for i in range(1, slice_area):
		#范围选择小心id值
		if matrix[i] > 0:
			sums += matrix[i]*i
	return sums
#print(np.mean(matrix_count[id_index_dict[173080]][1:slice_area]))
#print(np.var(matrix_count[id_index_dict[173080]][1:slice_area]))
#print(np.mean(matrix_count[id_index_dict[173080]][1:slice_area])*(slice_area-1))
def avg_days(slice_area, matrix):
	return np.mean(matrix[1:slice_area])

def var_days(slice_area, matrix):
	return np.var(matrix[1:slice_area])

def whole_times(slice_area, matrix):
	return np.mean(matrix[1:slice_area])*(slice_area-1)

#写入统计值
def Write_result_count(slice_area,matrix_result,matrix_count):
	for i in range(matrix_result.shape[0]):
		#avg':1,'vari':2, 'ld_times':3, 'max':4, 
		#'min':5, 'constant':6,'ld_sums':7,
		matrix_result[i][result_index['avg']] = avg_days(slice_area, matrix_count[i])
		matrix_result[i][result_index['vari']] = var_days(slice_area, matrix_count[i])
		matrix_result[i][result_index['ld_times']] = whole_times(slice_area, matrix_count[i])
		matrix_result[i][result_index['max']] = max_days(slice_area, matrix_count[i])
		matrix_result[i][result_index['min']] = min_days(slice_area, matrix_count[i])
		matrix_result[i][result_index['constant']] = constant_days(slice_area, matrix_count[i])
		matrix_result[i][result_index['ld_sums']] = ld_sums_days(slice_area, matrix_count[i])
		if i %100 == 0:
			print('processing',i)
	
	return matrix_result




def Save_text(matrix_result, matrix_predict):
	name_start = 'test'+str(start_date)+'_'+str(end_date)+'.txt'
	name_predict = 'test'+str(end_date+1)+'_pre.txt'
	np.savetxt(name_start, matrix_result, fmt=["%f"]*matrix_result.shape[1], delimiter="\t")
	np.savetxt(name_predict, matrix_predict, fmt=["%f"]*matrix_predict.shape[1], delimiter="\t")

###初始化区域

def Initial(Time_range, Start_date, End_date):
	global time_range
	global start_date
	global end_date
	time_range = Time_range
	start_date = Start_date
	end_date = End_date


def main():
	global matrix_result
	global matrix_count
	global id_index_dict 
	global start_date
	global end_date
	global test_date_range
	global RANGE
	#在这个函数里确定时间范围
	Initial(7, 8, 14)
	matrix_count, matrix_result = Matrix_intial(RANGE, matrix_count, matrix_result, 7, 19, test_date_range)
	matrix_predict = matrix_result.copy()
	matrix_predict_count = matrix_count.copy()
	#得到预测集，由于内容都是0，所以可以直接拷贝


	print(matrix_count.shape, '\t', matrix_predict_count.shape)
	#可变对象，相当于传引用调用
	id_index_dict = Dict_intial(matrix_result, id_index_dict)
	#print(id_index_dict)

	#print(id_index_dict)

	#print(matrix_result.shape[0])
	print('Initial complete')
	#动作和页数的值被载入
	matrix_count, matrix_result, matrix_predict, matrix_predict_count =  Read_activity(matrix_count, matrix_result,  matrix_predict_count, matrix_predict, start_date, end_date, test_date_range)
	#print(matrix_count, '\n', matrix_predict_count)


	matrix_result = Write_result_count(slice_area, matrix_result, matrix_count)
	matrix_predict = Write_result_count(slice_area, matrix_predict, matrix_predict_count)
	Save_text(matrix_result, matrix_predict) 


if __name__ == '__main__':
	main()