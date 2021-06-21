# import dis

# this_is_list = []

# def list_sort():
#     a = 5
#     b = 23.78932
#     this_is_list.sort()
#     print("hi")
#     return "ok"

# dis.dis(list_sort)

import threading
import time

run = True

def main(url, num):
    # print('開始執行', url)
    # time.sleep(2)
    # print("hello")
    # print('結束', num)
    while run:
        print(num)

url_list1 = ['www.yahoo.com.tw, www.google.com']
url_list2 = ['www.yahoo.com.tw, www.google.com']    
url_list3 = ['www.yahoo.com.tw, www.google.com']

# 定義線程
t_list = []

t1 = threading.Thread(target=main, args=(url_list1, 1))
t_list.append(t1)
t2 = threading.Thread(target=main, args=(url_list2, 2))
t_list.append(t2)
t3 = threading.Thread(target=main, args=(url_list3, 3))
t_list.append(t3)

# 開始工作
for t in t_list:
    t.start()
    print(t)
    # time.sleep(1)
    # run = False
    # t.join()
    # run = True

time.sleep(1)
run = False

for t in t_list:
    t.join()


# # 調整多程順序
# for t in t_list:
#     t.join()