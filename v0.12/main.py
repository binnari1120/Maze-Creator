from PyQt5.QtWidgets import *
from PyQt5.Qt import *
import numpy
import sys
import random

class MazeCell(QPushButton):
    def __init__(self, str, row, column):
        super().__init__(str)
        self.row = row
        self.column = column

        self.is_visited = False
        self.previous_cell = None
        self.next_cell = None


class MazeRoute(QMainWindow):
    def __init__(self):
        super().__init__()
        self.route_row_count = 3
        self.route_column_count = 3
        self.route_map = [None for i in range(self.route_row_count * self.route_column_count)]
        self.route_map = numpy.array(self.route_map).reshape(self.route_row_count, self.route_column_count)
        for i in range(self.route_row_count):
            for j in range(self.route_column_count):
                self.route_map[i][j] = MazeCell("", i, j)

        #self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        table_layout = QHBoxLayout()
        table = QTableWidget()
        table.setRowCount(self.route_row_count)
        table.setColumnCount(self.route_column_count)
        table.horizontalHeader().hide()
        table.verticalHeader().hide()
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table_layout.addWidget(table)
        for i in range(self.route_row_count):
            for j in range(self.route_column_count):
                table.setCellWidget(i, j, self.route_map[i][j])
        main_layout.addLayout(table_layout)

        btns_layout = QHBoxLayout()
        create_route_btn = QPushButton("Create route")
        create_route_btn.clicked.connect(self.is_create_route_btn_clicked)
        btns_layout.addWidget(create_route_btn)
        main_layout.addLayout(btns_layout)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(main_layout)
        self.show()

    def is_create_route_btn_clicked(self):
        self.create_route()

    def create_route(self):
        rand_row = random.randint(0, self.route_row_count-1)
        rand_column = random.randint(0, self.route_column_count-1)
        initial_cell = self.route_map[rand_row][rand_column]
        current_cell = initial_cell
        current_cell.is_visited = True
        # current_cell.setText("√")

        print("Starting from", (current_cell.row, current_cell.column))
        while True:
            next_cell = self.get_next_bounded_cell_unvisited(current_cell)
            if next_cell == None:
                if current_cell == initial_cell:
                    print("No cells to move.. now at inital point.. exiting the loop..")
                    break
                else:
                    print("No cells to move.. back to the previous cell..")
                    current_cell = current_cell.previous_cell
                    print((current_cell.row, current_cell.column))
            else:
                previous_cell = current_cell
                previous_cell.next_cell = next_cell
                current_cell = next_cell
                # current_cell.setText("√")

                current_cell.previous_cell = previous_cell
                current_cell.is_visited = True
                print((current_cell.row, current_cell.column))


    def get_next_bounded_cell_unvisited(self, current_cell):
        directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]
        next_cell_row = 0
        next_cell_column = 0
        for direction in directions:
            next_cell_row = current_cell.row + direction[0]
            next_cell_column = current_cell.column + direction[1]
            if next_cell_row >= 0 and next_cell_row < self.route_row_count:
                if next_cell_column >= 0 and next_cell_column < self.route_column_count:
                    next_cell = self.route_map[next_cell_row][next_cell_column]
                    print("Checking ", (next_cell.row, next_cell.column))
                    if next_cell.is_visited == False:
                        return next_cell
        return None


class Maze(QMainWindow):
    def __init__(self, route):
        super().__init__()
        self.route = route

        self.maze_map_row_count = route.route_row_count * 2 + 1
        self.maze_map_column_count = route.route_column_count * 2 + 1
        self.maze_map = [None for i in range(self.maze_map_row_count * self.maze_map_column_count)]
        self.maze_map = numpy.array(self.maze_map).reshape(self.maze_map_row_count, self.maze_map_column_count)
        for i in range(self.maze_map_row_count):
            for j in range(self.maze_map_column_count):
                item = QTableWidgetItem()
                item.setText("■")
                self.maze_map[i][j] = item
                # if i % 2 != 0 and j % 2 != 0:
                #     self.maze_map[i][j] = MazeCell("＠", i, j)
                # else:
                #     self.maze_map[i][j] = MazeCell("■", i, j)

        self.init_ui()

    def init_ui(self):
        self.setGeometry(300, 300, 700, 700)
        self.setWindowTitle("Maze Creator")

        main_layout = QVBoxLayout()

        table_layout = QHBoxLayout()
        table = QTableWidget()
        table.setRowCount(self.maze_map_row_count)
        table.setColumnCount(self.maze_map_column_count)
        table.horizontalHeader().hide()
        table.verticalHeader().hide()
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table_layout.addWidget(table)
        for i in range(self.maze_map_row_count):
            for j in range(self.maze_map_column_count):
                table.setItem(i, j, self.maze_map[i][j])


        main_layout.addLayout(table_layout)

        btns_layout = QHBoxLayout()
        create_route_btn = QPushButton("Create route")
        create_route_btn.clicked.connect(self.is_create_route_btn_clicked)
        btns_layout.addWidget(create_route_btn)
        main_layout.addLayout(btns_layout)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        self.show()


    def is_create_route_btn_clicked(self):
        self.route.is_create_route_btn_clicked()
        self.insert_route_map_into_maze_map()


    def insert_route_map_into_maze_map(self):
        for i in range(self.route.route_row_count):
            for j in range(self.route.route_column_count):
                self.maze_map[2 * i + 1][2 * j + 1].setText("")
                current_route_cell = self.route.route_map[i][j]
                current_route_cell_row = current_route_cell.row
                current_route_cell_column = current_route_cell.column

                previous_route_cell = current_route_cell.previous_cell
                print(previous_route_cell)
                if previous_route_cell != None:
                    previous_route_cell_row = previous_route_cell.row
                    previous_route_cell_column = previous_route_cell.column
                    print("Current: ", (current_route_cell_row, current_route_cell_column), " / Previous: ", (previous_route_cell_row, previous_route_cell_column))

                    distance_row = abs(current_route_cell_row - previous_route_cell_row)
                    distance_column = abs(current_route_cell_column - previous_route_cell_column)

                    wall_row = 0
                    wall_column = 0
                    if distance_row == 0:
                        wall_row = current_route_cell_row
                    else:
                        if current_route_cell_row > previous_route_cell_row:
                            wall_row = 2 * current_route_cell_row
                        else:
                            wall_row = 2 * previous_route_cell_row

                    if distance_column == 0:
                        wall_column = current_route_cell_column
                    else:
                        if current_route_cell_column > previous_route_cell_column:
                            wall_column = 2 * current_route_cell_column
                        else:
                            wall_column = 2 * previous_route_cell_column
                    self.maze_map[wall_row][wall_column].setText("T")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    route = MazeRoute()
    maze = Maze(route)
    app.exec()
    sys.exit()
