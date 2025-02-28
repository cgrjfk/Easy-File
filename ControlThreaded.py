# 控制多线程还是单线程的类，只有这个类可以控制线程的开关--多线程操作类
from MultiThreaded import multiThreaded  # 导入多线程类


class ControlThreaded:
    def __init__(self):
        self.open = True  # 默认开启

    # 设置为一个静态方法
    @staticmethod
    # 关闭多线程类
    def close(self):
        multiThreaded.set_multi(False)
        self.open = False  # 该信号量变成False
