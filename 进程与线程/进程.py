import time, os, random
from multiprocessing import Process, Pool, cpu_count, Queue

'''
做个简单的比喻：进程=火车，线程=车厢
线程在进程下行进（单纯的车厢无法运行）
一个进程可以包含多个线程（一辆火车可以有多个车厢）
不同进程间数据很难共享（一辆火车上的乘客很难换到另外一辆火车，比如站点换乘）
同一进程下不同线程间数据很易共享（A车厢换到B车厢很容易）
进程要比线程消耗更多的计算机资源（采用多列火车相比多个车厢更耗资源）
进程间不会相互影响，一个线程挂掉将导致整个进程挂掉（一列火车不会影响到另外一列火车，但是如果一列火车上中间的一节车厢与前一节产生断裂，将影响后面的所有车厢）
进程可以拓展到多机，进程最多适合多核（不同火车可以开在多个轨道上，同一火车的车厢不能在行进的不同的轨道上）
进程使用的内存地址可以上锁，即一个线程使用某些共享内存时，其他线程必须等它结束，才能使用这一块内存。（比如火车上的洗手间）－"互斥锁"
进程使用的内存地址可以限定使用量（比如火车上的餐厅，最多只允许多少人进入，如果满了需要在门口等，等有人出来了才能进去）－“信号量”
'''
def long_time_task(i):
    print('当前进程: {} - 任务{}'.format(os.getpid(),i ))
    time.sleep(2)
    print('结果：{}'.format(8 ** 70))


'''
正常简单的循环计算
'''
if __name__ == '__main__':
    print('当前线程：{}'.format(os.getpid()))
    start=time.clock()
    for i in range(2):
        long_time_task(i)
    end=time.clock()
    print("用时{0:.20f}秒".format((end-start)))
    print('-'*60)


'''
multiprocessing模块
'''
if __name__ == '__main__':
    print('当前母进程：{}'.format(os.getpid()))
    start=time.time()
    p1=Process(target=long_time_task, args=(0,))
    p2=Process(target=long_time_task, args=(1,))
    print('等待所有子进程完成')
    p1.start()
    p2.start()
    p1.join()               #使用join()是为了让母进程阻塞，等待子进程都完成后才打印，否则输出时间只是母进程执行的时间
    p2.join()
    end=time.time()
    print("总共用时{}秒".format((end-start)))
    print('-' * 60)


'''
Pool模块
手动设置一个个Process实例比较麻烦，可以直接用进程池Pool，Pool类当有新的请求提交时，若进程池还没满，
就会创建一个新的进程来运算（超过CPU的话就是并发运算，没超过就是并行同时运算），若进程池已满，就会告知先等待，
直到池中有进程结束，再执行请求。
'''
'''
这里的情况是：如果Pool设置为8，8个任务并发运行，因为有sleep2秒的代码存在，差不多2秒多就结束运行了
而如果Pool设置为4，,4个任务并行运行，然后等待了2秒，任务0结束后输出结果，再插入任务4，再任务1结束后输出结果，再插入任务5，新插入
的任务又得sleep2秒，所以反而运行慢。如果没有sleep2秒的代码存在，设置为4会更快
'''
if __name__ == '__main__':
    print("CPU内核数：{}".format(cpu_count()))
    print("当前母进程：{}".format(os.getpid()))
    start=time.clock()
    p=Pool(4)
    for i in range(8):
        p.apply_async(long_time_task, args=(i,))
    print('等待所有子进程完成。')
    p.close()
    p.join()
    end=time.clock()
    print("总共用时{}秒".format((end-start)))
    print('-' * 60)


'''
数据共享与通信
通常，进程之间是相互独立的，每个进程都有独立的内存。但可以使用队列queue来实现不同进程间的数据共享，或者通过共享内存，这里
讲解队列queue
'''
def write(q):
    print('Process to write: {}'.format(os.getpid()))
    for value in ['A', 'B', 'C']:
        print('Put %s to queue...' % value)
        q.put(value)
        time.sleep(random.random())

def read(q):
    print('Process to read:{}'.format(os.getpid()))
    while True:
        value=q.get(True)                                   #blocking=True的话就是阻塞模式，即如果取数据的时候为空，就等一会
        print('Get %s from queue.' % value)

if __name__ == '__main__':
    q=Queue()
    pw=Process(target=write, args=(q, ))
    pr=Process(target=read, args=(q,))
    pw.start()
    pr.start()
    pw.join()
    pr.terminate()                  #因为pr里是死循环，强行终止掉
    print('-' * 60)

