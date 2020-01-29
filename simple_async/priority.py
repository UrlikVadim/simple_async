# coding: utf-8
__author__ = 'urlik_vm'


class PriorityCounter(object):
    def __init__(self):
        self.__value = 0

    def increment(self):
        self.__value += 1

    def decrement(self):
        if self.__value > 0:
            self.__value -= 1
        else:
            raise ValueError('Counter is unsigned')

    @property
    def value(self):
        return self.__value

    def __int__(self):
        return self.__value

    def __repr__(self):
        return '<PriorityCounter: {0}>'.format(self.__value)


class PriorityDict(object):

    def __init__(self, priority_set=None):
        self.priority_set = set(priority_set) if priority_set else {1, 2, 3, 4, 5}
        self.min_priority = min(self.priority_set)
        self.max_priority = max(self.priority_set)
        self._priority_iter = self.__infinityiter()
        for pr in self.priority_set:
            self[pr] = PriorityCounter()

    def __getitem__(self, key):
        if key not in self.priority_set:
            raise IndexError('Priority number must be {0}'.format(self.priority_set))
        return self.__dict__.get(key)

    def __setitem__(self, key, value):
        if not self.__dict__.get(key) and key in self.priority_set:
            self.__dict__[key] = value
        else:
            raise IndexError('Priority number must be {0}'.format(self.priority_set))

    def __repr__(self):
        return str(self.__dict__)

    def __infinityiter(self):
        while True:
            for pr in self.priority_set:
                for _ in range(max(self.priority_set) - pr + 1):
                    if self[pr].value > 0:
                        yield pr
                    else:
                        break
    
    def next_priority(self):
        return next(self._priority_iter) 

