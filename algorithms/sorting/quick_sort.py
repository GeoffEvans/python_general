def sort(numbers):
    recursive_sort(numbers, 0, len(numbers)-1)

def recursive_sort(numbers, start_index, end_index):
    if start_index < end_index:
        middle = partition(numbers, start_index, end_index)
        recursive_sort(numbers, start_index, middle-1)    
        recursive_sort(numbers, middle+1, end_index)

def partition(numbers, start, end):
    pivot = numbers[end]
    after_lower = start
    for index in range(start, end):
        if numbers[index] <= pivot:
            exchange(numbers, index, after_lower)            
            after_lower += 1
    exchange(numbers, after_lower, end)
    return after_lower
            
def exchange(numbers, index1, index2):
    temp = numbers[index1]
    numbers[index1] = numbers[index2]
    numbers[index2] = temp
    
if __name__ == '__main__':
    import performance
    performance.test(sort)
            
    