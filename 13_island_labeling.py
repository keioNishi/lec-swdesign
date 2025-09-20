import random

# 島ラベリングアルゴリズム：連結された陸地を同じ番号でラベル付け
def label_islands(grid):
    def dfs(r, c, label):
        # 境界チェックと陸地判定
        if r < 0 or r >= 8 or c < 0 or c >= 8 or grid[r][c] != 1:
            return
        grid[r][c] = label
        # 四方向への再帰的探索
        for dr, dc in [(0,1), (1,0), (0,-1), (-1,0)]:
            dfs(r+dr, c+dc, label)

    label = 2  # ラベル開始番号（0=海、1=未処理陸地）
    for i in range(8):
        for j in range(8):
            if grid[i][j] == 1:  # 未処理の陸地発見
                dfs(i, j, label)
                label += 1
    return label - 2  # 島の総数

# ランダムな海域マップを生成（陸地の出現確率25%）
def create_sea_map():
    return [[random.choice([0,0,0,1]) for _ in range(8)] for _ in range(8)]

if __name__ == "__main__":
    print("=== 島ラベリング ===")
    sea = create_sea_map()
    print("元の海域 (1=陸地, 0=海):")
    for row in sea:
        print(''.join(map(str, row)))

    islands = label_islands(sea)
    print(f"\n島ラベリング結果 (島数: {islands}):")
    for row in sea:
        print(''.join([str(x) if x else '～' for x in row]))

    print("\n別の例:")
    sea2 = create_sea_map()
    print("元の海域 (1=陸地, 0=海):")
    for row in sea2:
        print(''.join(map(str, row)))

    islands2 = label_islands(sea2)
    print(f"\n島ラベリング結果 (島数: {islands2}):")
    for row in sea2:
        print(''.join([str(x) if x else '～' for x in row]))
