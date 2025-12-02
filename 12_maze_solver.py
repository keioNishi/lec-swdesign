import random

# =========================
# 迷路生成（再帰的バックトラック）
# =========================
def generate_maze(size=21):
    """
    再帰的バックトラック（DFS）で perfect maze を生成する。
    - '#' : 壁
    - ' ' : 通路
    - 'S' : スタート
    - 'G' : ゴール
    """
    if size % 2 == 0:
        raise ValueError("迷路サイズは奇数にしてください (例: 21)")

    # 最初は全部壁
    maze = [['#'] * size for _ in range(size)]

    # 再帰的に通路を掘る
    def carve(y, x):
        maze[y][x] = ' '  # 現在位置を通路に
        # 2マス先へ進む候補（上下左右）をランダム順に試す
        directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
        random.shuffle(directions)

        for dy, dx in directions:
            ny, nx = y + dy, x + dx
            # 2マス先が迷路の内側かつまだ壁なら掘り進める
            if 1 <= ny < size - 1 and 1 <= nx < size - 1 and maze[ny][nx] == '#':
                # 間の1マスも通路にする
                maze[y + dy // 2][x + dx // 2] = ' '
                carve(ny, nx)  # 再帰

    # (1,1) から掘り始める
    carve(1, 1)

    # スタートとゴールを外周に開ける
    maze[1][0] = 'S'                # 左側にスタート
    maze[1][1] = ' '                # すぐ右は通路
    maze[size - 2][size - 1] = 'G'  # 右側にゴール
    maze[size - 2][size - 2] = ' '  # すぐ左は通路

    return maze

# =========================
# 迷路解法（再帰 DFS）
# =========================
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
        # （スタートも一時的に '.' になるが、後で復元する）
        maze[r][c] = '.'
        # 四方向への再帰的探索 - 1 つでも成功すれば True
        if any(dfs(r+dr, c+dc) for dr, dc in [(0,1), (1,0), (0,-1), (-1,0)]):
            return True
        # バックトラック：探索失敗時は元に戻す
        maze[r][c] = ' '
        return False

    # スタート地点を見つけて DFS 開始
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == 'S':
                if dfs(i, j):
                    maze[i][j] = 'S'  # スタート位置を復元
                    return True
                else:
                    return False
    return False

# =========================
# ユーティリティ
# =========================
def print_maze(maze):
    for row in maze:
        print(''.join(row))

# =========================
# 実行例
# =========================
if __name__ == "__main__":
    size = 21

    print("=== 生成された迷路 ===")
    maze = generate_maze(size)
    print_maze(maze)

    # 解く用にコピー（生成した迷路を残したい場合）
    maze_solved = [row[:] for row in maze]

    if solve_maze(maze_solved):
        print("\n=== 解かれた迷路 ('.' が解経路) ===")
        print_maze(maze_solved)
    else:
        print("\n解経路が見つかりませんでした。")

