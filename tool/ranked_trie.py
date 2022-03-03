import numpy as np

class RankedTrieNode:
    def __init__(self):
        self.children = np.array([None, None])
        self.char = -1
        self.height = 0
        self.size = 0
        self.contains_0_vector = False
        self.contains_1_vector = False

    def has_sequence(self, x):
        node = self
        for i,c in enumerate(x):
            if node.children[c] is None:
                return False
            node = node.children[c]
        return True

    def insert_sequence(self, x):
        if self.has_sequence(x):
            return

        self.__insert_sequence_internal(x)

    def __insert_sequence_internal(self, x):
        self.size += 1
        if x.size == 0:
            return

        self.height = x.size

        if np.all(x==0):
            self.contains_0_vector = True   
        elif np.all(x==1):
            self.contains_1_vector = True 

        letter = x[0]
        if self.children[letter] is None:
            self.children[letter] = RankedTrieNode()

        self.children[letter].char = letter
        self.children[letter].__insert_sequence_internal(x[1:])

    def print_tree(self):
        self.__print_tree(0)

    def __print_tree(self, depth):
        print(f'({depth}) - char {self.char} has {self.size} sequences.\n\t\
            contains the 0 vector: {self.contains_0_vector}\n\t\
            contains the 1 vector: {self.contains_1_vector}')
        for child in self.children:
            if child is not None:
               child.__print_tree(depth+1)

    def print_all_sequences(self):
        self.__print_all_sequences(np.array([], dtype=np.ubyte))

    
    def __print_all_sequences(self, path):
        if np.all(self.children == None):
            print(path)
        for child in self.children:
            if child is None:
                continue
            child.__print_all_sequences(np.append(path, child.char))

    def decrease_size_by(self, k):
        if k <= 0:
            return self

        node = RankedTrieNode()
        node.size = self.size - k
        node.char = self.char
        node.height = self.height

        if self.children[0] is not None and self.children[0].size <= k:
            node.children[1] = self.children[1].decrease_size_by(k - self.children[0].size)
            node.children[0] = None
        elif self.children[1] is not None and self.children[1].size <= k:
            node.children[0] = self.children[0].decrease_size_by(k - self.children[1].size)
            node.children[1] = None
        elif self.children[0] is not None:
            node.children[0] = self.children[0].decrease_size_by(k)
            node.children[1] = self.children[1]
        else: 
            node.children[0] = self.children[0]
            node.children[1] = self.children[1].decrease_size_by(k)

        if node.children[0] is not None:
            node.contains_0_vector = node.children[0].contains_0_vector
        if node.children[1] is not None:
            node.contains_1_vector = node.children[1].contains_1_vector

        return node
        

    def decrease_size_to(self, N):
        return self.decrease_size_by(self.size - N)

    def get_unique_path(self):
        if self.size > 1:
            raise Exception()

        path = []

        node = self
        while node.height > 0:
            if node.children[0] is not None:
                path.append(0)
                node = node.children[0]
            else:
                path.append(1)
                node = node.children[1]
        
        return np.array(path, dtype=int)
