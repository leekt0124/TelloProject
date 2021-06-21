import threading
import time

# 子執行緒類別
class MyThread(threading.Thread):
  def __init__(self, num):
    threading.Thread.__init__(self)
    self.num = num

  def run(self):
    print("Thread", self.num)
    time.sleep(2)

# 建立 5 個子執行緒
threads = []
for i in range(5):
  threads.append(MyThread(i))
  threads[i].start()

# 主執行緒繼續執行自己的工作
# ...

# 等待所有子執行緒結束
for i in range(5):
  threads[i].join()

print("Done.")