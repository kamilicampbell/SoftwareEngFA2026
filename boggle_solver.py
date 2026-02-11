class Boggle:
    def __init__(self, grid, dictionary):
        self.grid = grid
        self.dictionary = dictionary
        self.solutions = []
    

    def getSolution(self):
        if not self.grid or not self.grid[0]:
            return []

        rows = len(self.grid)
        cols = len(self.grid[0])

        board = [[cell.lower() for cell in row] for row in self.grid]
        words = set(word.lower() for word in self.dictionary)

        prefixes = set()
        for w in words:
            for i in range(1, len(w) + 1):
                prefixes.add(w[:i])

        found = set()

        def dfs(r, c, path, visited):
            if r < 0 or r >= rows or c < 0 or c >= cols:
                return
            if (r, c) in visited:
                return

            val = board[r][c]
            new_path = path + val

            if new_path not in prefixes:
                return

            if len(new_path) >= 3 and new_path in words:
                found.add(new_path)

            visited.add((r, c))

            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr != 0 or dc != 0:
                        dfs(r + dr, c + dc, new_path, visited)

            visited.remove((r, c))

        for r in range(rows):
            for c in range(cols):
                dfs(r, c, "", set())

        result = []
        for w in found:
            for orig in self.dictionary:
                if orig.lower() == w:
                    result.append(orig)

        return sorted(set(result))

def main():
    grid = [["T", "W", "Y", "R"], ["E", "N", "P", "H"],["G", "Z", "Qu", "R"],["O", "N", "T", "A"]]
    dictionary = ["art", "ego", "gent", "get", "net", "new", "newt", "prat", "pry", "qua", "quart", "quartz", "rat", "tar", "tarp", "ten", "went", "wet", "arty", "rhr", "not", "quar"]
    
    mygame = Boggle(grid, dictionary)
    print(mygame.getSolution())

if __name__ == "__main__":
    main()