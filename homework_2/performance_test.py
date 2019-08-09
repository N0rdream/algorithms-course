import time
from arrays import SingleArray, VectorArray, FactorArray, MatrixArray


def timeit(func):
    def timed(*args, **kw):
        ts = time.time()
        result = func(*args, **kw)
        te = time.time()
        print(round(te - ts, 3), 's')
        return result
    return timed


@timeit
def append_values(array, n):
    for i in range(n):
        array.append(i)
    print(array.__class__.__name__ + ':')

     
@timeit        
def insert_values(array, n):
    for i in range(n):
        array.insert(i // 2, i)
    print(array.__class__.__name__ + ':')


s = SingleArray((0, ))
v = VectorArray(100)
f = FactorArray(10)
m = MatrixArray(100)
d = []

print('Тест производительности добавления нового элемента в конец массива:')
append_values(s, 2500)
append_values(v, 25000)
append_values(f, 200000)
append_values(m, 200000)
append_values(d, 2000000)
print()

s = SingleArray((0, ))
v = VectorArray(100)
f = FactorArray(10)
m = MatrixArray(100)
d = []

print('Тест производительности вставки нового элемента в середину массива:')
insert_values(s, 2500)
insert_values(v, 2500)
insert_values(f, 2500)
insert_values(m, 2500)
insert_values(d, 25000)