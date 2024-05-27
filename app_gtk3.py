import sys
import random
import json
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Pango

from board import Board

class SudokuSolver(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="SudokuSolver")
        self.set_default_size(1280, 720)
        
        self.board = Board()
        self.init_ui()
        self.update_board_view()

    def init_ui(self):
        vbox = Gtk.VBox()
        self.add(vbox)

        self.create_menu(vbox)

        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(b"""
            .square-button {
                border-radius: 0;
                border: 5px solid black;
            }
        """)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        vbox.pack_start(hbox, True, True, 0)

        self.create_board_layout(hbox)
        self.create_panel_layout(hbox)

    def create_board_layout(self, hbox):
        grid = Gtk.Grid()
        hbox.pack_start(grid, True, True, 0)
        
        self.cell_views = []
        for i in range(9):
            for j in range(9):
                cell = self.create_board_cell(i, j)
                grid.attach(cell, j, i, 1, 1)
                self.cell_views.append(cell)

    def create_board_cell(self, i, j):
        cell = Gtk.Button(label="", name="square-button")
        cell.modify_font(Pango.FontDescription("Arial 20"))
        cell.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("white"))
        cell.connect("clicked", self.select_cell_event, i, j)
        return cell

    def create_panel_layout(self, hbox):
        panel_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        hbox.pack_start(panel_box, False, False, 0)

        for number in range(1, 10):
            button = Gtk.Button(label=str(number))
            button.set_size_request(50, 50)
            button.modify_font(Pango.FontDescription("Arial 20"))
            button.connect("clicked", self.input_number_event, number)
            panel_box.add(button)

        eraser_button = Gtk.Button(label="Gumka")
        eraser_button.modify_font(Pango.FontDescription("Arial 20"))
        eraser_button.connect("clicked", self.erase_cell_event)
        panel_box.add(eraser_button)

        new_board_button = Gtk.Button(label="Nowa plansza")
        new_board_button.modify_font(Pango.FontDescription("Arial 15"))
        new_board_button.connect("clicked", self.generate_board)
        panel_box.add(new_board_button)

    def create_menu(self, vbox):
        menu_bar = Gtk.MenuBar()
        vbox.pack_start(menu_bar, False, False, 0)

        file_menu = Gtk.Menu()
        save_action = Gtk.MenuItem(label="Zapisz grę")
        save_action.connect("activate", self.save_game_event)
        load_action = Gtk.MenuItem(label="Wczytaj grę")
        load_action.connect("activate", self.load_game)
        file_menu.append(save_action)
        file_menu.append(load_action)

        file_menu_item = Gtk.MenuItem(label="Plik")
        file_menu_item.set_submenu(file_menu)
        menu_bar.append(file_menu_item)

        options_menu = Gtk.Menu()
        about_action = Gtk.MenuItem(label="O aplikacji")
        about_action.connect("activate", self.show_about_event)
        options_menu.append(about_action)

        options_menu_item = Gtk.MenuItem(label="Opcje")
        options_menu_item.set_submenu(options_menu)
        menu_bar.append(options_menu_item)

    def update_board_view(self):
        for i in range(9):
            for j in range(9):
                cell = self.board.get_cells()[i][j]
                cell_view = self.cell_views[i*9 + j]
                cell_view.set_label(str(cell.value) if cell.value != None else "")
                cell_style = self.get_default_cell_style(i, j)

                if(cell == self.board.selected_cell):
                    cell_style += "background-color: lightblue;"

                if(not cell.is_valid):
                    cell_style += "color: red;"

                cell_view.get_style_context().add_class("button")
                #cell_view.get_style_context().set_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(1, 1, 1, 1))

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

    def select_cell_event(self, widget, i, j):
        self.board.set_selected_cell(i,j)
        self.update_board_view()

    def input_number_event(self, widget, number):
        self.board.set_selected_cell_value(number)
        self.update_board_view()

    def erase_cell_event(self, widget):
        self.board.set_selected_cell_value(None)
        self.update_board_view()

    def generate_board(self, widget):
        self.board.generate_sudoku_game()
        self.update_board_view()

    def save_game_event(self, widget):
        dialog = Gtk.FileChooserDialog("Zapisz grę", self, Gtk.FileChooserAction.SAVE, 
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_SAVE, Gtk.ResponseType.ACCEPT))
        dialog.set_do_overwrite_confirmation(True)
        response = dialog.run()
        if response == Gtk.ResponseType.ACCEPT:
            file_path = dialog.get_filename()
            self.board.save(file_path)
        dialog.destroy()

    def load_game(self, widget):
        dialog = Gtk.FileChooserDialog("Wczytaj grę", self, Gtk.FileChooserAction.OPEN, 
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.ACCEPT))
        response = dialog.run()
        if response == Gtk.ResponseType.ACCEPT:
            file_path = dialog.get_filename()
            self.board.load_game(file_path)
            self.update_board_view()
        dialog.destroy()

    def show_about_event(self, widget):
        dialog = Gtk.MessageDialog(parent=self, flags=0, message_type=Gtk.MessageType.INFO, 
                                   buttons=Gtk.ButtonsType.OK, text="SudokuSolver to aplikacja do rozwiązywania sudoku.\n\nAutor: Łukasz Smoliński 184306")
        dialog.run()
        dialog.destroy()

if __name__ == "__main__":
    app = SudokuSolver()
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()
