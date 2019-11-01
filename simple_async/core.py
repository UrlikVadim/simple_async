# coding: utf-8
__author__ = 'urlik_vm'

import random
from collections import deque
from datetime import datetime, timedelta

from .priority import PriorityDict
from .utils import ASleep, AChangePriority, Return


class TaskInstance:

    def __init__(self, generator, func_name):
        self.generator = generator
        self.gen_inited = False  # нужен для реализации асинхроных ответов
        self.__priority = None

        self.sleep = False
        self.last_time = datetime.now()
        
        self.finish = False
        self.childTask = None
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
        res = None
        try:
            if self.childTask is not None and not self.childTask.finish:

                res = self.childTask()

                if self.childTask.finish:
                    child_res = self.childTask.result
                    self.childTask = None
                    res = self.generator.send(child_res)
                    if type(res) == Return:
                        self.result = res.result
                        res = self.result
                        raise StopIteration
            else:

                res = next(self.generator)
                if type(res) == Return:
                    self.result = res.result
                    res = self.result
                    raise StopIteration
                elif type(res) == TaskInstance:
                    self.childTask = res

        except StopIteration:
            self.finish = True

        return res


class Task:

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        generator = self.func(*args, **kwargs)
        return TaskInstance(generator, self.func.__name__)


class Dispetcher:

    def __init__(self, tasks, priority_set=None):
        self.tasks = tasks
        self.task_queue = deque()
        self.task_queue.extend(self.tasks)
        self.priority_dict = PriorityDict(priority_set)
        for t in tasks:
            t.priority = t.priority if t.priority is not None else self.priority_dict.min_priority
            self.priority_dict[t.priority].increment()



    def run(self):
        get_priority = iter(self.priority_dict)

        while len(self.task_queue):

            task = self.task_queue.popleft()
            cycle_time = datetime.now()

            if task.last_time <= cycle_time:
                if task.sleep:
                    task.sleep = False
                    self.priority_dict[task.priority].increment()

                if task.priority != next(get_priority):
                    self.task_queue.append(task)
                    continue

                res = task()

                if type(res) == ASleep:
                    task.last_time = cycle_time + timedelta(seconds=res.seconds)
                    task.sleep = True
                    self.priority_dict[task.priority].decrement()
                elif type(res) == AChangePriority:
                    self.priority_dict[task.priority].decrement()
                    self.priority_dict[res.priority].increment()
                    task.priority = res.priority
                else:
                    pass
            
            if task.finish:
                self.priority_dict[task.priority].decrement()
            else:
                self.task_queue.append(task)
