import random

# 迷路生成（前のファイルと同じアルゴリズム）
def generate_maze(size=9):
    maze = [['#'] * size for _ in range(size)]

    def carve(x, y, w, h):
        if w < 3 or h < 3:
            return
        if w > h:
            wx, dy = x + random.randrange(1, w-1, 2), y + random.randrange(0, h, 2)
            for i in range(y, y+h):
                maze[i][wx] = '#'
            maze[dy][wx] = ' '
            carve(x, y, wx-x, h)
            carve(wx+1, y, x+w-wx-1, h)
        else:
            wy, dx = y + random.randrange(1, h-1, 2), x + random.randrange(0, w, 2)
            for i in range(x, x+w):
                maze[wy][i] = '#'
            maze[wy][dx] = ' '
            carve(x, y, w, wy-y)
            carve(x, wy+1, w, y+h-wy-1)

    for i in range(1, size, 2):
        for j in range(1, size, 2):
            maze[i][j] = ' '

    carve(1, 1, size-2, size-2)
    maze[1][0], maze[size-2][size-1] = 'S', 'G'
    return maze

# 深度優先探索（DFS）による迷路解法
def solve_maze(maze):
    def dfs(r, c):
        # 境界チェックと訪問済み・壁チェック
        if (r < 0 or r >= len(maze) or c < 0 or c >= len(maze[0]) or
            maze[r][c] in ['#', '.']):
            return False
        # ゴール到達判定
        if maze[r][c] == 'G':
            return True
        # 現在位置を訪問済みとしてマーク
        maze[r][c] = '.'
        # 四方向への再帰的探索 - any()で一つでも成功すればTrue
        if any(dfs(r+dr, c+dc) for dr, dc in [(0,1), (1,0), (0,-1), (-1,0)]):
            return True
        # バックトラック：探索失敗時は元に戻す
        maze[r][c] = ' '
        return False

    # スタート地点を見つけてDFS開始
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == 'S' and dfs(i, j):
                maze[i][j] = 'S'  # スタート位置を復元
                return True
    return False

def print_maze(maze):
    for row in maze:
        print(''.join(row))

# スクリプトが直接実行された場合のみ以下を実行
if __name__ == "__main__":
    print("=== 迷路生成と解答 ===")
    maze = generate_maze(9)
    print("生成された迷路:")
    print_maze(maze)

    print("\n解答:")
    solve_maze(maze)  # '.'で解答経路をマーク
    print_maze(maze)
