import numpy as np
from matrixxx.matrix import Matrix as DunderMatrix
from matrixxx.mixin_matrix import Matrix as MixinMatrix

# Set seed
np.random.seed(0)
# Generate matrices
matrix_a = np.random.randint(0, 10, (10, 10))
matrix_b = np.random.randint(0, 10, (10, 10))

# 1. "dunder" Matrix
m1 = DunderMatrix(matrix_a)
m2 = DunderMatrix(matrix_b)

(m1 + m2).write_to_file("3_1_matrix+.txt")
(m1 * m2).write_to_file("3_1_matrix*.txt")
(m1 @ m2).write_to_file("3_1_matrix@.txt")

# 2. MixinMatrix
m1 = MixinMatrix(matrix_a)
m2 = MixinMatrix(matrix_b)

(m1 + m2).write_to_file("3_2_matrix+.txt")
(m1 * m2).write_to_file("3_2_matrix*.txt")
(m1 @ m2).write_to_file("3_2_matrix@.txt")

# 3. Hash
A = DunderMatrix([
    [1, 2, 3],
    [3, 2, 1],
    [2, 1, 3],
])
B = DunderMatrix([
    [10, 2, 5],
    [6, 3, 2],
    [5, 5, 5],
])
C = DunderMatrix([
    [3, 2, 1],
    [2, 1, 3],
    [1, 3, 2],
])
D = DunderMatrix([
    [10, 2, 5],
    [6, 3, 2],
    [5, 5, 5],
])

assert hash(A) == hash(C)
assert A != C
assert B == D


A.write_to_file('A.txt')
B.write_to_file('B.txt')
C.write_to_file('C.txt')
D.write_to_file('D.txt')

AB = A @ B
CD = C @ D

assert AB != CD

AB.write_to_file('AB.txt')
CD.write_to_file('CD.txt')

with open('hash.txt', 'w') as f:
    f.write(f"{hash(AB)}\n{hash(CD)}")
