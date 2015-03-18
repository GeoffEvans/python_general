import numpy.random as rnd
import timeit
import copy

def test(sorting_func):
    for n in range(1000):
        numbers = rnd.randint(0, high=100, size=100).tolist()
        numbers_copy = copy.copy(numbers)
        numbers_copy.sort()
        sorting_func(numbers)
        assert numbers == numbers_copy
        
def time_range(sorting_func, string):
    times = []    
    for length in [10*m for m in range(1,21)]:
        def time_func():
            numbers = rnd.randint(0, high=100, size=length)        
            sorting_func(numbers)
        new_time = timeit.timeit(time_func, number=100)
        times.append(new_time)
    plt.plot(times, string)

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    
    import bubble_sort
    time_range(bubble_sort.sort, 'r')
    import insertion_sort
    time_range(insertion_sort.sort, 'b')
    import selection_sort
    time_range(selection_sort.sort, 'g')
    import heap_sort
    time_range(heap_sort.sort, 'k')
    import merge_sort
    time_range(merge_sort.sort, 'c')    
    import quick_sort
    time_range(quick_sort.sort, 'y')
