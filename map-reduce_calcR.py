#coding=utf-8

import random
import multiprocessing
from multiprocessing import Process

class MapReduce(object):

    def __init__(self, map_func, reduce_func, workers_num=None):

        self.map_func = map_func

        self.reduce_func = reduce_func

        self.workers_num = workers_num

        if not workers_num:

            workers_num = multiprocessing.cpu_count()*2

        self.pool = multiprocessing.Pool(workers_num)

 

    def __call__(self, inputs):

        map_result = self.pool.map(self.map_func, inputs)

        reduce_result = self.reduce_func(map_result)

        return reduce_result

 

def calculator(*args):

    print multiprocessing.current_process().name,' processing'

    points, circle_round = args[0]

    points_in_circle = 0

    for i in range(points):

     # 这里其实只取了1/4圆

        x = random.random()*circle_round

        y = random.random()*circle_round

        if (x**2 + y**2) < circle_round**2:

            points_in_circle += 1

    return points_in_circle

 

def count_circle_points(points_list):

    return sum(points_list)

 

if __name__ == '__main__':

    # 半径

    CIRCLE_ROUND = 10

    # 总点数

    POINTS = 10000000

    # 总进程数

    WORKERS_NUM = 10

 

    map_reduce = MapReduce(calculator, count_circle_points, WORKERS_NUM)

    inputs = [(POINTS/WORKERS_NUM, CIRCLE_ROUND)] * WORKERS_NUM

    all_points_in_circle = map_reduce(inputs)

    ac_as = float(all_points_in_circle)/POINTS

    print 'pi approach to:%7f'%(4*ac_as)
