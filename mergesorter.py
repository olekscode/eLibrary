import _thread as thread
import time


class MergeSorter:
    def __init__(self, num_of_thrds):
        self.__num_of_thrds = num_of_thrds
        self.__arr = []
        self.__criteria = ''
        self.__part_res = []
        self.__res = []

    def sort(self, arr, criteria):
        self.__arr = arr
        self.__criteria = criteria

        if self.__num_of_thrds == 1:
            return self.__merge_sort_seq(0, len(arr))

        elif self.__num_of_thrds > 1:
            return self.__merge_sort_parallel()

        else:
            raise Exception('Number of threads should be positive')

    def __merge_sort_seq(self, begin, end):
        if end - begin == 1:
            return [self.__arr[begin]]

        mid = (begin + end) // 2
        left = self.__merge_sort_seq(begin, mid)
        right = self.__merge_sort_seq(mid, end)
        return self.__merge(left, right)

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

    def __merge_parts(self, left, right):
        self.__res.extend(self.__merge(left, right))

    def __merge_parts_parallel(self):
        self.__res = []
        num = len(self.__part_res)
        half_num = num // 2
        # remainder = num % 2

        for i in range(0, half_num):
            thread.start_new_thread(
                self.__merge_parts, 
                (self.__part_res[2 * i], self.__part_res[2 * i + 1],))

    # TODO: Replace with lambda
    def __merge_sort_partial(self, begin, end):
        self.__part_res.append(self.__merge_sort_seq(begin, end))

    # TODO: Replace _thread module with threading. Otherwise the
    # time evaluation may go wrong as there's no join() in _thread
    def __merge_sort_parallel(self):
        self.__part_res = []
        part_len = len(self.__arr) // self.__num_of_thrds

        start = time.time()
        for i in range(0, self.__num_of_thrds - 1):
            thread.start_new_thread(
                self.__merge_sort_partial,
                (i * part_len, (i + 1) * part_len,))

        thread.start_new_thread(
            self.__merge_sort_partial,
            ((self.__num_of_thrds - 1) * part_len, len(self.__arr),))
        
        end = time.time()

        self.__merge_parts_parallel()
        return self.__res
