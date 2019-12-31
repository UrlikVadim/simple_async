# coding: utf-8
__author__ = 'urlik_vm'

from simple_async.core import coroutine, Dispetcher
from simple_async.utils import Async, Return


@coroutine()
def any_async_function(num):
    print('{1}Task {0} start'.format(num, ' ' * num * 2))
    res = yield any_async_function2(num)
    print('{1}Task {0} end: {2}'.format(num, ' ' * num * 2, res))
    

@coroutine()
def any_async_function2(num):
    print('{1}CTask {0} start'.format(num, ' ' * num * 2))
    try:
        yield
        for i in range(2):
            print('{2}CTask {0}: --------- 1 cycle {1}'.format(num, i, ' ' * num * 2))
            yield

        if num in (1, 2):
            yield Async.change_priority(4)

        if num in (2, 3):
            yield Async.sleep(10)

        for i in range(2):
            print('{2}CTask {0}: +++++++++ 2 cycle {1}'.format(num, i, ' ' * num * 2))
            yield
        print('{1}CTask {0} end'.format(num, ' ' * num * 2))
        yield Return(num*10)
    except ValueError:
        pass
    finally:
        print('{1}CTask {0} finally'.format(num, ' ' * num * 2))


if __name__ == '__main__':
    print('=START=')
    tasks = [any_async_function(i+1) for i in range(5)]
    disp = Dispetcher(tasks)
    disp.run()
    print('=END=')
