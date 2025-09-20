# ヒープソート：最大ヒープを利用した選択ソート
def heapsort(arr):
    # ヒープ化：親ノードが子ノードより大きくなるよう調整
    def heapify(arr, n, i):
        largest = i
        left, right = 2*i + 1, 2*i + 2

        # 左の子と比較
        if left < n and arr[left] > arr[largest]:
            largest = left
        # 右の子と比較
        if right < n and arr[right] > arr[largest]:
            largest = right

        # 必要なら親と子を交換し、再帰的にヒープ化
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(arr, n, largest)

    n = len(arr)

    # 最大ヒープを構築（末尾の親から開始）
    for i in range(n//2 - 1, -1, -1):
        heapify(arr, n, i)

    # 要素を一つずつ取り出してソート
    for i in range(n-1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]  # 最大値を末尾に移動
        heapify(arr, i, 0)  # 残り要素でヒープ再構築

    return arr

if __name__ == "__main__":
    data = [64, 34, 25, 12, 22, 11, 90]
    print(f"元配列: {data}")
    print(f"ソート後: {heapsort(data.copy())}")

    test_data = [64, 34, 25, 12, 22, 11, 90, 88, 76, 50, 42, 18, 6, 82]
    print(f"\nテストデータ: {test_data}")

    heap_result = heapsort(test_data.copy())
    print(f"ヒープソート: {heap_result}")

    builtin_result = sorted(test_data)
    print(f"内蔵ソート: {builtin_result}")

    print(f"結果が一致: {heap_result == builtin_result}")

    print("\n=== アルゴリズム比較表 ===")
    print("アルゴリズム     | 用途           | 特徴")
    print("-" * 45)
    print("クイックソート   | 一般的な用途   | 平均的に最も高速")
    print("マージソート     | 安定性が必要   | 最悪時間が保証される")
    print("ヒープソート     | メモリ制約がある| インプレース")
    print("Python内蔵      | 実用的な用途   | 最適化済み（Timsort）")
