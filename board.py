import json
import random

class Board():
    def __init__(self):
        self.cells = [[BoardCell() for j in range(9)] for i in range(9)]
        self.selected_cell = None

    def get_cells(self):
        return self.cells

    def set_selected_cell(self, i: int, j: int):
        self.selected_cell = self.cells[i][j]

    def set_selected_cell_value(self, value: int):
        if self.selected_cell == None:
            return
        self.selected_cell.value = value
        self.check_board()

    def check_board(self):
        for i in range(9):
            for j in range(9):
                if self.cells[i][j].value != None:
                    if not self.is_valid(i, j):
                        self.cells[i][j].is_valid = False
                        #self.cell_views[i][j].setStyleSheet(self.get_default_cell_style(i, j) + "color: red;")
                    else:
                        self.cells[i][j].is_valid = True
                        #self.cell_views[i][j].setStyleSheet(self.get_default_cell_style(i, j) + "color: black;")

    def is_valid(self, row, col):
        num = self.cells[row][col].value
        self.cells[row][col].value = None

        for i in range(9):
            if self.cells[row][i].value == num or self.cells[i][col].value == num:
                self.cells[row][col].value = num
                return False

        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.cells[start_row + i][start_col + j].value == num:
                    self.cells[row][col].value = num
                    return False

        self.cells[row][col].value = num
        return True
    
    def find_empty(self):
        for i in range(9):
            for j in range(9):
                if self.cells[i][j].value is None:
                    return i, j
        return None

    def solve(self):
        empty = self.find_empty()
        if not empty:
            return True
        row, col = empty

        for num in range(1, 10):
            self.cells[row][col].value = num
            if self.is_valid(row, col):
                if self.solve():
                    return True
            self.cells[row][col].value = None

        return False

    def generate_full_board(self):
        self.solve()

    def remove_numbers(self, num_holes):
        while num_holes > 0:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if self.cells[row][col].value is not None:
                self.cells[row][col].value = None
                self.cells[row][col].is_modifiable = True
                num_holes -= 1

    def generate_sudoku_game(self):
        self.clear()
        self.generate_full_board()
        num_holes = 40
        self.remove_numbers(num_holes)
        for i in range(9):
            for j in range(9):
                if self.cells[i][j].value is not None:
                    self.cells[i][j].is_modifiable = False

    def clear(self):
        self.cells = [[BoardCell() for j in range(9)] for i in range(9)]
    
    def save(self, file_path):
        if file_path:
            with open(file_path, 'w') as file:
                json.dump(self.cells, file, cls=BoardCellEncoder)

    def load_game(self, file_path):
        try:
            if file_path:
                with open(file_path, 'r') as file:
                    self.cells = json.load(file, object_hook=board_cell_decoder)
        except:
            print("bad file")

class BoardCell():
    def __init__(self,value: int = None):
        self.value = value
        self.is_valid = True
        self.is_modifiable = True

    def to_dict(self):
        return {
            'value': self.value,
            'is_valid': self.is_valid,
            'is_modifiable': self.is_modifiable
        }
    
class BoardCellEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, BoardCell):
            return obj.to_dict()
        return super().default(obj)

def board_cell_decoder(dct):
    if 'value' in dct and 'is_valid' in dct and 'is_modifiable' in dct:
        cell = BoardCell(dct['value'])
        cell.is_valid = dct['is_valid']
        cell.is_modifiable = dct['is_modifiable']
        return cell
    return dct