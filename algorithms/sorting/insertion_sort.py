def sort(numbers):
    for length in range(2, len(numbers) + 1):
        rev_rng = range(length-1)
        rev_rng.reverse()        
        for index in rev_rng:
            if numbers[index+1] >= numbers[index]:
                break                
            swap(numbers, index+1, index)
                
def swap(numbers, i1, i2):
    temp = numbers[i1]
    numbers[i1] = numbers[i2]
    numbers[i2] = temp
    
if __name__ == '__main__':
    import performance
    performance.test(sort)

