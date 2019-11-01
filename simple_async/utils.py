__author__ = 'urlik_vm'

# TODO add classes to __slots__

__all__ = ['Async']


class ASleep:
    def __init__(self, sec):
        self.seconds = int(sec)


class AChangePriority:
    def __init__(self, prior):
        self.priority = int(prior)

class Return:
    def __init__(self, result):
        self.result = result


class Async:

    @staticmethod
    def sleep(sec):
        return ASleep(sec)

    @staticmethod
    def change_priority(prior):
        return AChangePriority(prior)
