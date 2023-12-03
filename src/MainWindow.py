import math
import sys
from copy import deepcopy
from operator import xor

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QStandardItemModel
from PyQt5.QtWidgets import QTableWidget, QApplication, QWidget, QHBoxLayout, \
    QPushButton, QVBoxLayout, QTableWidgetItem, QHeaderView, QMessageBox, QLabel
from treelib import Tree

from src.TSPSolver import TSPSolver
from src.InputWindow import InputWindow


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("TSP solver")
        self.setGeometry(800, 800, 800, 800)
        self.solver = None
        self.flag = True
        self.inputWindow = InputWindow()

        self.table1 = QTableWidget()
        self.table1.setMinimumSize(510, 470)
        self.table1.setRowCount(6)
        self.table1.setColumnCount(6)

        self.table2 = QTableWidget()
        self.table2.setMinimumSize(510, 470)
        self.table2.setRowCount(6)
        self.table2.setColumnCount(6)

        self.table3 = QTableWidget()
        self.table3.setMinimumSize(510, 470)
        self.table3.setRowCount(6)
        self.table3.setColumnCount(6)

        fontLabels = QFont("Roboto", 12)
        self.label1 = QLabel("Max Zeros")
        self.label2 = QLabel("Right branch (add to the result)")
        self.label3 = QLabel("Left branch")
        self.label1.setFont(fontLabels)
        self.label2.setFont(fontLabels)
        self.label3.setFont(fontLabels)

        self.buttonNext = QPushButton("Next step")
        self.buttonMatrix = QPushButton("Insert matrix")
        self.font = QFont("Roboto", 14)
        self.buttonNext.setFont(self.font)
        self.buttonMatrix.setFont(self.font)
        self.buttonNext.setStyleSheet("background-color: green")
        self.buttonMatrix.setStyleSheet("background-color: cyan")
        self.buttonNext.clicked.connect(self.updateWindow)
        self.buttonMatrix.clicked.connect(self.inputWindow.invoke)

        self.header1 = self.table1.horizontalHeader()
        self.header2 = self.table2.horizontalHeader()
        self.header3 = self.table3.horizontalHeader()

        for i in range(self.table1.columnCount()):
            self.header1.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
            self.header2.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
            self.header3.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)

        self.graphFont = QFont("Roboto", 18)
        self.graph = QLabel("0")
        self.graph.setFont(self.font)
        self.graphLabel = QLabel("Tree")
        self.graphLabel.setFont(self.font)
        self.graphLabel.setStyleSheet("background-color: yellow")
        self.graphLabel.setAlignment(Qt.AlignCenter)

        self.matrixLayout = QVBoxLayout()
        self.graphLayout = QVBoxLayout()
        self.matrixLayout.addWidget(self.buttonNext)
        self.matrixLayout.addWidget(self.label1)
        self.matrixLayout.addWidget(self.table1)
        self.graphLayout.addWidget(self.graphLabel)
        self.graphLayout.addWidget(self.graph)
        self.matrixLayout.addLayout(self.graphLayout)

        self.mainLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.matrixLayout)

        # -----------------------------------

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.buttonMatrix)
        self.layout.addWidget(self.label2)
        self.layout.addWidget(self.table2)
        self.layout.addWidget(self.label3)
        self.layout.addWidget(self.table3)
        self.mainLayout.addLayout(self.layout)
        self.setLayout(self.mainLayout)
        # -----------------------------------
        self.show()

    def drawGraph(self):
        tree = Tree()
        tree.create_node(f"root, weight: {self.solver.tree.treeRoot['value']}", str(self.solver.tree.treeRoot["path"]))
        self.addNodeToDrawingTree(tree, self.solver.tree.treeRoot['left'])
        self.addNodeToDrawingTree(tree, self.solver.tree.treeRoot['right'])
        self.graph.setGeometry(300, 350, 300, 150)
        self.graph.setWordWrap(True)
        self.graph.setText(str(tree))

    def addNodeToDrawingTree(self, tree, node):
        if node is None:
            return
        text = "add" if node["path"][0] else "skip"
        tree.create_node(f"{text} route:[{node['path'][1]+1},{node['path'][2]+1}] weight: {node['value']}", str(node['path']), parent=str(node['prev']['path']))
        self.addNodeToDrawingTree(tree, node['left'])
        self.addNodeToDrawingTree(tree, node['right'])

    def updateWindow(self):
        if self.inputWindow.inputMatrix is None:
            self.inputWindow.invoke()
            return
        if self.solver is None:
            self.solver = TSPSolver(self.inputWindow.inputMatrix, matrixCallback=self.showTable, graphCallback=self.drawGraph)
        try:
            next(self.solver)
        except StopIteration:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText(f"The algorithm came to the end, result = {self.solver.result}\n{self.solver.resultPath}")
            msg.setWindowTitle("Competed")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

    def showTable(self, tableNumber: int, curMatrix: list, horizontalLabels: list, verticalLabels: list, zeros=None):
        horizontalLabels_str = deepcopy(horizontalLabels)
        verticalLabels_str = deepcopy(verticalLabels)
        for i in range(len(horizontalLabels_str)):
            horizontalLabels_str[i] = str(horizontalLabels_str[i]+1)

        for i in range(len(verticalLabels_str)):
            verticalLabels_str[i] = str(verticalLabels_str[i]+1)

        table = None
        header = None
        if tableNumber == 1:
            table = self.table1
            header = self.header1
        elif tableNumber == 2:
            table = self.table2
            header = self.header2
        elif tableNumber == 3:
            table = self.table3
            header = self.header3

        table.setRowCount(len(curMatrix))
        table.setColumnCount(len(curMatrix))
        table.setHorizontalHeaderLabels(horizontalLabels_str)
        table.setVerticalHeaderLabels(verticalLabels_str)

        for i in range(table.rowCount()):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
        for i in range(len(curMatrix)):
            for j in range(len(curMatrix[i])):
                value = curMatrix[i][j]
                if math.isnan(curMatrix[i][j]):
                    value = float("inf")
                item = QTableWidgetItem(str(value))
                item.setFlags(xor(item.flags(), QtCore.Qt.ItemIsEditable))
                table.setItem(i, j, item)
        if zeros is not None:
            for i in range(len(zeros)):
                value = "0(" + str(zeros[i][0]) + ")"
                item = QTableWidgetItem(value)
                item.setFlags(xor(item.flags(), QtCore.Qt.ItemIsEditable))
                table.setItem(zeros[i][1], zeros[i][2], item)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
