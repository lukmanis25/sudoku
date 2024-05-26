import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt


class SudokuBoard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sudoku")
        self.setGeometry(100, 100, 400, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Tworzenie siatki głównej
        main_grid = QGridLayout()
        layout.addLayout(main_grid)

        # Tworzenie przycisków
        self.buttons = []
        for i in range(9):
            row = []
            for j in range(9):
                button = QPushButton("")
                button.setStyleSheet(
                    """
                    background-color: white;
                    border: 1px solid black;
                    font-size: 20px;
                    """
                )
                button.setFixedSize(40, 40)
                row.append(button)
                main_grid.addWidget(button, i, j)

            self.buttons.append(row)

        # Dodanie linii oddzielających sekcje planszy
        for i in range(1, 3):
            for j in range(3):
                line = QLabel()
                line.setFrameShape(QLabel.VLine)
                line.setFrameShadow(QLabel.Sunken)
                main_grid.addWidget(line, i * 3, j * 3 - 1)

        for i in range(1, 3):
            for j in range(3):
                line = QLabel()
                line.setFrameShape(QLabel.HLine)
                line.setFrameShadow(QLabel.Sunken)
                main_grid.addWidget(line, j * 3 - 1, i * 3)

        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SudokuBoard()
    sys.exit(app.exec_())
