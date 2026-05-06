from .randomGen import *
from .readJSONFile import *

class Boggle:
    def __init__(self, grid, dictionary):
        self.grid = grid
        self.dictionary = dictionary
        self.solutions = []
        self.setGrid(grid)
        self.setDictionary(dictionary)

    def setGrid(self, grid):
        if not grid or not isinstance(grid, list):
            self.grid = []
            return
        self.grid = grid

    def setDictionary(self, dictionary):
        if not dictionary or not isinstance(dictionary, list):
            self.dictionary = []
            return
        self.dictionary = dictionary

    def getSolution(self):
        if not self.grid or not self.dictionary:
            return []
        found = []
        for word in self.dictionary:
            if len(word) < 3:
                continue
            if self.exists(word):
                found.append(word)
        self.solutions = found
        return found

    def exists(self, word):
        rows = len(self.grid)
        cols = len(self.grid[0])
        word = word.upper()
        for r in range(rows):
            for c in range(cols):
                visited = [[False] * cols for _ in range(rows)]
                if self.dfs(r, c, word, 0, visited):
                    return True
        return False

    def dfs(self, r, c, word, index, visited):
        rows = len(self.grid)
        cols = len(self.grid[0])
        if index == len(word):
            return True
        if not (0 <= r < rows and 0 <= c < cols):
            return False
        if visited[r][c]:
            return False
        tile = self.grid[r][c].upper()
        if not word.startswith(tile, index):
            return False
        visited[r][c] = True
        next_index = index + len(tile)
        if next_index == len(word):
            return True
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr != 0 or dc != 0:
                    if self.dfs(r + dr, c + dc, word, next_index, visited):
                        return True
        visited[r][c] = False
        return False
