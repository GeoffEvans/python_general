
class SinglyLinkedList(object):

    def __init__(self):
        self.list = None

    def append(self, value):
        self.list = [value, self.list]

    def get(self, index):
        elem = self.list
        for n in range(index):
            elem = elem[1]
        return elem[0]

class DoublyLinkedList(object):

    def __init__(self):
        self.list = [None, None]

    def append(self, value):
        old_list = self.list
        self.list = [None, value, self.list]
        old_list[0] = self.list

    def get(self, index):
        elem = self.list
        for n in range(index):
            elem = elem[2]
        return elem

    def get_val(self, index):
        return self.get(index)[1]

    def del_val(self, index):
        elem_before = self.get(index-1)
        elem_after = self.get(index+1)
        elem_before[0] = elem_after
        elem_after[2] = elem_before

