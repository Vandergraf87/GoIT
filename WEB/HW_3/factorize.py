#===============================Synchronous version==========================#

# import time

# start = time.perf_counter()

# def factorize(numbers):
#     total_results = list()
#     for n in numbers:
#         result = list()
#         for i in range(1, n+1):
#             if n%i == 0:
#                 result.append(i)
#         total_results.append(result)
#     return print(total_results)


# factorize([128, 255, 99999, 10651060])

# stop = time.perf_counter()

# print(f'Calculating time = {stop-start}')

#=============================================================================#

#===============================Asynchronous version==========================#

import time
from multiprocessing import Pool, cpu_count

start = time.perf_counter()

def  calculating(numbers):
    total_results = list()
    for n in numbers:
        result = list()
        for i in range(1, n+1):
            if n%i == 0:
                result.append(i)
        total_results.append(result)
    return print(total_results)


def factorize(numbers):
    with Pool(cpu_count()) as pool:
        mapped = pool.apply_async(calculating, numbers)
    return mapped

test_numb = [128, 255, 99999, 10651060]
factorize(test_numb)

stop = time.perf_counter()

print(f'Calculating time = {stop-start}')



#=====================================Test values==================================#
# assert a == [1, 2, 4, 8, 16, 32, 64, 128]
# assert b == [1, 3, 5, 15, 17, 51, 85, 255]
# assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
# assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]