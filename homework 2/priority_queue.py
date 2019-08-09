class PriorityQueue:
    
    def __init__(self):
        self.queue = []
    
    def enqueue(self, priority, value):
        if priority < 0:
            raise ValueError('Priority must be greater than 0')
        self.queue.append((priority, value))
        self.queue.sort(key=lambda x: x[0])
        
    def dequeue(self):
        if self.is_empty():
            raise IndexError('Queue is empty')
        return self.queue.pop(0)[1]
    
    def is_empty(self):
        return not self.queue