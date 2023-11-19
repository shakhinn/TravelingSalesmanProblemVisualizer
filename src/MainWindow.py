import random
import sys
from operator import xor
import math
import matplotlib.pyplot as plt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QTableWidget, QApplication, QWidget, QHBoxLayout, QPushButton, QVBoxLayout, \
    QTableWidgetItem, QHeaderView, QMessageBox, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from qtpy import QtCore
from src.TSPSolver import TSPSolver


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("TSP solver")
        matrix = [[1, 27, 43, 16, 30, 26], [7, 1, 16, 1, 30, 25], [20, 13, 1, 35, 5, 0],
                  [21, 16, 25, 1, 18, 18], [12, 46, 27, 48, 1, 5], [23, 5, 5, 9, 5, 1]]
        self.solver = TSPSolver(matrix, callback=self.showTable)
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
        self.label2 = QLabel("Left branch")
        self.label3 = QLabel("Right branch (add to the result)")
        self.label1.setFont(fontLabels)
        self.label2.setFont(fontLabels)
        self.label3.setFont(fontLabels)

        self.buttonNext = QPushButton("Next step")
        font = QFont("Roboto", 14)
        self.buttonNext.setFont(font)
        self.buttonNext.setStyleSheet("background-color: green")
        self.buttonNext.clicked.connect(self.updateWindow)

        self.header1 = self.table1.horizontalHeader()
        self.header2 = self.table2.horizontalHeader()
        self.header3 = self.table3.horizontalHeader()

        for i in range(self.table1.columnCount()):
            self.header1.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
            self.header2.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
            self.header3.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)

        self.matrixLayout = QVBoxLayout()
        self.matrixLayout.addWidget(self.buttonNext)
        self.matrixLayout.addWidget(self.label1)
        self.matrixLayout.addWidget(self.table1)
        self.matrixLayout.addWidget(self.label2)
        self.matrixLayout.addWidget(self.table2)
        self.matrixLayout.addWidget(self.label3)
        self.matrixLayout.addWidget(self.table3)
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.matrixLayout)

        # -----------------------------------
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.button = QPushButton('Plot')
        self.button.clicked.connect(self.plot)
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        self.mainLayout.addLayout(layout)
        self.setLayout(self.mainLayout)
        # -----------------------------------
        self.show()

    def plot(self):
        data = [random.random() for i in range(10)]
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(data, '*-')
        self.canvas.draw()

    def updateWindow(self):
        try:
            next(self.solver)
            print(self.solver.tree.currentRoot["matrix"])
        except StopIteration:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("The algorithm came to the end")
            msg.setWindowTitle("Competed")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

    def showTable(self, tableNumber: int, curMatrix: list, zeros=None):
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

        print(f"table: {tableNumber}, matrix: {curMatrix}")
        table.setRowCount(len(curMatrix))
        table.setColumnCount(len(curMatrix))
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
