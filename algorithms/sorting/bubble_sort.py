def sort(numbers):
    length = len(numbers)
    for m in range(length-1):
        move_mth_largest_to_mth_from_end(m, numbers, length)
        
def move_mth_largest_to_mth_from_end(m, numbers, length):
    for n in range(length-1-m):
        swap_if_necessary(n, numbers)
        
def swap_if_necessary(n, numbers):
    temp = 0        
    if numbers[n] > numbers[n+1]:
        temp = numbers[n]
        numbers[n] = numbers[n+1]
        numbers[n+1] = temp
        
if __name__ == '__main__':
    import performance
    performance.test(sort)
        
