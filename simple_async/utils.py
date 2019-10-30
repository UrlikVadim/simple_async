# coding: utf-8
__author__ = 'urlik_vm'

# TODO add classes to __slots__

__all__ = ['Async']


class ASleep(object):
    def __init__(self, sec):
        self.seconds = int(sec)


class AChangePriority(object):
    def __init__(self, prior):
        self.priority = int(prior)


class Async(object):

    @staticmethod
    def sleep(sec):
        return ASleep(sec)

    @staticmethod
    def change_priority(prior):
        return AChangePriority(prior)
