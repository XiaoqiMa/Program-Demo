# import _thread
# import time

# format: _thread.start_new_thread(func, args[, kwargs])
# Old format to write threads; inherited from python2 thread module

# def print_time(threadName, delay):
#     count = 0
#     while count < 5:
#         print('{name} : {t}'.format(name=threadName, t=time.ctime(time.time())))
#         time.sleep(delay)
#         count += 1


# def start_threads():
#     try:
#         _thread.start_new_thread(print_time, ('Thread-1', 1, ))
#         _thread.start_new_thread(print_time, ('Thread-2', 5, ))
#         _thread.start_new_thread(print_time, ('Thread-3', 10, ))
#     except:
#         print('Cannot start threads')


# start_threads()
# while 1:
#     pass


import threading
import time

# threading.activeCount() − Returns the number of thread objects that are active.
# threading.currentThread() − Returns the number of thread objects in the caller's thread control.
# threading.enumerate() − Returns a list of all thread objects that are currently active.
# run() − The run() method is the entry point for a thread.
# start() − The start() method starts a thread by calling the run method.
# join([time]) − The join() waits for threads to terminate.
# isAlive() − The isAlive() method checks whether a thread is still executing.


# Then, override the run(self [,args]) method to implement what the thread should do when started.
#

# Define a new subclass of the Thread class.
class MyThread(threading.Thread):

    # Override the __init__(self [,args]) method to add additional arguments.
    def __init__(self, threadId, name, delay):
        threading.Thread.__init__(self)
        self.threadId = threadId
        self.name = name
        self.delay = delay

    def print_time(self, name, id, delay, counter):
        i = 0
        while i < counter:
            print('{name}-{id}: {t}'.format(name=name, id=id, t=time.ctime(time.time())))
            time.sleep(delay)
            i += 1

    def run(self):
        # Synchronize threads
        threadLock.acquire()
        print('{name}-{id} starts'.format(name=self.name, id=self.threadId))
        # threading functions
        # print('current thread: ', threading.currentThread())
        # print('active count: ', threading.activeCount())
        # print('active list: ', threading.enumerate())
        self.print_time(self.name, self.threadId, self.delay, 5)
        print('{name}-{id} ends'.format(name=self.name, id=self.threadId))
        threadLock.release()


threadLock = threading.Lock()
thread1 = MyThread('1', 'thread', 2)
thread2 = MyThread('2', 'thread', 3)

thread1.start()
thread2.start()
thread1.join()
thread2.join()
print('Main Thead ends')
