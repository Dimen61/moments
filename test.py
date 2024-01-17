import sys
from PySide2.QtWidgets import (
    QApplication, QMainWindow, QLabel, 
    QLineEdit, QVBoxLayout, QWidget,
    QHBoxLayout
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        self.label = QLabel()

        self.input = QLineEdit()
        self.input.textChanged.connect(self.label.setText)

        layout = QVBoxLayout()
        layout.addWidget(self.input)
        layout.addWidget(self.label)

        label2 = QLabel()
        label2.setText("Label 2")

        label3 = QLabel()
        label3.setText("Label 3")

        child_layout = QHBoxLayout()
        child_layout.addWidget(label2)
        child_layout.addWidget(label3)

        layout.addLayout(child_layout)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()