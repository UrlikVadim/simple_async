# simple_async
simple async python library

```python

from simple_async.core import Task, Dispetcher
from simple_async.utils import Async


@Task
def any_async_function(num):
    print('{1}Task {0} start'.format(num, ' ' * num * 2))
    yield
    for i in range(2):
        print('{2}Task {0}: --------- 1 cycle {1}'.format(num, i, ' ' * num * 2))
        yield

    if num in (1, 2):
        yield Async.change_priority(4)

    if num in (2, 3):
        yield Async.sleep(5)

    for i in range(2):
        print('{2}Task {0}: +++++++++ 2 cycle {1}'.format(num, i, ' ' * num * 2))
        yield
    print('{1}Task {0} end'.format(num, ' ' * num * 2))


if __name__ == '__main__':
    print('=START=')
    tasks = [any_async_function(i+1) for i in range(5)]
    disp = Dispetcher(tasks)
    disp.run()
    print('=END=')

```