# import threading
# import time
# #
# # def tstart(arg):
# #     time.sleep(0.5)
# #     print("%s running...." % arg)
# #
# # if __name__ == '__main__':
# #     t1 = threading.Thread(target=tstart, args=('This is thread 1',))
# #     t2 = threading.Thread(target=tstart, args=('This is thread 2',))
# #     t1.start()
# #     t2.start()
# #     print("This is main function")
#
# def tstart(arg):
#     var = 0
#     for i in range(100000000):
#         var += 1
#
# if __name__ == '__main__':
#     t1 = threading.Thread(target=tstart, args=('This is thread 1',))
#     t2 = threading.Thread(target=tstart, args=('This is thread 2',))
#     start_time = time.time()
#     t1.start()
#     t2.start()
#     t1.join()
#     t2.join()
#     print("Two thread cost time: %s" % (time.time() - start_time))
#     start_time = time.time()
#     tstart("This is thread 0")
#     print("Main thread cost time: %s" % (time.time() - start_time))