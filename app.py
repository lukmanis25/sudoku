import sys
import random
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QMenuBar, QAction, QLabel, QFileDialog, QMessageBox, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor

class SudokuSolver(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SudokuSolver")
        self.setGeometry(100, 100, 600, 700)
        #self.setGeometry(300, 300, 300, 200)

        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.initUI()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(0)
        self.create_board()

        self.panel_layout = QVBoxLayout()
        self.create_panel()

        self.main_layout = QHBoxLayout()
        self.main_layout.addLayout(self.grid_layout, 2)
        self.main_layout.addLayout(self.panel_layout, 1)
        self.central_widget.setLayout(self.main_layout)

        self.create_menu()

    def create_board(self):
        self.cells = []
        for i in range(9):
            row = []
            for j in range(9):
                cell = QPushButton("")
                #cell.setFixedSize(50, 50)
                cell.setFont(QFont("Arial", 20))
                cell.setStyleSheet(self.get_cell_style(i, j))
                cell.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                cell.clicked.connect(self.select_cell)
                self.grid_layout.addWidget(cell, i, j)
                row.append(cell)
            self.cells.append(row)
        self.selected_cell = None

    def get_cell_style(self, i, j):
        style = "background-color: white; border: 1px solid black;"
        if i % 3 == 0 and i != 0:
            style += "border-top: 2px solid black;"
        if j % 3 == 0 and j != 0:
            style += "border-left: 2px solid black;"
        if (i + 1) % 3 == 0 and (i + 1) != 9:
            style += "border-bottom: 2px solid black;"
        if (j + 1) % 3 == 0 and (j + 1) != 9:
            style += "border-right: 2px solid black;"
        return style

    def create_panel(self):
        for number in range(1, 10):
            button = QPushButton(str(number))
            button.setFixedSize(50, 50)
            button.setFont(QFont("Arial", 20))
            button.clicked.connect(self.input_number)
            self.panel_layout.addWidget(button)

        self.eraser_button = QPushButton("Gumka")
        #self.eraser_button.setFixedSize(50, 50)
        self.eraser_button.setFont(QFont("Arial", 20))
        self.eraser_button.clicked.connect(self.erase_cell)
        self.panel_layout.addWidget(self.eraser_button)

        self.new_board_button = QPushButton("Nowa plansza")
        #self.new_board_button.setFixedSize(100, 50)
        self.new_board_button.setFont(QFont("Arial", 15))
        self.new_board_button.clicked.connect(self.generate_board)
        self.panel_layout.addWidget(self.new_board_button)

    def create_menu(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("Plik")
        save_action = QAction("Zapisz grę", self)
        save_action.triggered.connect(self.save_game)
        load_action = QAction("Wczytaj grę", self)
        load_action.triggered.connect(self.load_game)
        file_menu.addAction(save_action)
        file_menu.addAction(load_action)

        options_menu = menu_bar.addMenu("Opcje")
        about_action = QAction("O aplikacji", self)
        about_action.triggered.connect(self.show_about)
        options_menu.addAction(about_action)

    def select_cell(self):
        button = self.sender()
        if self.selected_cell:
            self.selected_cell.setStyleSheet(self.get_cell_style(*self.get_cell_position(self.selected_cell)))
        self.selected_cell = button
        self.selected_cell.setStyleSheet("background-color: lightblue;")

    def input_number(self):
        if not self.selected_cell:
            return

        button = self.sender()
        number = int(button.text())
        row, col = self.get_cell_position(self.selected_cell)
        
        self.board[row][col] = number
        self.selected_cell.setText(str(number))
        self.check_board()

    def erase_cell(self):
        if not self.selected_cell:
            return

        row, col = self.get_cell_position(self.selected_cell)
        self.board[row][col] = 0
        self.selected_cell.setText("")

    def generate_board(self):
        self.board = self.generate_sudoku()
        self.update_board()

    def save_game(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Zapisz grę", "", "JSON Files (*.json);;All Files (*)", options=options)
        if file_path:
            with open(file_path, 'w') as file:
                json.dump(self.board, file)

    def load_game(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Wczytaj grę", "", "JSON Files (*.json);;All Files (*)", options=options)
        if file_path:
            with open(file_path, 'r') as file:
                self.board = json.load(file)
            self.update_board()

    def show_about(self):
        QMessageBox.about(self, "O aplikacji", "SudokuSolver to aplikacja do rozwiązywania sudoku.\n\nAutor: TwójAutor")

    def update_board(self):
        for i in range(9):
            for j in range(9):
                value = self.board[i][j]
                self.cells[i][j].setText(str(value) if value != 0 else "")
                self.cells[i][j].setStyleSheet(self.get_cell_style(i, j))

    def get_cell_position(self, button):
        for i in range(9):
            for j in range(9):
                if self.cells[i][j] == button:
                    return i, j
        return None, None

    def check_board(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != 0:
                    if not self.is_valid(i, j):
                        self.cells[i][j].setStyleSheet(self.get_cell_style(i, j) + "color: red;")
                    else:
                        self.cells[i][j].setStyleSheet(self.get_cell_style(i, j) + "color: black;")

    def is_valid(self, row, col):
        num = self.board[row][col]
        self.board[row][col] = 0

        for i in range(9):
            if self.board[row][i] == num or self.board[i][col] == num:
                self.board[row][col] = num
                return False

        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.board[start_row + i][start_col + j] == num:
                    self.board[row][col] = num
                    return False

        self.board[row][col] = num
        return True

    def generate_sudoku(self):
        # Simple random sudoku generator for demonstration
        # For a real sudoku generator, replace with a more complex algorithm
        board = [[0 for _ in range(9)] for _ in range(9)]
        for _ in range(30):
            row, col = random.randint(0, 8), random.randint(0, 8)
            while board[row][col] != 0:
                row, col = random.randint(0, 8), random.randint(0, 8)
            num = random.randint(1, 9)
            board[row][col] = num
            if not self.is_valid(row, col):
                board[row][col] = 0
        return board

if __name__ == '__main__':
    app = QApplication(sys.argv)
    solver = SudokuSolver()
    solver.show()
    sys.exit(app.exec_())
