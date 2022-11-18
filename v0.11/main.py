import random
import numpy
import os
import copy


class MazeCell:
    def __init__(self, row, column, is_visited, previous_cell, is_wall):
        self.row = row
        self.column = column
        self.is_visited = is_visited
        self.previous_cell = previous_cell
        self.is_wall = is_wall


class MazeRoute:
    def __init__(self):
        self.route_row_count = 3
        self.route_column_count = 3
        self.init_route_map()
        self.explore()

    def init_route_map(self):
        self.map = []
        for i in range(self.route_row_count):
            for j in range(self.route_column_count):
                self.map.append(MazeCell(i, j, False, None, False))
        self.map = numpy.array(self.map).reshape(self.route_row_count, self.route_column_count)

    def explore(self):
        entry_pos = (0, 0)
        print("Entry pos: ", entry_pos)
        self.map[entry_pos[0]][entry_pos[1]].is_visited = True

        current_cell = self.map[entry_pos[0]][entry_pos[1]]

        while self.are_all_cells_visited() == False:

            possible_directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
            random.shuffle(possible_directions)
            does_next_cell_exist = False

            for direction in possible_directions:
                next_pos = (current_cell.row + direction[0], current_cell.column + direction[1])
                if next_pos[0] < 0 or next_pos[0] == self.route_row_count:
                    continue
                if next_pos[1] < 0 or next_pos[1] == self.route_column_count:
                    continue
                next_cell = self.map[next_pos[0]][next_pos[1]]
                if next_cell.is_visited == True:
                    continue

                if next_cell.is_visited == False:
                    # print("Current pos: ", (current_cell.row, current_cell.column, current_cell.is_visited), " Next pos: ", (next_cell.row, next_cell.column, next_cell.is_visited))
                    print("Current pos: ", (current_cell.row, current_cell.column))
                    previous_cell = current_cell
                    current_cell = next_cell
                    # current_cell = copy.copy(next_cell)
                    current_cell.is_visited = True
                    current_cell.previous_cell = previous_cell
                    does_next_cell_exist = True
                    break
            if does_next_cell_exist == False:
                # current_cell = copy.copy(current_cell.previous_cell)
                current_cell = copy.copy(current_cell.previous_cell)
                print("All visited.. moving to previous cell..")


    def are_all_cells_visited(self):
        for i in range(self.route_row_count):
            for j in range(self.route_column_count):
                if self.map[i][j].is_visited == False:
                    return False
        return True



if __name__ == "__main__":
    route = MazeRoute()
