#!/usr/bin/python3

import threading
import time

# global variables used as a shared memory in threads
# not sure if it's legal
part_results = []
result = []


class Sorter(threading.Thread):
    # TODO: Find a way to assign the 'end' parameter with default value len(arr)
    def __init__(self, thread_id, arr, criteria, mutex, begin, end):
        self.__id = thread_id
        self.__arr = arr
        self.__criteria = criteria
        self.__mutex = mutex
        self.__begin = begin
        self.__end = end
        threading.Thread.__init__(self)

    def run(self):
        part_res = self.__merge_sort_seq(self.__begin, self.__end)
        global part_results

        with self.__mutex:
            part_results.append(part_res)

    def __merge_sort_seq(self, begin, end):
        if end - begin == 1:
            return [self.__arr[begin]]

        mid = (begin + end) // 2
        left = self.__merge_sort_seq(begin, mid)
        right = self.__merge_sort_seq(mid, end)

        # TODO: Avoid using this mutex. It's just a stopgap
        stopgap_mutex = threading.Lock()
        merger = Merger(left, right, self.__criteria, stopgap_mutex)

        # TODO: Avoid using 'results' as an intermediary: smells like a dirty code
        with self.__mutex:
            result.clear()
            merger.run()

        return result


class Merger(threading.Thread):
    def __init__(self, arr1, arr2, criteria, mutex):
        self.__arr1 = arr1
        self.__arr2 = arr2
        self.__criteria = criteria
        self.__mutex = mutex
        threading.Thread.__init__(self)

    def run(self):
        with self.__mutex:
            result.append(self.__merge(self.__arr1, self.__arr2))

    def __merge(self, left, right):
        res = []
        li = 0
        ri = 0

        crit = self.__criteria

        while li != len(left) and ri != len(right):
            if left[li][crit] > right[ri][crit]:
                res.append(right[ri])
                ri += 1

            elif left[li][crit] < right[ri][crit]:
                res.append(left[li])
                li += 1

            else:
                res.append(right[ri])
                ri += 1

                res.append(left[li])
                li += 1

        while li != len(left):
            res.append(left[li])
            li += 1

        while ri != len(right):
            res.append(right[ri])
            ri += 1

        return res


def sort_parallel(arr, criteria, num_of_thrds):
    time_start = time.time()

    threads = []
    mutex = threading.Lock()
    part_len = len(arr) // num_of_thrds

    for i in range(num_of_thrds - 1):
        threads.append(Sorter(i, arr, criteria, mutex,
                              i * part_len,
                              (i + 1) * part_len))

    threads.append(Sorter(i, arr, criteria, mutex,
                          (num_of_thrds - 1) * part_len,
                          len(arr)))

    for thread in threads:
        thread.start()
        thread.join()

    threads.clear()

    num_of_res = num_of_thrds
    global part_results

    while num_of_res != 1:
        num_of_res //= 2
        for i in range(num_of_res):
            threads.append(Merger(part_results[2 * i],
                                  part_results[2 * i + 1],
                                  criteria, mutex))

        if num_of_thrds % 2 == 1:
            threads.append(Merger(result,
                                  part_results[num_of_thrds - 1],
                                  criteria, mutex))

        for thread in threads:
            thread.start()
            thread.join()

        part_results = result

    time_end = time.time()

    print("Time parallel: %s" % (time_end - time_start))
    return result
