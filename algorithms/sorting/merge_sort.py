def sort(numbers):
    recursive_sort(numbers, 0, len(numbers))    
    return numbers    
    
def recursive_sort(numbers, start, end):
    length = end - start
    if length == 1:   
        return # nothing to sort
        
    middle = int( (start + end) / 2 )
    recursive_sort(numbers, start, middle)
    recursive_sort(numbers, middle, end)

    merge(numbers, start, middle, end)

def merge(numbers, start, middle, end):   
    temp = numbers[start:middle]    

    index = start
    first_pos = 0 # index into temp
    second_pos = middle
    
    while first_pos < (middle-start) and second_pos < end:
        first = temp[first_pos]        
        second = numbers[second_pos] 
        if first < second:
            numbers[index] = first
            first_pos += 1
        else:
            numbers[index] = second
            second_pos += 1
        index += 1
        
    # if first finishes then second are already in place
    if second_pos == end: # if second finishes, put first into place
        numbers[index:end] = temp[first_pos:middle]     
        
if __name__ == '__main__':
    import performance
    performance.test(sort)
        
        
        
        
    
    

