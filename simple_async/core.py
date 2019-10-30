# coding: utf-8
__author__ = 'urlik_vm'

import random
from collections import deque
from datetime import datetime, timedelta

from .priority import PriorityDict
from .utils import ASleep, AChangePriority


class TaskInstance(object):

    def __init__(self, generator, func_name):
        self.generator = generator
        self.gen_inited = False  # нужен для реализации асинхроных ответов
        self.__priority = 1
        self.last_time = datetime.now()
        self.finish = False
        self.__name__ = func_name

    @property
    def priority(self):
        return self.__priority

    @priority.setter
    def priority(self, value):
        value = int(value)
        if 1 <= value <= 5:
            self.__priority = value
        else:
            raise ValueError('Priority is unsigned (Priority number must be 1-5)')

    def __call__(self):
        if not self.gen_inited:
            self.gen_inited = True
            return next(self.generator)
        try:
            res = self.generator.send(None)  # TODO реализация асинхроных ответов
            return res
        except StopIteration:
            self.finish = True


class Task(object):

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        generator = self.func(*args, **kwargs)
        return TaskInstance(generator, self.func.__name__)


class Dispetcher(object):

    def __init__(self, tasks, priority_set=None):
        self.tasks = tasks
        self.task_queue = deque()
        self.task_queue.extend(self.tasks)
        self.priority_dict = PriorityDict(priority_set)
        for t in tasks:
            self.priority_dict[t.priority].increment()
        from pprint import pprint
        print('priority dict')
        pprint(self.priority_dict)


    def run(self):
        while True:
            if len(self.task_queue) == 0:
                break
            for pr in self.priority_dict:
                task = self.task_queue.popleft()
                if task.priority != pr:
                    self.task_queue.append(task)
                    continue

                cycle_time = datetime.now()

                if task.last_time <= cycle_time:
                    res = task()

                    if task.finish:
                        self.priority_dict[task.priority].decrement()

                    if type(res) == ASleep:
                        task.last_time = cycle_time + timedelta(seconds=res.seconds)
                    elif type(res) == AChangePriority:
                        self.priority_dict[task.priority].decrement()
                        self.priority_dict[res.priority].increment()
                        task.priority = res.priority
                    else:
                        pass
                if not task.finish:
                    self.task_queue.append(task)
