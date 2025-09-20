import random

# 迷路生成アルゴリズム（再帰的分割法）
def generate_maze(size=9):
    # 2次元リスト内包表記で迷路の初期化（全て壁）
    maze = [['#'] * size for _ in range(size)]

    # ネストした関数：再帰的分割により通路を作成
    def carve(x, y, w, h):
        # ベースケース：分割できない小さな領域
        if w < 3 or h < 3:
            return
        # 幅が高さより大きい場合：縦に分割
        if w > h:
            # ランダムな位置に壁と通路を配置
            wx, dy = x + random.randrange(1, w-1, 2), y + random.randrange(0, h, 2)
            for i in range(y, y+h):
                maze[i][wx] = '#'
            maze[dy][wx] = ' '  # 通路を作成
            # 左右の領域を再帰的に分割
            carve(x, y, wx-x, h)
            carve(wx+1, y, x+w-wx-1, h)
        else:
            # 高さが幅以上の場合：横に分割
            wy, dx = y + random.randrange(1, h-1, 2), x + random.randrange(0, w, 2)
            for i in range(x, x+w):
                maze[wy][i] = '#'
            maze[wy][dx] = ' '  # 通路を作成
            # 上下の領域を再帰的に分割
            carve(x, y, w, wy-y)
            carve(x, wy+1, w, y+h-wy-1)

    # 奇数座標を通路として初期化
    for i in range(1, size, 2):
        for j in range(1, size, 2):
            maze[i][j] = ' '

    # 再帰的分割を開始
    carve(1, 1, size-2, size-2)
    # スタートとゴールを設定
    maze[1][0], maze[size-2][size-1] = 'S', 'G'
    return maze

# 迷路を視覚的に表示
def print_maze(maze):
    for row in maze:
        # join()メソッドで文字列連結
        print(''.join(row))

# スクリプトが直接実行された場合のみ以下を実行
if __name__ == "__main__":
    print("=== 迷路生成 ===")
    maze = generate_maze(9)
    print_maze(maze)

    print("\n別の迷路:")
    maze2 = generate_maze(11)
    print_maze(maze2)
