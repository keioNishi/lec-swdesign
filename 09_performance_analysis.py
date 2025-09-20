import time
from functools import wraps

# デコレータ：関数の実行時間を測定する高階関数
def measure_time(func):
    # @wraps(func)は元の関数の情報（名前、ドキュメントなど）を保持
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__}: {end_time - start_time:.4f}秒")
        return result
    return wrapper

# デコレータを適用：関数実行時に自動的に時間測定が行われる
@measure_time
def fibonacci_slow(n):
    """再帰的実装：指数時間計算量 O(2^n) - 非効率"""
    if n <= 1:
        return n
    return fibonacci_slow(n-1) + fibonacci_slow(n-2)

@measure_time
def fibonacci_fast(n):
    """反復的実装：線形時間計算量 O(n) - 効率的"""
    if n <= 1:
        return n
    a, b = 0, 1
    # アンパック代入を使用した効率的な値の交換
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

# スクリプトが直接実行された場合のみ以下を実行
if __name__ == "__main__":
    print("=== フィボナッチ数列の性能比較 ===")

    print("高速な実装:")
    result_fast = fibonacci_fast(30)
    print(f"結果: {result_fast}")

    print("\n遅い実装:")
    result_slow = fibonacci_slow(30)
    print(f"結果: {result_slow}")

    print("\n両方とも同じ結果ですが、実行時間が大きく異なります。")
