# 多线程类,使用单例模式进行创建
class MultiThreaded:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.is_multi = True
        return cls._instance

    def get_is_multi(self):
        return self.is_multi

    def set_multi(self, value):
        if not isinstance(value, bool):
            raise TypeError("传递的数值必须是布尔值")
        self.is_multi = value


# 创建一个贡献的全局对象,供所有的工具类引用，这个类没有实现需要的功能

multiThreaded = MultiThreaded()
