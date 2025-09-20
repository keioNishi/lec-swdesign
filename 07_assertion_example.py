# アサーション（assert文）を使用した条件チェックと契約プログラミングの例
def divide(a, b):
    # 事前条件：型チェック - isinstance()で型を検証
    assert isinstance(a, (int, float)), "aは数値である必要があります"
    assert isinstance(b, (int, float)), "bは数値である必要があります"
    assert b != 0, "ゼロで割ることはできません"

    result = a / b

    # 事後条件：浮動小数点演算の精度チェック - 計算の妥当性を検証
    assert abs(result * b - a) < 1e-10, "計算結果が正確ではありません"
    return result

# アサーションを使った二分探索の実装例
def binary_search(arr, target):
    # 事前条件：引数の型と配列のソート状態を検証
    assert isinstance(arr, list), "arrはリストである必要があります"
    # all()とジェネレータ式を使用してソート済み配列かを一括チェック
    assert all(arr[i] <= arr[i+1] for i in range(len(arr)-1)), \
        "配列はソート済みである必要があります"

    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1

# スクリプトが直接実行された場合のみ以下を実行
if __name__ == "__main__":
    print("=== divide関数のテスト ===")
    # try-except文でアサーションエラーをキャッチ
    try:
        result = divide(10, 2)
        print(f"10 / 2 = {result}")

        result = divide(7, 3)
        print(f"7 / 3 = {result}")

        # 意図的にアサーションエラーを発生させる（ゼロ除算）
        result = divide(5, 0)
    except AssertionError as e:
        print(f"アサーションエラー: {e}")

    print("\n=== binary_search関数のテスト ===")
    sorted_array = [1, 3, 5, 7, 9, 11, 13]

    try:
        index = binary_search(sorted_array, 7)
        print(f"7の位置: {index}")

        index = binary_search(sorted_array, 4)
        print(f"4の位置: {index}")

        # 意図的にアサーションエラーを発生させる（非ソート配列）
        unsorted_array = [3, 1, 5, 2]
        index = binary_search(unsorted_array, 3)
    except AssertionError as e:
        print(f"アサーションエラー: {e}")
