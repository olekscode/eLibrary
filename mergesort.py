#!/usr/bin/python3

import threading
import time

# global variables used as a shared memory in threads
# not sure if it's legal
part_results = []
result = []


class Sorter(threading.Thread):
    # TODO: Find a way to assign the 'end' parameter with default value len(arr)
    def __init__(self, thrd_id, arr, criteria, begin = 0, end = 0):
        self.__id = thrd_id
        self.__arr = arr
        self.__criteria = criteria
        self.__begin = begin
        self.__end = len(arr) if end == 0 else end
        threading.Thread.__init__(self)

    def run(self):
        part_results.append(self.__merge_sort_seq(self.__begin, self.__end))

    def __merge_sort_seq(self, begin, end):
        if end - begin == 1:
            return [self.__arr[begin]]

        mid = (begin + end) // 2
        left = self.__merge_sort_seq(begin, mid)
        right = self.__merge_sort_seq(mid, end)

        merger = Merger(left, right, self.__criteria)

        # TODO: Avoid using 'results' as an intermediary: smells like a dirty code
        result.clear()
        merger.run()

        return result


class Merger(threading.Thread):
    def __init__(self, arr1, arr2, criteria):
        self.__arr1 = arr1
        self.__arr2 = arr2
        self.__criteria = criteria
        threading.Thread.__init__(self)

    def run(self):
        result.extend(self.__merge(self.__arr1, self.__arr2))

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
    threads = []
    part_len = len(arr) // num_of_thrds

    for i in range(num_of_thrds - 1):
        threads.append(Sorter(i, arr, criteria, i * part_len, (i + 1) * part_len))

    threads.append(Sorter(i, arr, criteria, (num_of_thrds - 1) * part_len, len(arr)))

    time_start = time.time()
    for thread in threads:
        thread.start()
        thread.join()
    time_end = time.time()

    print("Time parallel: %s" % (time_end - time_start))
    return part_results
