from Tree import Tree
from copy import deepcopy

n = int(input())
matrix = []

cityRows = []
cityColumns = []
StartMatrix = []
tree = Tree()


# Функция нахождения минимального элемента, исключая текущий элемент
def Min(lst, myindex):
    return min(x for idx, x in enumerate(lst) if idx != myindex)


# функция удаления нужной строки и столбцах
def Delete(matrix, index1, index2):
    del matrix[index1]
    for i in matrix:
        del i[index2]
    return matrix


# Функция вывода матрицы
def PrintMatrix(matrix):
    print("---------------")
    for i in range(len(matrix)):
        print(matrix[i])
    print("---------------")


# Редукция матрицы
def reduceMatrix(myMatrix, Hk_1):
    H_0 = 0
    for i in range(len(myMatrix)):
        temp = min(myMatrix[i])
        H_0 += temp
        for j in range(len(myMatrix)):
            myMatrix[i][j] -= temp

    # Вычитаем минимальный элемент в столбцах
    for i in range(len(myMatrix)):
        temp = min(row[i] for row in myMatrix)
        H_0 += temp
        for j in range(len(myMatrix)):
            myMatrix[j][i] -= temp

    H_0 += Hk_1
    return myMatrix, H_0


def findMaxZero(myMatrix):
    maximum = 0
    index1 = 0
    index2 = 0
    for i in range(len(myMatrix)):
        for j in range(len(myMatrix)):
            if myMatrix[i][j] == 0:
                tmp = Min(myMatrix[i], j) + Min((row[j] for row in myMatrix), i)
                if tmp > maximum:
                    maximum = tmp
                    index1 = i
                    index2 = j
    return maximum, index1, index2


def addWayToResult(_matrix, row, column, city_rows, city_cols):
    matrix_ = deepcopy(_matrix)
    oldIndex1 = city_rows[row]
    oldIndex2 = city_cols[column]
    if oldIndex2 in city_rows and oldIndex1 in city_cols:
        NewIndex1 = city_rows.index(oldIndex2)
        NewIndex2 = city_cols.index(oldIndex1)
        matrix_[NewIndex1][NewIndex2] = float('inf')

    tmpRows = city_rows[row]
    tmpColms = city_cols[column]
    city_rows.pop(row)
    city_cols.pop(column)
    matrix_ = Delete(matrix_, row, column)
    matrix_, Hk = reduceMatrix(matrix_, tree.currentRoot["value"])
    tree.currentRoot["right"] = {
            "path": [1, tmpRows, tmpColms],
            "value": Hk,
            "matrix": matrix_,
            "city_rows": city_rows,
            "city_cols": city_cols,
            "prev": tree.currentRoot,
            "left": None,
            "right": None,
        }
    tree.availableNodes.append(tree.currentRoot["right"])


def skipWay(matrix_, maxZero, row, col):
    new_matrix = deepcopy(matrix_)
    new_matrix[row][col] = float("inf")
    new_matrix, _ = reduceMatrix(new_matrix, 0)
    tree.currentRoot["left"] = {
        "path": [0, row, col],
        "value": tree.currentRoot["value"] + maxZero,
        "matrix": new_matrix,
        "city_rows": deepcopy(tree.currentRoot["city_rows"]),
        "city_cols": deepcopy(tree.currentRoot["city_cols"]),
        "prev": tree.currentRoot,
        "left": None,
        "right": None,
    }
    tree.availableNodes.append(tree.currentRoot["left"])


def findMinNode():
    minNode = tree.availableNodes[0]
    for i in range(1, len(tree.availableNodes)):
        if tree.availableNodes[i]["value"] < minNode["value"]:
            minNode = tree.availableNodes[i]
    tree.availableNodes.remove(minNode)
    return minNode


# Инициализируем массивы для сохранения индексов
for i in range(n):
    cityRows.append(i)
    cityColumns.append(i)

# Вводим матрицу
for i in range(n):
    matrix.append(list(map(int, input().split())))

# Сохраняем изначальную матрицу
for i in range(n):
    StartMatrix.append(matrix[i].copy())

# Присваеваем главной диагонали float(inf)
for i in range(n):
    matrix[i][i] = float('inf')

# Редуцируем ориг матрицу

matrix, H = reduceMatrix(matrix, 0)
tree.currentRoot["value"] = H
tree.currentRoot["matrix"] = matrix
tree.currentRoot["city_rows"] = cityRows
tree.currentRoot["city_cols"] = cityColumns

while len(tree.currentRoot["matrix"]) > 1:

    # Оцениваем нулевые клетки и ищем нулевую клетку с максимальной оценкой
    NullMax, rowIndex, columnIndex = findMaxZero(tree.currentRoot["matrix"])
    addWayToResult(tree.currentRoot["matrix"], rowIndex, columnIndex, deepcopy(tree.currentRoot["city_rows"]), deepcopy(tree.currentRoot["city_cols"]))
    skipWay(tree.currentRoot["matrix"], NullMax, rowIndex, columnIndex)
    tree.currentRoot = findMinNode()



# # Формируем порядок пути
# for i in range(0, len(res) - 1, 2):
#     if res.count(res[i]) < 2:
#         result.append(res[i])
#         result.append(res[i + 1])
# for i in range(0, len(res) - 1, 2):
#     for j in range(0, len(res) - 1, 2):
#         if result[len(result) - 1] == res[j]:
#             result.append(res[j])
#             result.append(res[j + 1])
# print("----------------------------------")
# print(result)
#
# # Считаем длину пути
# for i in range(0, len(result) - 1, 2):
#     if i == len(result) - 2:
#         PathLength += StartMatrix[result[i] - 1][result[i + 1] - 1]
#         PathLength += StartMatrix[result[i + 1] - 1][result[0] - 1]
#     else:
#         PathLength += StartMatrix[result[i] - 1][result[i + 1] - 1]
# print(PathLength)
# print("----------------------------------")

# print(tree.currentRoot["value"])
result = 0
result += StartMatrix[tree.currentRoot["city_rows"][0]][tree.currentRoot["city_cols"][0]]
while tree.currentRoot is not None:
    if len(tree.currentRoot["path"]) > 0 and tree.currentRoot["path"][0]:
        result += StartMatrix[tree.currentRoot["path"][1]][tree.currentRoot["path"][2]]
    print(tree.currentRoot["path"])
    tree.currentRoot = tree.currentRoot["prev"]

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