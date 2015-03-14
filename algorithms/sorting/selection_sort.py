def sort(numbers):
    length = len(numbers)
    for start in range(length-1):        
        min_index = start
        for index in range(start, length):
            if numbers[index] < numbers[min_index]:
                min_index = index
        swap(numbers, start, min_index)
        
def swap(numbers, i1, i2):
    temp = numbers[i1]
    numbers[i1] = numbers[i2]
    numbers[i2] = temp
    
if __name__ == '__main__':
    import performance
    performance.test(sort)
            
            

