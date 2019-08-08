import time, threading

def long_time_task(i):
    print('当前子线程：{} - 任务{}'.format(threading.current_thread().name, i))
    time.sleep(2)
    print('结果：{}'.format(8**20))

'''
独立的运行
因为没有用join()方法，主线程和子线程其实是独立运行的，主线程没有等子线程完成
结束后就打印了消耗时间，主线程结束后，子线程仍在独立运行
'''
if __name__ == '__main__':
    start=time.clock()
    print('这是主线程：{}'.format(threading.current_thread().name))
    t1=threading.Thread(target=long_time_task, args=(1,))
    t2=threading.Thread(target=long_time_task, args=(2,))
    t1.start()
    t2.start()
    end=time.clock()
    print('总共用时{}秒'.format((end-start)))
    print('-' * 60)


'''
使用join()方法来实现：主线程等待子线程实现线程的同步
'''
if __name__ == '__main__':
    start=time.clock()
    print('这是主线程：{}'.format(threading.current_thread().name))
    thread_list=[]
    for i in range(1,3):
        t=threading.Thread(target=long_time_task, args=(i, ))
        thread_list.append(t)

    for t in thread_list:
        t.start()

    for t in thread_list:
        t.join()

    end=time.clock()
    print('总共用时{}秒'.format((end - start)))
    print('-' * 60)


'''
使用t.setDaemon(True)来实现：主线程结束时不再执行子线程
'''
if __name__ == '__main__':
    start=time.clock()
    print('这是主线程：{}'.format(threading.current_thread().name))
    thread_list=[]
    for i in range(5):
        t=threading.Thread(target=long_time_task, args=(i, ))
        t.setDaemon(True)
        t.start()

    end=time.clock()
    print('总共用时{}秒'.format((end - start)))
    print('-' * 60)

'''
数据共享与通信
多进程和多线程最大的不同在于：多进程中，同一个变量，各有一份拷贝在每个进程中，互不影响；而多线程中，所有变量都由所有线程共享，
容易把内容改乱
'''
'''
具体balance为何不为零的原因查看廖晓峰的Python教程部分
'''
balance=0

def change_it(n):
    global balance
    balance=balance+n
    balance=balance-n

def run_thread(n):
    for i in range(1000000):
        change_it(n)

start=time.clock()
t1=threading.Thread(target=run_thread, args=(5, ))
t2=threading.Thread(target=run_thread, args=(9, ))
t1.start()
t2.start()
t1.join()
t2.join()
end=time.clock()
print(balance)
print((end-start))


'''
解决方法就是给change_it2加锁，当某个线程执行change_it2()时，其他线程不能同时执行，不过这样速度也就慢下来了。
'''
'''
锁的好处就是确保了某段关键代码只能由一个线程从头到尾完整执行，坏处是阻止了多线程并发执行，包含
锁的某段代码实际上只能以单线程模式执行，效率下降

延伸到GIL问题上，GIL就是全局锁，最初是为了数据安全所做的决定，保证CPU在同一时间只能执行一个线程，
在单核时代，Python的多线程与其它语言的多线程本质没什么区别，因为都是并发，不是并行，实际上瞬间都只有一条线程在运行，某个线程
运行的时候都可以拿到GIL（类似于通行证）。但是多核时并行就不可以了，GIL只能分配给一个线程。
综合来讲：单核时代，多进程、多线程用什么语言都没差别，因为都是并发运行。多核时代，Python的多进程没问题，因为每一个进程都有一个GIL，可以
在多核上并行运行，但是多线程出现问题，因为只有一把GIL，同时只能有一个线程在一个核上运行，其他的核和线程都在围观，还得等这个线程结束时进行
抢夺GIL
'''
balance_2=0
lock=threading.Lock()

def change_it2(n):
    global balance_2
    balance_2=balance_2+n
    balance_2=balance_2-n

def run_thread2(n):
    for i in range(1000000):
        lock.acquire()
        try:
            change_it(n)
        finally:
            lock.release()
start=time.clock()
t1=threading.Thread(target=run_thread2, args=(5, ))
t2=threading.Thread(target=run_thread2, args=(9, ))
t1.start()
t2.start()
t1.join()
t2.join()
end=time.clock()
print(balance_2)
print((end-start))