import threading


class MyThread(threading.Thread):
    def __init__(self, func, args=(), kwargs=None):
        super(MyThread, self).__init__()
        if kwargs is None:
            kwargs = {}
        self.func = func
        self.args = args
        self.kwargs = kwargs # 传参进来的时候 必须和被执行的函数入参名一样才可以

    def run(self):
        self.result = self.func(*self.args,**self.kwargs)

    def get_result(self):
        try:
            return self.result  # 如果子线程不使用join方法，此处可能会报没有self.result的错误
        except Exception:
            return None


