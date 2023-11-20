from PyQt5.QtWidgets import QWidget, QTableWidget, QHBoxLayout, QVBoxLayout, QHeaderView, QPushButton, \
    QComboBox


class InputWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.inputTable = QTableWidget()
        self.inputTable.setMinimumSize(450, 310)
        self.inputTable.resizeColumnsToContents()
        self.header = self.inputTable.horizontalHeader()
        self.inputSize = QComboBox()
        self.inputSize.addItem("4")
        self.inputSize.addItem("5")
        self.inputSize.addItem("6")
        self.inputSize.addItem("7")
        self.setSize()
        self.inputSize.currentTextChanged.connect(self.setSize)

        self.matrixButton = QPushButton("Set matrix")
        self.matrixButton.clicked.connect(self.parseTable)
        self.inputMatrix = None

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.inputSize)
        self.layout.addWidget(self.inputTable)
        self.layout.addWidget(self.matrixButton)

        self.setWindowTitle("Set matrix")
        self.setLayout(self.layout)

    def setSize(self):
        if self.inputSize.currentTextChanged:
            size = int(self.inputSize.currentText())
            print("size: ", size)
            if size > 0:
                self.inputTable.setRowCount(size)
                self.inputTable.setColumnCount(size)
                for i in range(self.inputTable.columnCount()):
                    self.header.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
                self.inputTable.update()

    def invoke(self):
        self.show()

    def parseTable(self):
        self.inputMatrix = []
        for i in range(self.inputTable.rowCount()):
            row = []
            for j in range(self.inputTable.columnCount()):
                row.append(int(self.inputTable.item(i, j).text()))
            self.inputMatrix.append(row)
        self.close()