# 再帰の基本例：階乗計算
def factorial(n):
    # ベースケース：再帰の終了条件
    if n <= 1:
        return 1
    # 再帰的ケース：自分自身を呼び出し
    return n * factorial(n - 1)

# 非効率な再帰例：フィボナッチ数列（重複計算が多い）
def fibonacci(n):
    if n <= 1:
        return n
    # 同じ値を重複計算するため非効率（指数時間）
    return fibonacci(n - 1) + fibonacci(n - 2)

# メモ化技法：計算結果をキャッシュして効率化
def fibonacci_memo(n, memo={}):
    # キャッシュから既計算値を取得
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    # 計算結果をmemo辞書に保存（動的プログラミング）
    memo[n] = fibonacci_memo(n-1, memo) + fibonacci_memo(n-2, memo)
    return memo[n]

# スクリプトが直接実行された場合のみ以下を実行
if __name__ == "__main__":
    print("=== 階乗の計算 ===")
    for i in range(1, 8):
        print(f"{i}! = {factorial(i)}")

    print("\n=== フィボナッチ数列 ===")
    print("通常の再帰:")
    for i in range(10):
        print(f"fib({i}) = {fibonacci(i)}")

    print("\nメモ化版:")
    memo = {}
    for i in range(10):
        print(f"fib_memo({i}) = {fibonacci_memo(i, memo)}")

    print("\n大きな数での比較:")
    # メモ化により大きな数も高速計算可能
    print(f"fib_memo(35) = {fibonacci_memo(35)}")
