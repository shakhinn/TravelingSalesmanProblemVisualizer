import random
import sys
from operator import xor
from src.TSPSolver import TSPSolver
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QTableWidget, QApplication, QWidget, QHBoxLayout, QPushButton, QVBoxLayout, QDialog, \
    QTableWidgetItem, QHeaderView, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from pyqt5_plugins.examples.exampleqmlitem import QtCore


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("TSP solver")
        matrix = [[1, 27, 43, 16, 30, 26], [7, 1, 16, 1, 30, 25], [20, 13, 1, 35, 5, 0],
                  [21, 16, 25, 1, 18, 18], [12, 46, 27, 48, 1, 5], [23, 5, 5, 9, 5, 1]]
        self.solver = TSPSolver(matrix)
        self.table1 = QTableWidget()
        self.table1.setMinimumSize(510, 500)
        self.table1.setRowCount(6)
        self.table1.setColumnCount(6)

        self.table2 = QTableWidget()
        self.table2.setMinimumSize(510, 500)
        self.table2.setRowCount(6)
        self.table2.setColumnCount(6)

        self.table3 = QTableWidget()
        self.table3.setMinimumSize(510, 500)
        self.table3.setRowCount(6)
        self.table3.setColumnCount(6)
        self.buttonNext = QPushButton("Next step")
        font = QFont("Roboto", 14)
        self.buttonNext.setFont(font)
        self.buttonNext.setStyleSheet("background-color: green")
        self.buttonNext.clicked.connect(self.updateWindow)

        header1 = self.table1.horizontalHeader()
        header2 = self.table2.horizontalHeader()
        header3 = self.table3.horizontalHeader()

        for i in range(self.table1.columnCount()):
            header1.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
            header2.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
            header3.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)

        self.matrixLayout = QVBoxLayout()
        self.matrixLayout.addWidget(self.buttonNext)
        self.matrixLayout.addWidget(self.table1)
        self.matrixLayout.addWidget(self.table2)
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
            self.showTable()
        except StopIteration:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("The algorithm came to the end")
            msg.setWindowTitle("Competed")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

    def showTable(self):
        self.table1.clearContents()
        records = self.solver.tree.currentRoot["matrix"]
        for i in range(len(records)):
            self.table1.setRowCount(len(records))
            self.table1.setColumnCount(len(records))
            for j in range(len(records[i])):
                item1 = QTableWidgetItem(str(records[i][j]))
                item1.setFlags(xor(item1.flags(), QtCore.Qt.ItemIsEditable))
                item2 = QTableWidgetItem(str(records[i][j]))
                item2.setFlags(xor(item1.flags(), QtCore.Qt.ItemIsEditable))
                item3 = QTableWidgetItem(str(records[i][j]))
                item3.setFlags(xor(item3.flags(), QtCore.Qt.ItemIsEditable))
                item4 = QTableWidgetItem(str(records[i][j]))
                item4.setFlags(xor(item4.flags(), QtCore.Qt.ItemIsEditable))
                item5 = QTableWidgetItem(str(records[i][j]))
                item5.setFlags(xor(item5.flags(), QtCore.Qt.ItemIsEditable))
                self.table1.setItem(i, j, item1)
                self.table1.setItem(i, j, item2)
                self.table1.setItem(i, j, item3)
                self.table1.setItem(i, j, item4)
                self.table1.setItem(i, j, item5)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
