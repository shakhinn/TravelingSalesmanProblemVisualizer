from copy import deepcopy
from src.Tree import Tree


class TSPSolver:
    def __init__(self, matrix, matrixCallback, graphCallback):
        for i in range(len(matrix)):
            matrix[i][i] = float('inf')
        self.__StartMatrix = deepcopy(matrix)
        self.tree = Tree(matrix)
        self.firstStep = True
        self.matrixCallback = matrixCallback
        self.graphCallback = graphCallback

    def __iter__(self):
        return self

    def __next__(self):
        if self.firstStep:
            matrix, H = self.__reduceMatrix(self.tree.currentRoot["matrix"], 0)
            self.tree.currentRoot["value"] = H
            self.tree.currentRoot["matrix"] = matrix
            self.firstStep = False
            if self.matrixCallback:
                self.matrixCallback(1, self.tree.currentRoot["matrix"], self.tree.currentRoot["city_cols"],
                                    self.tree.currentRoot["city_rows"])
        else:
            if len(self.tree.currentRoot["matrix"]) > 1:
                # Оцениваем нулевые клетки и ищем нулевую клетку с максимальной оценкой
                NullMax, rowIndex, columnIndex = self.__findMaxZero(self.tree.currentRoot["matrix"])
                self.__addWayToResult(self.tree.currentRoot["matrix"], rowIndex, columnIndex,
                                      deepcopy(self.tree.currentRoot["city_rows"]),
                                      deepcopy(self.tree.currentRoot["city_cols"]))
                self.__skipWay(self.tree.currentRoot["matrix"], NullMax, rowIndex, columnIndex)
                self.tree.currentRoot = self.__findMinNode()
            else:
                self.result = 0
                self.resultPath = ""
                self.result += self.__StartMatrix[self.tree.currentRoot["city_rows"][0]][
                    self.tree.currentRoot["city_cols"][0]]
                print(self.tree.currentRoot["city_rows"][0] + 1, self.tree.currentRoot["city_cols"][0] + 1, sep=", ")
                self.resultPath += f"({self.tree.currentRoot['city_rows'][0] + 1} -> {self.tree.currentRoot['city_cols'][0] + 1}), "
                while self.tree.currentRoot is not None:
                    if len(self.tree.currentRoot["path"]) > 0 and self.tree.currentRoot["path"][0]:
                        self.result += self.__StartMatrix[self.tree.currentRoot["path"][1]][
                            self.tree.currentRoot["path"][2]]
                        self.resultPath += f"({self.tree.currentRoot['path'][1] + 1} -> {self.tree.currentRoot['path'][2] + 1}), "

                    self.tree.currentRoot = self.tree.currentRoot["prev"]

                print(self.result)
                raise StopIteration

    def __findMin(self, lst, myindex):
        return min(x for idx, x in enumerate(lst) if idx != myindex)

    # функция удаления нужной строки и столбцах
    def __deleteRowAndCol(self, matrix, index1, index2):
        del matrix[index1]
        for i in matrix:
            del i[index2]
        return matrix

    # Редукция матрицы
    def __reduceMatrix(self, myMatrix, Hk_1):
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

    def __findMaxZero(self, myMatrix):
        maximum = 0
        index1 = 0
        index2 = 0
        zeros = []
        for i in range(len(myMatrix)):
            for j in range(len(myMatrix)):
                if myMatrix[i][j] == 0:
                    tmp = self.__findMin(myMatrix[i], j) + self.__findMin((row[j] for row in myMatrix), i)
                    zeros.append((tmp, i, j))
                    if tmp >= maximum:
                        maximum = tmp
                        index1 = i
                        index2 = j
        if self.matrixCallback:
            self.matrixCallback(1, myMatrix, self.tree.currentRoot["city_cols"],
                                self.tree.currentRoot["city_rows"], zeros)
        return maximum, index1, index2

    def __addWayToResult(self, _matrix, row, column, city_rows, city_cols):
        matrix_ = deepcopy(_matrix)
        oldIndex1 = city_rows[row]
        oldIndex2 = city_cols[column]
        if oldIndex2 in city_rows and oldIndex1 in city_cols:
            NewIndex1 = city_rows.index(oldIndex2)
            NewIndex2 = city_cols.index(oldIndex1)
            matrix_[NewIndex1][NewIndex2] = float('inf')

        tmpRows = city_rows[row]
        tmpColumns = city_cols[column]
        city_rows.pop(row)
        city_cols.pop(column)
        matrix_ = self.__deleteRowAndCol(matrix_, row, column)
        matrix_, Hk = self.__reduceMatrix(matrix_, self.tree.currentRoot["value"])
        self.tree.currentRoot["right"] = {
            "path": [1, tmpRows, tmpColumns],
            "value": Hk,
            "matrix": matrix_,
            "cycles": deepcopy(self.tree.currentRoot["cycles"]),
            "city_rows": city_rows,
            "city_cols": city_cols,
            "prev": self.tree.currentRoot,
            "left": None,
            "right": None,
        }

        self.__findAndRemoveCycles(self.tree.currentRoot["right"])
        self.tree.availableNodes.append(self.tree.currentRoot["right"])
        if self.matrixCallback:
            self.matrixCallback(2, matrix_, city_cols, city_rows)

    def __skipWay(self, matrix_, maxZero, row, col):
        new_matrix = deepcopy(matrix_)
        new_matrix[row][col] = float("inf")
        new_matrix, _ = self.__reduceMatrix(new_matrix, 0)
        tmpRows = self.tree.currentRoot["city_rows"][row]
        tmpColumns = self.tree.currentRoot["city_cols"][col]
        self.tree.currentRoot["left"] = {
            "path": [0, tmpRows, tmpColumns],
            "value": self.tree.currentRoot["value"] + maxZero,
            "matrix": new_matrix,
            "cycles": deepcopy(self.tree.currentRoot["cycles"]),
            "city_rows": deepcopy(self.tree.currentRoot["city_rows"]),
            "city_cols": deepcopy(self.tree.currentRoot["city_cols"]),
            "prev": self.tree.currentRoot,
            "left": None,
            "right": None,
        }
        self.__findAndRemoveCycles(self.tree.currentRoot["left"])
        self.tree.availableNodes.append(self.tree.currentRoot["left"])
        if self.matrixCallback:
            self.matrixCallback(3, new_matrix, self.tree.currentRoot["city_cols"], self.tree.currentRoot["city_rows"])

    def __findMinNode(self):
        minNode = self.tree.availableNodes[0]
        for i in range(1, len(self.tree.availableNodes)):
            if self.tree.availableNodes[i]["value"] < minNode["value"]:
                minNode = self.tree.availableNodes[i]
        self.tree.availableNodes.remove(minNode)
        if self.graphCallback:
            self.graphCallback()
        return minNode

    def __findAndRemoveCycles(self, node: dict):
        cycles: dict = node["cycles"]
        matrix_: list = node["matrix"]
        city_rows: list = node["city_rows"]
        city_cols: list = node["city_cols"]

        # add edge to dict
        flag = True
        for value in cycles.items():
            if node["path"][0] == 1 and value[1] == node["path"][1] and cycles.get(node["path"][2]) is None:
                cycles[value[0]] = node["path"][2]
                flag = False

        if node["path"][0] == 1 and cycles.get(node["path"][2]) is not None:
            val = cycles.pop(node["path"][2])
            cycles.update([(node["path"][1], val)])
            flag = False

        err = None
        for value in cycles.items():
            if cycles.get(value[1]) is not None:
                err = value
        if err is not None:
            cycles[err[0]] = cycles.pop(err[1])
            flag = False

        if flag:
            cycles.update([(node["path"][1], node["path"][2])])

        # find cycles
        for i in range(len(city_rows)):
            for j in range(len(city_cols)):
                if cycles.get(city_cols[j]) is not None:
                    if cycles.get(city_cols[j]) == city_rows[i]:
                        matrix_[i][j] = float('inf')
