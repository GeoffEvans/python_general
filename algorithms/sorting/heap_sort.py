from math import ceil

def sort(numbers):
    heap = make_heap(numbers)
    while heap[1] > 0:
        remove_node(heap, 0)
    return heap[0]

def left(index):
    return 2 * index + 1
    
def right(index):
    return 2 * index + 2
    
def parent(index):
    return ceil(index/2 - 1)
    
def make_heap(numbers):
    length = len(numbers)    
    heap = [numbers, length]
    for index in range(length-1, -1, -1):
        sift_down(heap, index)
    return heap
    
def get_node(heap, index):
    if index >= heap[1] or index < 0:
        return None
    return heap[0][index]
    
def swap_nodes(heap, i1, i2):
    temp = heap[0][i1]
    heap[0][i1] = heap[0][i2]
    heap[0][i2] = temp
    
def sift_down(heap, index):
    left_val = get_node(heap, left(index))
    right_val = get_node(heap, right(index))
    
    new_index = index    
    if not left_val == None and left_val > get_node(heap, new_index):
        new_index = left(index)
    if not right_val == None and right_val > get_node(heap, new_index):
        new_index = right(index)
    
    if not new_index == index:
        swap_nodes(heap, index, new_index)
        sift_down(heap, new_index)
 
def sift_up(heap, index):
    val = get_node(heap, index)
    parent_val = get_node(heap, parent(index))
    if not parent_val == None and val > parent_val:
        swap_nodes(heap, parent(index), index)
        index = parent(index)
        sift_up(heap, index)

def add_node(heap, val):
    heap[0].append(val)
    index = heap[1]    
    heap[1] += 1
    sift_up(heap, index)    

def remove_node(heap, index):
    heap[1] -= 1
    swap_nodes(heap, heap[1], index)    
    sift_down(heap, index)

if __name__ == '__main__':
    import performance
    performance.test(sort)