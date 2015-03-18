from numpy.random import randint

class TreeNode(object):
    
    def __init__(self, value, parent=None):
        self.value = value
        self.parent = parent
        if parent is not None:
            parent.children.append(self)
        self.been_visited = False
        self.children = []
        self.distance = float("inf")
        
def make_tree():
    depth = 4
    first_node = TreeNode(randint(0, 10))
    add_children(first_node, depth-1)
    return first_node

def add_children(parent, depth):
    if depth == 0:
        return
    number_of_children = randint(2, 4)
    for n in randint(2, high=5, size=number_of_children).tolist():
        new_node = TreeNode(randint(0, 10), parent)
        add_children(new_node, depth-1)
        
def dfs_tree(top, cond):
    top.distance = 0
    return visit_children(top, cond)

def visit_children(node, cond):
    if cond(node):
        return node
    for child in node.children:
        child.distance = node.distance + 1
        match = visit_children(child, cond)
        if match is not None:
            return match

def bfs_tree(top, cond):
    top.distance = 0
    
    import Queue     
    q = Queue.Queue()    
    q.put(top)    
    
    while not q.empty():
        node = q.get()    
        if cond(node):
            return node
        for child in node.children:
            child.distance = node.distance + 1
            q.put(child)

if __name__ == '__main__':
    t = make_tree()
    cond = lambda x: x.value == 3
    node = bfs_tree(t, cond)
    print node.distance
    print node.value
