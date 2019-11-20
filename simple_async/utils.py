__author__ = 'urlik_vm'

__all__ = ['Async']


class ASleep:
    __slots__ = ('seconds',)
    def __init__(self, sec):
        self.seconds = int(sec)


class AChangePriority:
    __slots__ = ('priority',)
    def __init__(self, prior):
        self.priority = int(prior)


class AAppendTask:
    __slots__ = ('task',)
    def __init__(self, task):
        self.task = task


class Async:

    @staticmethod
    def sleep(sec):
        return ASleep(sec)

    @staticmethod
    def change_priority(prior):
        return AChangePriority(prior)
    
    @staticmethod
    def append_task(task):
        return AAppendTask(task)


class Return:
    __slots__ = ('result',)
    def __init__(self, result):
        self.result = result
