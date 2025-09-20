# 静的メソッドの例：インスタンスと無関係なユーティリティ関数群
class MathUtils:
    @staticmethod  # デコレータ：selfパラメータ不要、クラス名で直接呼び出し可能
    def factorial(n):
        if n <= 1:
            return 1
        return n * MathUtils.factorial(n - 1)  # 再帰呼び出し

    @staticmethod
    def gcd(a, b):  # 最大公約数を求めるユークリッドの互除法
        while b:  # bが0でない間繰り返し
            a, b = b, a % b  # タプルで同時代入
        return a

    @staticmethod
    def is_prime(n):
        if n < 2:
            return False
        # 平方根までの約数をチェックする効率的なアルゴリズム
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:  # 約数が見つかったら素数ではない
                return False
        return True

if __name__ == "__main__":
    # 静的メソッドの正しい使い方：クラス名から直接呼び出し
    print(f"5の階乗: {MathUtils.factorial(5)}")
    print(f"12と18の最大公約数: {MathUtils.gcd(12, 18)}")
    print(f"17は素数か: {MathUtils.is_prime(17)}")
    print(f"15は素数か: {MathUtils.is_prime(15)}")

    # インスタンス経由でも呼び出し可能だが非推奨
    utils = MathUtils()
    result = utils.factorial(4)
    print(f"インスタンス経由での4の階乗: {result}")
