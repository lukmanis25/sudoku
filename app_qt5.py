import sys
import random
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QMenuBar, QAction, QLabel, QFileDialog, QMessageBox, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor
from board import Board

class SudokuSolver(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SudokuSolver")
        self.setGeometry(100, 100, 1280, 720)
        #self.setGeometry(300, 300, 300, 200)

        self.board = Board()
        self.initUI()
        self.update_board_view()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.board_layout = QGridLayout()
        self.board_layout.setSpacing(0)
        self.create_board_layout()

        self.panel_layout = QVBoxLayout()
        self.create_panel_layout()

        self.main_layout = QHBoxLayout()
        self.main_layout.addLayout(self.board_layout, 5)
        self.main_layout.addLayout(self.panel_layout, 1)
        self.central_widget.setLayout(self.main_layout)

        self.create_menu()

    def create_board_layout(self):
        self.cell_views = []
        for i in range(9):
            row = []
            for j in range(9):
                cell = self.create_board_cell(i, j)
                self.board_layout.addWidget(cell, i, j)
                row.append(cell)
            self.cell_views.append(row)


    def create_board_cell(self,i, j, is_modifiable=True):        
        cell = QPushButton("")
        cell.setFont(QFont("Arial", 20))
        cell.setStyleSheet(self.get_default_cell_style(i, j))
        cell.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        cell.clicked.connect(lambda _, x=i, y=j: self.select_cell_event(x, y))
        if(not is_modifiable):
            cell.setEnabled(False)
        return cell

    def create_panel_layout(self):
        for number in range(1, 10):
            button = QPushButton(str(number))
            #button.setFixedSize(50, 50)
            button.setFont(QFont("Arial", 20))
            button.clicked.connect(lambda _, n=number: self.input_number_event(n))
            self.panel_layout.addWidget(button)

        self.eraser_button = QPushButton("Gumka")
        #self.eraser_button.setFixedSize(50, 50)
        self.eraser_button.setFont(QFont("Arial", 20))
        self.eraser_button.clicked.connect(self.erase_cell_event)
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
        save_action.triggered.connect(self.save_game_event)
        load_action = QAction("Wczytaj grę", self)
        load_action.triggered.connect(self.load_game)
        file_menu.addAction(save_action)
        file_menu.addAction(load_action)

        options_menu = menu_bar.addMenu("Opcje")
        about_action = QAction("O aplikacji", self)
        about_action.triggered.connect(self.show_about_event)
        options_menu.addAction(about_action)

    def get_default_cell_style(self, i, j):
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

    def update_board_view(self):
        for i in range(9):
            for j in range(9):
                cell = self.board.get_cells()[i][j]
                cell_view = self.cell_views[i][j]
                cell_view.setText(str(cell.value) if cell.value != None else "")
                cell_style = self.get_default_cell_style(i, j)

                if(cell == self.board.selected_cell):
                    cell_style += "background-color: lightblue;"

                if(not cell.is_valid):
                    cell_style += "color: red;"

                if(not cell.is_modifiable):
                    #cell_style += "text-decoration: underline;"
                    cell_view.setEnabled(False)
                else:
                    cell_view.setEnabled(True)

                cell_view.setStyleSheet(cell_style)



    def select_cell_event(self, i, j):
        self.board.set_selected_cell(i,j)
        self.update_board_view()

    def input_number_event(self, number):
        self.board.set_selected_cell_value(number)
        self.update_board_view()

    def erase_cell_event(self):
        self.board.set_selected_cell_value(None)
        self.update_board_view()

    def generate_board(self):
        self.board.generate_sudoku_game()
        self.update_board_view()

    def save_game_event(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Zapisz grę", "", "JSON Files (*.json);;All Files (*)", options=options)
        self.board.save(file_path)

    def load_game(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Wczytaj grę", "", "JSON Files (*.json);;All Files (*)", options=options)
        self.board.load_game(file_path)
        self.update_board_view()

    def show_about_event(self):
        QMessageBox.about(self, "O aplikacji", "SudokuSolver to aplikacja do rozwiązywania sudoku.\n\nAutor: Łukasz Smoliński 184306")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    solver = SudokuSolver()
    solver.show()
    sys.exit(app.exec_())
