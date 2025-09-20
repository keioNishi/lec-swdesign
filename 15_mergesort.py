# mergesort 関数では arr を基に処理の流れを整理します。
def mergesort(arr):
    # len(arr) <= 1 を評価し、満たす場合の処理に分岐します。
    if len(arr) <= 1:
        # 求めた arr を呼び出し元へ返します。
        return arr

    # midを 式 len(arr) // 2 として設定し、後続の処理で利用できるようにします。
    mid = len(arr) // 2
    # leftを整えるために mergesort を利用して処理を進めます。
    left = mergesort(arr[:mid])
    # rightを整えるために mergesort を利用して処理を進めます。
    right = mergesort(arr[mid:])

    # 求めた merge を利用して処理を進めます を呼び出し元へ返します。
    return merge(left, right)

# マージをまとめる merge 関数では left, right を基に処理の流れを整理します。
def merge(left, right):
    # resultを リスト として設定し、後続の処理で利用できるようにします。
    result = []
    # (i, j)を (0, 0) として設定し、後続の処理で利用できるようにします。
    i, j = 0, 0

    # 条件 i < len(left) and j < len(right) が成り立つあいだ繰り返し処理します。
    while i < len(left) and j < len(right):
        # left[i] <= right[j] を評価し、満たす場合の処理に分岐します。
        if left[i] <= right[j]:
            # リストの末尾に要素を追加します。
            result.append(left[i])
            i += 1
        else:
            # リストの末尾に要素を追加します。
            result.append(right[j])
            j += 1

    # 複数要素をまとめて末尾に追加します。
    result.extend(left[i:])
    # 複数要素をまとめて末尾に追加します。
    result.extend(right[j:])
    # 求めた result を呼び出し元へ返します。
    return result

# スクリプトが直接実行された場合のみ以下を実行
if __name__ == "__main__":
    arr = [64, 34, 25, 12, 22, 11, 90]

    # Pythonの標準ソート関数とメソッド
    sorted_arr = sorted(arr)  # 新しいリストを返す
    arr_copy = arr.copy()
    arr_copy.sort()  # リスト自体を変更

    print("PythonのソートはTimsort（マージソート改良版）です")
    print(f"元の配列: {arr}")
    print(f"sorted()結果: {sorted_arr}")
    print(f"sort()結果: {arr_copy}")

    # 自作マージソートの実行
    mergesort_result = mergesort(arr)
    print(f"マージソート結果: {mergesort_result}")

    # 大きなデータでのテスト
    import random
    large_arr = [random.randint(1, 1000) for _ in range(100)]
    print(f"\n大きな配列のソート結果（最初の10個）: {mergesort(large_arr)[:10]}")
