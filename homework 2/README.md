Тест производительности добавления нового элемента в конец массива
------------------
### Параметры:
```
s = SingleArray((0, ))
v = VectorArray(100)
f = FactorArray(10)
m = MatrixArray(100)
d = []

append_values(s, 2500)
append_values(v, 25000)
append_values(f, 200000)
append_values(m, 200000)
append_values(d, 2000000)
```

### Результаты:
```
SingleArray:
1.01 s
VectorArray:
1.036 s
FactorArray:
0.888 s
MatrixArray:
0.981 s
list:
0.163 s
```
SingleArray показывает себя хуже всех. За ним идет VectorArray. FactorArray и MatrixArray примерно равны, но при увеличении количества добавляемых элементов FactorArray начинает отрываться.


Тест производительности вставки нового элемента в середину массива:
---------
### Параметры:
```
s = SingleArray((0, ))
v = VectorArray(100)
f = FactorArray(10)
m = MatrixArray(100)
d = []

insert_values(s, 2500)
insert_values(v, 2500)
insert_values(f, 2500)
insert_values(m, 2500)
insert_values(d, 25000)
```

### Результаты:
```
SingleArray:
1.056 s
VectorArray:
0.568 s
FactorArray:
0.563 s
MatrixArray:
2.353 s
list:
0.058 s
```
MatrixArray показывает себя хуже всех. За ним идет SingleArray. FactorArray и Vector примерно равны.