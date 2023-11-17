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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
