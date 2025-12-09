import random

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
    maze[1][1] = ' '                # すぐ右は必ず通路
    maze[size - 2][size - 1] = 'G'  # 右側にゴール
    maze[size - 2][size - 2] = ' '  # すぐ左は必ず通路

    return maze

def print_maze(maze):
    for row in maze:
        print(''.join(row))

if __name__ == "__main__":
    print("=== 21x21 迷路 ===")
    m = generate_maze(21)
    print_maze(m)
