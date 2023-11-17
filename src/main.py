from Tree import Tree
from copy import deepcopy

from src.TSPSolver import TSPSolver

n = int(input())
matrix = []
StartMatrix = []

# Вводим матрицу
for i in range(n):
    matrix.append(list(map(int, input().split())))

# Сохраняем изначальную матрицу
for i in range(n):
    StartMatrix.append(matrix[i].copy())

solver = TSPSolver(matrix)
# Присваеваем главной диагонали float(inf)


for i in solver:
    continue



# print(tree.currentRoot["value"])
result = 0
result += StartMatrix[solver.tree.currentRoot["city_rows"][0]][solver.tree.currentRoot["city_cols"][0]]
print(solver.tree.currentRoot["city_rows"][0], solver.tree.currentRoot["city_cols"][0], sep=", ")
while solver.tree.currentRoot is not None:
    if len(solver.tree.currentRoot["path"]) > 0 and solver.tree.currentRoot["path"][0]:
        result += StartMatrix[solver.tree.currentRoot["path"][1]][solver.tree.currentRoot["path"][2]]
    print(solver.tree.currentRoot["path"])
    solver.tree.currentRoot = solver.tree.currentRoot["prev"]

print(result)
'''
5
1 20 18 12 8
5 1 14 7 11
12 18 1 6 11
11 17 11 1 12
5 5 5 5 1
'''

'''
6
1 27 43 16 30 26
7 1 16 1 30 25
20 13 1 35 5 0
21 16 25 1 18 18
12 46 27 48 1 5
23 5 5 9 5 1
'''

'''
6
1 4	4 5	4 3	
2 1	7 1	1 6
2 3	1 9	4 5	
1 3	2 1	3 1	
7 4	1 1	1 4	
2 3	4 7	9 1	
'''
