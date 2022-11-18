from PyQt5.QtWidgets import *
from PyQt5.Qt import *
import sys
import numpy
import random

class Cell(QTableWidgetItem):
    def __init__(self, str, row, column):
        #super().__init__(str)
        super().__init__()
        self.row = row
        self.column = column

        self.is_visited = False
        self.previous_route_cell = None
        self.is_route_initial_cell = False


class Maze(QMainWindow):
    def __init__(self, route_row_count = 10, route_column_count = 10, route_color = "white", wall_color = "black", show_route_log = False):
        super().__init__()
        self.route_row_count = route_row_count
        self.route_column_count = route_column_count
        self.maze_row_count = self.route_row_count * 2 + 1
        self.maze_column_count = self.route_column_count * 2 + 1

        self.maze_map = [None for i in range(self.maze_row_count * self.maze_column_count)]
        self.maze_map = numpy.array(self.maze_map).reshape(self.maze_row_count, self.maze_column_count)
        for i in range(self.maze_row_count):
            for j in range(self.maze_column_count):
                self.maze_map[i][j] = Cell("", i, j)

        self.show_route_log = show_route_log
        self.init_ui()

    # def init_maze(self):
    #     pass

    def init_ui(self):
        self.setGeometry(100, 100, 800, 800)
        self.setWindowTitle("Maze Creator")
        main_layout = QVBoxLayout()

        table_layout = QHBoxLayout()
        table = QTableWidget()
        table.setRowCount(self.maze_row_count)
        table.setColumnCount(self.maze_column_count)
        table.horizontalHeader().hide()
        table.verticalHeader().hide()
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        for i in range(self.maze_row_count):
            for j in range(self.maze_column_count):
                #table.setCellWidget(i, j, self.maze_map[i][j])
                table.setItem(i, j, self.maze_map[i][j])
        table_layout.addWidget(table)
        main_layout.addLayout(table_layout)

        btns_layout = QHBoxLayout()
        show_route_btn = QPushButton("Show route")
        show_route_btn.clicked.connect(self.is_show_route_btn_clicked)
        btns_layout.addWidget(show_route_btn)
        main_layout.addLayout(btns_layout)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        self.show()

    def is_show_route_btn_clicked(self):
        self.generate_maze_route()

    def generate_maze_route(self):
        rand_route_row = random.randint(0, self.route_row_count - 1)
        rand_column_row = random.randint(0, self.route_column_count - 1)

        initial_route_cell = self.maze_map[rand_route_row * 2 + 1][rand_column_row * 2 + 1]
        initial_route_cell.is_visited = True
        current_route_cell = initial_route_cell
        # current_route_cell.setText("aa")
        if self.show_route_log == True: print("Starting from: ", (current_route_cell.row, current_route_cell.column))
        while True:
            next_route_cell = self.get_next_unvisted_cell_on_route(current_route_cell)
            if next_route_cell == None:
                if current_route_cell == initial_route_cell:
                    if self.show_route_log == True: print("No cell to move on.. now at initial cell.. exiting the loop..")
                    break
                else:
                    if self.show_route_log == True: print("No cell to move on.. back to the previous cell..")
                    current_route_cell = current_route_cell.previous_route_cell
                    if self.show_route_log == True: print((current_route_cell.row, current_route_cell.column))
            else:
                previous_route_cell = current_route_cell
                current_route_cell = next_route_cell
                current_route_cell.previous_route_cell = previous_route_cell
                current_route_cell.is_visited = True
                # current_route_cell.setText("a")
                if self.show_route_log == True: print((current_route_cell.row, current_route_cell.column))
                self.tunnelBetweenCurrentAndPreviousRouteCell(current_route_cell, current_route_cell.previous_route_cell)
        self.set_initial_route_cell()
        self.colorCells()

    def get_next_unvisted_cell_on_route(self, current_route_cell):
        directions = [(0, -2), (-2, 0), (0, 2), (2, 0)]
        random.shuffle(directions)
        for direction in directions:
            next_route_cell_row = current_route_cell.row + direction[0]
            next_route_cell_column = current_route_cell.column + direction[1]
            if next_route_cell_row >= 0 and next_route_cell_row < self.maze_row_count:
                if next_route_cell_column >= 0 and next_route_cell_column < self.maze_column_count:
                    next_route_cell = self.maze_map[next_route_cell_row][next_route_cell_column]
                    if self.show_route_log == True: print("Checking..", (next_route_cell.row, next_route_cell.column))
                    # print("Checking..", (next_cell_row, next_cell_column))
                    if next_route_cell.is_visited == False:
                        return next_route_cell
        return None

    def tunnelBetweenCurrentAndPreviousRouteCell(self, current_route_cell, previous_route_cell):
        current_route_cell_row = current_route_cell.row
        current_route_cell_column = current_route_cell.column
        previous_route_cell_row = previous_route_cell.row
        previous_route_cell_column = previous_route_cell.column

        tunneling_wall_cell = None
        if current_route_cell_row - previous_route_cell_row == 0:
            if current_route_cell_column > previous_route_cell_column:
                tunneling_wall_cell = self.maze_map[current_route_cell_row][previous_route_cell_column + 1]
            else:
                tunneling_wall_cell = self.maze_map[current_route_cell_row][current_route_cell_column + 1]
        else:
            if current_route_cell_row > previous_route_cell_row:
                tunneling_wall_cell = self.maze_map[previous_route_cell_row + 1][current_route_cell_column]
            else:
                tunneling_wall_cell = self.maze_map[current_route_cell_row + 1][current_route_cell_column]
        tunneling_wall_cell.is_visited = True


    def set_initial_route_cell(self):
        for i in range(2):
            possible_intial_route_cells = []
            for j in range(1, self.maze_column_count - 1):
                possible_intial_route_cells.append(self.maze_map[0][j])
            for j in range(1, self.maze_column_count - 1):
                possible_intial_route_cells.append(self.maze_map[self.maze_row_count - 1][j])
            for i in range(1, self.maze_row_count - 1):
                possible_intial_route_cells.append(self.maze_map[i][0])
            for i in range(1, self.maze_row_count - 1):
                possible_intial_route_cells.append(self.maze_map[i][self.maze_column_count - 1])
            initial_route_cell = random.choice(possible_intial_route_cells)
            initial_route_cell.is_visited = True
            initial_route_cell.is_route_initial_cell = True


    def colorCells(self):
        for i in range(self.maze_row_count):
            for j in range(self.maze_column_count):
                if self.maze_map[i][j].is_visited == True:
                    if self.maze_map[i][j].is_route_initial_cell == True:
                        #self.maze_map[i][j].setStyleSheet("background-color: red")
                        self.maze_map[i][j].setBackground(QBrush(QColor("Red")))
                    else:
                        # self.maze_map[i][j].setStyleSheet("background-color: white")
                        self.maze_map[i][j].setBackground(QBrush(QColor("White")))
                else:
                    self.maze_map[i][j].setBackground(QBrush(QColor("Black")))

                    # self.maze_map[i][j].setStyleSheet("background-color: black")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    maze = Maze(20, 20)
    app.exec()
    sys.exit()
