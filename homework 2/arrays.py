import ctypes


class Array:
    
    def check_index(self, index):
        if not self.size:
            raise IndexError('Array is empty')
        if index >= self.size or index < 0:
            raise IndexError('Invalid index')
    
    def __getitem__(self, index):
        return self.array[index]
    
    def __setitem__(self, index, value):
        self.array[index] = value
    
    def __repr__(self):
        return '[' + ', '.join([str(self[i]) for i in range(self.size)]) + ']'


class SingleArray(Array):
    
    def __init__(self, values):
        self.array = (ctypes.py_object * len(values))(*values)
    
    @property
    def size(self):
        return len(self.array)
    
    def append(self, value):
        new_array = (ctypes.py_object * (self.size + 1))()
        for i in range(self.size):
            new_array[i] = self.array[i]
        self.array = new_array
        self.array[self.size - 1] = value
    
    def insert(self, index, value):
        new_array = (ctypes.py_object * (self.size + 1))()
        for i in range(index):
            new_array[i] = self.array[i]
        for i in range(index, self.size): 
            new_array[i + 1] = self.array[i]
        new_array[index] = value
        self.array = new_array        
    
    def remove(self, index):
        self.check_index(index)
        new_array = (ctypes.py_object * (self.size - 1))()
        for i in range(index):
            new_array[i] = self.array[i]
        for i in range(index + 1, self.size): 
            new_array[i - 1] = self.array[i]
        removed_value = self.array[index] 
        self.array = new_array
        return removed_value


class VectorArray(Array):
    
    def __init__(self, vector):
        self.array = (ctypes.py_object * vector)()
        self.vector = vector
        self.size = 0
    
    def append(self, value):
        if self.size == len(self.array):
            new_array = (ctypes.py_object * (self.size + self.vector))()
            for i in range(self.size):
                new_array[i] = self.array[i]
            self.array = new_array
        self.array[self.size] = value
        self.size += 1
        
    def insert(self, index, value):
        if self.size == len(self.array):
            new_array = (ctypes.py_object * (self.size + self.vector))()
            for i in range(index):
                new_array[i] = self.array[i]
            for i in range(index, self.size): 
                new_array[i + 1] = self.array[i]
            new_array[index] = value
            self.array = new_array
        else:
            for i in range(self.size, index, -1):
                self.array[i] = self.array[i - 1]
            self.array[index] = value
        self.size += 1
        
    def remove(self, index):
        self.check_index(index)
        removed_value = self.array[index]
        for i in range(index, self.size): 
            self.array[i - 1] = self.array[i]
        self.size -= 1
        return removed_value


class FactorArray(Array):
    
    def __init__(self, factor):
        self.array = (ctypes.py_object * 10)()
        self.factor = factor
        self.size = 0
    
    def append(self, value):
        if self.size == len(self.array):
            new_array = (ctypes.py_object * (self.size + self.size * self.factor // 100))()
            for i in range(self.size):
                new_array[i] = self.array[i]
            self.array = new_array
        self.array[self.size] = value
        self.size += 1 
       
    def insert(self, index, value):
        if self.size == len(self.array):
            new_array = (ctypes.py_object * (self.size + self.size * self.factor // 100))()
            for i in range(index):
                new_array[i] = self.array[i]
            for i in range(index, self.size): 
                new_array[i + 1] = self.array[i]
            new_array[index] = value
            self.array = new_array
        else:
            for i in range(self.size, index, -1):
                self.array[i] = self.array[i - 1]
            self.array[index] = value
        self.size += 1
    
    def remove(self, index):    
        self.check_index(index)  
        removed_value = self.array[index]
        for i in range(index, self.size): 
            self.array[i - 1] = self.array[i]
        self.size -= 1
        return removed_value


class MatrixArray:
    
    def __init__(self, vector):
        self.array = SingleArray((VectorArray(vector), ))
        self.vector = vector
        self.size = 0
        
    def append(self, value):
        if self.size == self.array.size * self.vector:
            self.array.append(VectorArray(self.vector))
        self.array[self.size // self.vector].append(value)
        self.size += 1
        
    def __getitem__(self, index):
        return self.array[index // self.vector][index % self.vector]
    
    def __setitem__(self, index, value):
        self.array[index // self.vector][index % self.vector] = value
    
    def insert(self, index, value):
        if self.size == self.array.size * self.vector:
            self.array.append(VectorArray(self.vector))
        for i in range(self.size - 1, index - 1, -1):
            self[i + 1] = self[i]
        self[index] = value
        self.size += 1
        
    def remove(self, index):
        if not self.size:
            raise IndexError('Array is empty')
        if index >= self.size or index < 0:
            raise IndexError('Invalid index')
        removed_value = self[index]
        for i in range(index, self.size): 
            self[i - 1] = self[i]
        self.size -= 1
        return removed_value
            
    def __repr__(self):
        if self.size == 0:
            return '[[], ]'
        result = '['
        for i in range(self.size):
            if (i % self.vector == 0):
                result += '['
            result += str(self[i])
            if (i % self.vector != (self.vector - 1)):
                result += ', '
            if (i % self.vector == (self.vector - 1)):
                result += ']'
            if (i == self.size - 1) and (i % self.vector != (self.vector - 1)):
                result += ']'
            if ((i+1) % self.vector == 0) and (i != self.size - 1):
                result += ', '
        result += ']'
        return result