import random
import sys
from PyQt5.QtWidgets import QTableWidget, QApplication, QWidget, QHBoxLayout, QPushButton, QVBoxLayout, QDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("TSP solver")
        self.table = QTableWidget()
        self.table.setMinimumSize(1100, 500)
        self.table.setRowCount(5)
        self.table.setColumnCount(5)
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addWidget(self.table)

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
        # self.setLayout(layout)
        self.setLayout(self.mainLayout)
        # -----------------------------------

        # self.table.show()
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
