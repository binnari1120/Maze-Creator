import numpy
import random
import copy
import os

class MazeCell:
    def __init__(self, row, column, is_visited = False, previous_cell = None, is_wall = True):
        self.row = row
        self.column = column
        self.is_visited = is_visited
        self.previous_cell = previous_cell
        self.is_wall = is_wall

        self.possible_directions = [(-1, 0, "↑"), (0, 1, "→"), (1, 0, "↓"), (0, -1, "←")]
        self.symbol = ""

class MazeRoute:
    def __init__(self):
        self.number_of_rows_in_route = 3
        self.number_of_columns_in_route = 3

        self.init_maze_route_cells()
        self.create_route()

    def init_maze_route_cells(self):
        self.map = []
        for row in range(self.number_of_rows_in_route):
            for column in range(self.number_of_columns_in_route):
                self.map.append(MazeCell(row, column, False, None, False))
        self.map = numpy.array(self.map).reshape(self.number_of_rows_in_route, self.number_of_columns_in_route)

    def create_route(self):
        # starting_cell_row = random.randint(0, self.number_of_rows_in_route - 1)
        # starting_cell_column = random.randint(0, self.number_of_columns_in_route - 1)
        starting_cell_row = 0
        starting_cell_column = 0

        starting_cell = self.map[starting_cell_row][starting_cell_column]
        starting_cell.is_visited = True
        starting_cell.symbol = "↓"
        current_cell = copy.copy(starting_cell)
        print(current_cell.row, ", ", current_cell.column)

        while self.are_all_cells_visited() == False:
            random.shuffle(current_cell.possible_directions)
            for i in range(len(current_cell.possible_directions)):
                next_cell_row = current_cell.row + current_cell.possible_directions[i][0]
                next_cell_column = current_cell.column + current_cell.possible_directions[i][1]
                if next_cell_row >= self.number_of_rows_in_route or next_cell_column >= self.number_of_columns_in_route:
                    continue
                next_cell = self.map[next_cell_row][next_cell_column]
                if next_cell.is_visited == False:
                    next_cell.previous_cell = copy.copy(current_cell)
                    next_cell.is_visited = True
                    current_cell = copy.copy(next_cell)
                    current_cell.symbol = current_cell.possible_directions[i][2]
                    print(current_cell.row, ", ", current_cell.column)
                    break
                elif next_cell.is_visited == True:
                    if i == len(current_cell.possible_directions) - 1:
                        next_cell = copy.copy(current_cell.previous_cell)
                    continue

    def are_all_cells_visited(self):
        for row in range(self.number_of_rows_in_route):
            for column in range(self.number_of_columns_in_route):
                cell = self.map[row][column]
                if cell.is_visited == False:
                    return False
        return True


    def draw_maze_route_map(self):
        map = ""
        for i in range(self.number_of_rows_in_route):
            for j in range(self.number_of_columns_in_route):
                map = map + self.map[i][j].symbol
            map = map + "\n"

        full_file_name = os.path.join(os.path.dirname(__file__), "route_map.txt")
        with open(full_file_name, "w") as file:
            file.write(map)
        print(map)



class Maze:
    def __init__(self):
        self.maze_route = MazeRouteMap()
        self.number_of_rows_in_maze = self.maze_route_map.number_of_rows_in_route * 2 + 1
        self.number_of_columns_in_maze = self.maze_route_map.number_of_columns_in_route * 2 + 1

        self.init_maze_cells()
        self.incorporate_maze_route_cells_in_maze_cells()

    def init_maze_cells(self):
        self.maze_map = []
        for row in range(self.number_of_rows_in_maze):
            for column in range(self.number_of_columns_in_maze):
                self.maze_map.append(MazeCell(row, column, False, None, True))
        self.maze_map = numpy.array(self.maze_map).reshape(self.number_of_rows_in_maze, self.number_of_columns_in_maze)


    def incorporate_maze_route_cells_in_maze_cells(self):
        for i in range(self.maze_route.number_of_rows_in_route):
            for j in range(self.maze_route.number_of_columns_in_route):
                self.maze_map[i * 2 - 1][j * 2 - 1] = self.maze_route.map[i][j]

    def tunnel_walls(self):
        pass

    def draw_maze_map(self):
        map = ""

        for i in range(self.number_of_rows_in_maze):
            for j in range(self.number_of_columns_in_maze):
                if i == 0 and j == 1:
                    map = map + "↓"
                    continue
                if self.maze_map[i][j].is_wall == True:
                    map = map + "■"
                else:
                    map = map + "□"
            map = map + "\n"


        full_file_name = os.path.join(os.path.dirname(__file__), "map.txt")
        with open(full_file_name, "w") as file:
            file.write(map)
        print(map)


if __name__ == "__main__":
    maze_route_map = MazeRoute()
    maze_route_map.draw_maze_route_map()

    # maze_map = Maze()
    # maze_map.draw_maze_map()
