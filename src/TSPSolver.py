from Tree import Tree
from copy import deepcopy


class TSPSolver:
    def __init__(self, matrix):
        for i in range(len(matrix)):
            matrix[i][i] = float('inf')
        self.tree = Tree(matrix)
        self.firstStep = True

    def __iter__(self):
        return self

    def __next__(self):
        if self.firstStep:
            matrix, H = self.reduceMatrix(self.tree.currentRoot["matrix"], 0)
            self.tree.currentRoot["value"] = H
            self.tree.currentRoot["matrix"] = matrix
            self.firstStep = False
        else:
            if len(self.tree.currentRoot["matrix"]) > 1:
                # Оцениваем нулевые клетки и ищем нулевую клетку с максимальной оценкой
                NullMax, rowIndex, columnIndex = self.findMaxZero(self.tree.currentRoot["matrix"])
                self.addWayToResult(self.tree.currentRoot["matrix"], rowIndex, columnIndex,
                                    deepcopy(self.tree.currentRoot["city_rows"]),
                                    deepcopy(self.tree.currentRoot["city_cols"]))
                self.skipWay(self.tree.currentRoot["matrix"], NullMax, rowIndex, columnIndex)
                self.tree.currentRoot = self.findMinNode()
            else:
                raise StopIteration

    def Min(self, lst, myindex):
        return min(x for idx, x in enumerate(lst) if idx != myindex)

    # функция удаления нужной строки и столбцах
    def Delete(self, matrix, index1, index2):
        del matrix[index1]
        for i in matrix:
            del i[index2]
        return matrix

    # Редукция матрицы
    def reduceMatrix(self, myMatrix, Hk_1):
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

    def findMaxZero(self, myMatrix):
        maximum = 0
        index1 = 0
        index2 = 0
        for i in range(len(myMatrix)):
            for j in range(len(myMatrix)):
                if myMatrix[i][j] == 0:
                    tmp = self.Min(myMatrix[i], j) + self.Min((row[j] for row in myMatrix), i)
                    if tmp >= maximum:
                        maximum = tmp
                        index1 = i
                        index2 = j
        return maximum, index1, index2

    def addWayToResult(self, _matrix, row, column, city_rows, city_cols):
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
        matrix_ = self.Delete(matrix_, row, column)
        matrix_, Hk = self.reduceMatrix(matrix_, self.tree.currentRoot["value"])
        self.tree.currentRoot["right"] = {
            "path": [1, tmpRows, tmpColms],
            "value": Hk,
            "matrix": matrix_,
            "city_rows": city_rows,
            "city_cols": city_cols,
            "prev": self.tree.currentRoot,
            "left": None,
            "right": None,
        }
        setRows = set(city_rows)
        setCols = set(city_cols)
        difference = list(setRows.symmetric_difference(setCols))
        if len(difference) == 2:
            if difference[0] in city_rows:
                matrix_[city_rows.index(difference[0])][city_cols.index(difference[1])] = float('inf')
            else:
                matrix_[city_rows.index(difference[1])][city_cols.index(difference[0])] = float('inf')

        self.tree.availableNodes.append(self.tree.currentRoot["right"])

    def skipWay(self, matrix_, maxZero, row, col):
        new_matrix = deepcopy(matrix_)
        new_matrix[row][col] = float("inf")
        new_matrix, _ = self.reduceMatrix(new_matrix, 0)
        self.tree.currentRoot["left"] = {
            "path": [0, row, col],
            "value": self.tree.currentRoot["value"] + maxZero,
            "matrix": new_matrix,
            "city_rows": deepcopy(self.tree.currentRoot["city_rows"]),
            "city_cols": deepcopy(self.tree.currentRoot["city_cols"]),
            "prev": self.tree.currentRoot,
            "left": None,
            "right": None,
        }

        # TODO prohibit cycles
        setRows = set(self.tree.currentRoot["left"]["city_rows"])
        setCols = set(self.tree.currentRoot["left"]["city_cols"])
        difference = list(setRows.symmetric_difference(setCols))
        if len(difference) == 2:
            if difference[0] in self.tree.currentRoot["left"]["city_rows"]:
                matrix_[self.tree.currentRoot["left"]["city_rows"].index(difference[0])][
                    self.tree.currentRoot["left"]["city_cols"].index(difference[1])] = float('inf')
            else:
                matrix_[self.tree.currentRoot["left"]["city_rows"].index(difference[1])][
                    self.tree.currentRoot["left"]["city_cols"].index(difference[0])] = float('inf')

        self.tree.availableNodes.append(self.tree.currentRoot["left"])

    def findMinNode(self):
        minNode = self.tree.availableNodes[0]
        for i in range(1, len(self.tree.availableNodes)):
            if self.tree.availableNodes[i]["value"] < minNode["value"]:
                minNode = self.tree.availableNodes[i]
        self.tree.availableNodes.remove(minNode)
        return minNode
