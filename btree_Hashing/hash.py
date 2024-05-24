class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [None] * size
        self.step_sizes = {}

    def custom_hash(self, element):
        return int(element) % self.size
    

    def add_element_linear_probe(self, element):
        index = self.custom_hash(element)
        if self.table[index] is None:
            self.table[index] = element
        else:
            # Linear probing to handle collisions
            while self.table[index] is not None:
                index = (index + 1) % self.size
            self.table[index] = element

    def add_element_separate_chaining(self, element):
        index = self.custom_hash(element)
        if self.table[index] is None:
            self.table[index] = [element]
        else:
            # Separate chaining to handle collisions
            if isinstance(self.table[index], list):
                self.table[index].append(element)
            else:
                self.table[index] = [self.table[index], element]

    def add_element_internal_chaining(self, element):
        index = self.custom_hash(element)
        if self.table[index] is None:
            self.table[index] = [element]
        else:
            # Internal chaining to handle collisions
            if isinstance(self.table[index], list):
                self.table[index].append(element)
            else:
                self.table[index] = [self.table[index], element]

    def delete_element(self, element):
        index = self.custom_hash(element)
        if isinstance(self.table[index], list):
            # If the element is in a list at the hashed index (internal or separate chaining)
            if element in self.table[index]:
                self.table[index].remove(element)
        elif self.table[index] == element:
            # If the element is directly stored at the hashed index (linear probing)
            self.table[index] = None
        else:
            initial_index = index
            # Linear probing to handle collisions
            while True:
                index = (index + 1) % self.size
                if self.table[index] == element:
                    self.table[index] = None
                    break
                # If we have searched all slots and returned to the initial index, exit loop
                if index == initial_index:
                    break
    

    def add_element_double_hashing(self, element):
        index = self.custom_hash(element)
        if self.table[index] is None:
            self.table[index] = element
        else:
            # Double hashing to handle collisions
            step = self.custom_hash_2(element)
            while self.table[index] is not None:
                index = (index + step) % self.size
            self.table[index] = element

    def custom_hash_2(self, element):
        prime = 7  # Fixed prime number for simplicity
        step = prime - (int(element) % prime)  # Calculate the hash using the element

        return step