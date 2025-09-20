# ハッシュテーブル（辞書型データ構造）の実装
class HashTable:
    def __init__(self, size=10):
        self.size = size
        # チェイン法：各バケットにリストを用意して衝突を処理
        self.table = [[] for _ in range(size)]

    def _hash(self, key):
        # ハッシュ関数：キーをテーブルのインデックスに変換
        return hash(key) % self.size

    def put(self, key, value):
        # キーと値のペアを挿入
        index = self._hash(key)
        bucket = self.table[index]
        # 既存のキーがあれば値を更新
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        # 新しいキーの場合はバケットに追加
        bucket.append((key, value))

    def get(self, key):
        # キーに対応する値を取得
        index = self._hash(key)
        bucket = self.table[index]
        for k, v in bucket:
            if k == key:
                return v
        raise KeyError(key)

if __name__ == "__main__":
    print("=== 自作ハッシュテーブルの例 ===")
    hash_table = HashTable(5)
    hash_table.put("apple", 100)
    hash_table.put("banana", 200)
    hash_table.put("orange", 150)
    print(f"apple: {hash_table.get('apple')}")
    print(f"banana: {hash_table.get('banana')}")

    print("\n=== Python内蔵辞書の例 ===")
    hash_dict = {}
    hash_dict["apple"] = 100
    hash_dict["banana"] = 200
    hash_dict[42] = "数値キー"
    print(f"apple: {hash_dict['apple']}")
    print(f"'apple'のハッシュ値: {hash('apple')}")

    print("\n=== ハッシュ値の例 ===")
    print(f"hash('hello'): {hash('hello')}")
    print(f"hash(42): {hash(42)}")
    print(f"hash(3.14): {hash(3.14)}")
    print(f"hash((1, 2, 3)): {hash((1, 2, 3))}")
    print(f"hash('test'): {hash('test')}")
    print(f"hash('test'): {hash('test')}")  # 同じ値が出力される

    # ハッシュ化できないオブジェクトの例
    try:
        print(hash([1, 2, 3]))  # リストは不可
    except TypeError as e:
        print(f"エラー: {e}")

    print("\n=== set（集合）の例 ===")
    hash_set = {1, 2, 3, 4, 5}
    print(f"2 in hash_set: {2 in hash_set}")  # O(1)で高速検索

    # 重複除去の例
    data = [1, 2, 2, 3, 3, 3, 4]
    unique_data = list(set(data))
    print(f"重複除去: {unique_data}")
