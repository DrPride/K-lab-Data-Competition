import numpy as np
import pandas as pd

def toDataframe(data):
    data.to_csv("G://data6/c.csv")
    data = pd.read_csv("G://data6/c.csv")
    return data


def f(data):
    num = 0
    days = 0
    data.append(-1)
    for i in range(1,len(data)):
        if data[i] == data[i-1]+1:
            days = days + 1
        elif days != 0:
            days = 0
            num = num+1
        else:
            days = 0
    return num

def l(data):
    num = 0
    days = 0
    sum = 0
    data.append(-1)
    for i in range(1, len(data)):
        if data[i] == data[i - 1] + 1:
            days = days + 1
        elif days != 0:
            sum = sum + days + 1
            days = 0
            num = num + 1
        else:
            days = 0
    return sum

days = 30


#-----------------------------------------------------------------------------------------------------------------------
Data_Fin = pd.DataFrame()
app_launch_log_data = pd.read_table("G://data5/app_launch_log.csv", names=['user_id', 'days'])
app_launch_log_data = app_launch_log_data[app_launch_log_data['days'] < 24]
# print(app_launch_log_data)
data = toDataframe(app_launch_log_data.groupby('user_id').count())
# print(data)
Data_Fin['user_id']= data['user_id']
Data_Fin['count'] = data['days']
# print(Data_Fin)

data = toDataframe(app_launch_log_data.groupby('user_id').sum())
Data_Fin['sum'] = data['days']
# print(Data_Fin)

print(app_launch_log_data)
Data2 = pd.DataFrame(columns=['user_id', 'f', 'l'])
app_launch_log_data = app_launch_log_data.sort_values(by=['user_id', 'days'])
print(app_launch_log_data)
sum = 0
for name in app_launch_log_data.drop_duplicates(['user_id'])['user_id']:
    data = list(app_launch_log_data[app_launch_log_data['user_id']==name]['days'])
    print(name)
    print(data)
    # print(sum)
    Data2.loc[sum] = [name, f(data), l(data)]
    sum = sum +1
Data_Fin['f'] = Data2['f']
Data_Fin['l'] = Data2['l']
# print(Data_Fin)

# data = pd.read_csv("G://data5/1.csv")   # 当计算30天总数居时可以使用
# Data_Fin['f'] = data['f']
# Data_Fin['l'] = data['l']
print(Data_Fin)  # 启动天数， 启动日期之和， 连续几天启动总次数， 连续启动次数
Data_Fin.to_csv("G://data5/Data_Fin.csv")
#-----------------------------------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------------------------------------
Data_Fin2 = pd.DataFrame()
create_video_log_data = pd.read_table("G://data5/video_create_log.csv", names=['user_id', 'days'])
create_video_log_data = create_video_log_data[create_video_log_data['days'] < 24]
create_video_log_data['xxx'] = 1
# print(create_video_log_data)
data = toDataframe(create_video_log_data.groupby('user_id').count())
# print(data)
Data_Fin2['user_id'] = data['user_id']
Data_Fin2['count'] = data['days']
Data_Fin2['avg'] = data['days']/30
# print(Data_Fin2)
data = toDataframe(create_video_log_data.groupby(['user_id', 'days']).count())
# print(data)
data2 = data.loc[:, ['user_id', 'xxx']]
# print(data2)
Data_Fin2['var'] = toDataframe(data2.groupby('user_id').var())['xxx']
# print(Data_Fin2)
Data_Fin2['days_count'] = toDataframe(data2.groupby('user_id').count())['xxx']
Data_Fin2['max'] = toDataframe(data2.groupby('user_id').max())['xxx']
Data_Fin2['min'] = toDataframe(data2.groupby('user_id').min())['xxx']
# print(Data_Fin2)
data = data.loc[:, ['user_id', 'days']]
# print(data)



sum = 0
for name in data.drop_duplicates(['user_id'])['user_id']:
    datas = list(data[data['user_id']==name]['days'])
    # print(datas)
    print(sum)
    Data_Fin2.loc[sum, 'l'] = l(datas)
    sum = sum +1
# print(Data_Fin2)


data = toDataframe(create_video_log_data.groupby('user_id').sum())
Data_Fin2['days_sum'] = data['days']
# print(Data_Fin2)

Data_Fin2.to_csv("G://data5/Data_Fin2.csv")
# ------------------------------------------------------------------------------------------------------------------------



user_register_log_data = pd.read_table("G://data5/user_register_log.csv", names=['user_id', 'register_day', 'register_type', 'device_type'])
# print(user_register_log_data)
Data_Fin3 = user_register_log_data.loc[:, ['user_id', 'register_day']]
Data_Fin1 = pd.read_csv("G://data5/Data_Fin.csv")
Data_Fin2 = pd.read_csv("G://data5/Data_Fin2.csv")
# print(Data_Fin1)
# print(Data_Fin2)

Data_Fin = pd.merge(Data_Fin1, Data_Fin2, how='outer', on='user_id')
Data_Fin = pd.merge(Data_Fin, Data_Fin3, on='user_id')
Data_Fin = Data_Fin.fillna(0)
Data_Fin.to_csv("G://最终计算所需数据/24天所有人（1）.csv", index= False)
Data_Fin = pd.read_csv("G://最终计算所需数据/24天所有人（1）.csv", index_col= 0)
# user_register_log_data.to_csv("G://data5/7.csv")
# print(Data_Fin)

# Data_Fin = Data_Fin.astype('float32')
# # print(Data_Fin)
# Data_Fin_Martix = Data_Fin.values.astype('float32')
# # print(Data_Fin_Martix)

result = pd.read_table("G://data5/app_launch_log.csv", names=['user_id', 'days'])
result = result[result['days']>=24]
result['days'] = 1
result = result.drop_duplicates(['user_id']).sort_values(by='user_id')
# print(result)
# Data_Fin = pd.read_csv("G://最终计算所需数据/24天所有人（1）.csv", index_col= 0)
Data_Fin = pd.merge(Data_Fin, result, on='user_id', how='left').fillna(0)
Data_Fin.to_csv("G://最终计算所需数据/24天所有人（1）.csv", index= False)
print(Data_Fin)

Data_Fin = Data_Fin.astype('float32')
# # print(Data_Fin)
# Data_Fin_Martix = Data_Fin.values.astype('float32')
# # print(Data_Fin_Martix)