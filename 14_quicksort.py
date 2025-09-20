# クイックソート：分割統治法による効率的ソートアルゴリズム
def quicksort(arr):
    # ベースケース：要素が1個以下なら既にソート済み
    if len(arr) <= 1:
        return arr

    # ピボット（基準値）を配列の中央から選択
    pivot = arr[len(arr) // 2]
    # リスト内包表記で配列を3つに分割
    left = [x for x in arr if x < pivot]     # ピボットより小さい要素
    middle = [x for x in arr if x == pivot]  # ピボットと等しい要素
    right = [x for x in arr if x > pivot]    # ピボットより大きい要素

    # 再帰的に左右をソートし、結果を連結
    return quicksort(left) + middle + quicksort(right)

# スクリプトが直接実行された場合のみ以下を実行
if __name__ == "__main__":
    arr = [64, 34, 25, 12, 22, 11, 90]

    # Pythonの組み込みsorted()関数（新しいリストを返す）
    sorted_arr = sorted(arr)
    print("sorted()関数:")
    print(f"ソート結果: {sorted_arr}")
    print(f"元の配列: {arr}")  # 元の配列は変更されない

    # リストのsort()メソッド（リスト自体を変更）
    arr2 = [64, 34, 25, 12, 22, 11, 90]
    arr2.sort()
    print(f"\nlist.sort()メソッド:")
    print(f"ソート結果: {arr2}")

    # reverse=Trueで逆順ソート
    arr3 = [64, 34, 25, 12, 22, 11, 90]
    arr3.sort(reverse=True)
    print(f"逆順ソート: {arr3}")

    # 自作クイックソートの実行
    arr4 = [64, 34, 25, 12, 22, 11, 90]
    quicksort_result = quicksort(arr4)
    print(f"\nクイックソート結果: {quicksort_result}")
    print(f"元の配列: {arr4}")  # 元の配列は変更されない
