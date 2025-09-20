import hashlib

# 暗号学的ハッシュ関数のデモンストレーション
def crypto_hash_demo():
    text = "Hello, World!"

    # 各種ハッシュアルゴリズムでハッシュ値を計算
    md5_hash = hashlib.md5(text.encode()).hexdigest()
    print(f"MD5: {md5_hash}")

    sha256_hash = hashlib.sha256(text.encode()).hexdigest()
    print(f"SHA-256: {sha256_hash}")

    sha1_hash = hashlib.sha1(text.encode()).hexdigest()
    print(f"SHA-1: {sha1_hash}")

if __name__ == "__main__":
    print("=== 暗号学的ハッシュの例 ===")
    crypto_hash_demo()

    print("\n=== ハッシュ機能の比較表 ===")
    print("機能      | 用途                  | 時間計算量")
    print("-" * 50)
    print("hash()    | 基本ハッシュ値計算    | O(1)")
    print("dict      | キー・値ペア管理      | O(1)平均")
    print("set       | 重複なし集合          | O(1)平均")
    print("hashlib   | 暗号学的ハッシュ      | データ依存")

    print("\n=== データのハッシュ値計算例 ===")
    test_data = ["test1", "test2", "test1"]  # test1が重複
    sha256_hashes = {}

    for data in test_data:
        hash_value = hashlib.sha256(data.encode()).hexdigest()
        sha256_hashes[data] = hash_value
        print(f"{data}: {hash_value}")

    # 同じデータは同じハッシュ値を持つことを確認
    print(f"\ntest1のハッシュ値が同じ: {sha256_hashes['test1'] == hashlib.sha256('test1'.encode()).hexdigest()}")

    print("\n=== 異なるアルゴリズムの比較 ===")
    test_string = "アルゴリズムテスト"
    algorithms = ['md5', 'sha1', 'sha256', 'sha512']

    for alg in algorithms:
        hash_obj = hashlib.new(alg)
        hash_obj.update(test_string.encode('utf-8'))
        print(f"{alg.upper()}: {hash_obj.hexdigest()}")
