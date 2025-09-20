# 連結リストの各ノードを表現するクラス
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

# 連結リスト（線形データ構造）の実装
class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        # リストの末尾にデータを追加
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        # 末尾まで辿って新しいノードを追加
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def prepend(self, data):
        # リストの先頭にデータを追加
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def delete(self, data):
        # 指定されたデータを持つ最初のノードを削除
        if not self.head:
            return
        # 先頭ノードが削除対象の場合
        if self.head.data == data:
            self.head = self.head.next
            return
        # 削除対象のノードを探して削除
        current = self.head
        while current.next and current.next.data != data:
            current = current.next
        if current.next:
            current.next = current.next.next

    def display(self):
        # リストの全要素をリスト形式で返す
        elements = []
        current = self.head
        while current:
            elements.append(current.data)
            current = current.next
        return elements

if __name__ == "__main__":
    print("=== 連結リストの基本操作 ===")
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    ll.prepend(0)
    print(f"リスト: {ll.display()}")

    ll.delete(2)
    print(f"2を削除後: {ll.display()}")

    print("\n=== 配列と連結リストの比較 ===")
    print("操作             | 配列      | 連結リスト")
    print("-" * 45)
    print("要素アクセス     | O(1)      | O(n)")
    print("挿入・削除（先頭）| O(n)      | O(1)")
    print("挿入・削除（末尾）| O(1)      | O(n)")
    print("挿入・削除（中央）| O(n)      | O(1)※")
    print("メモリ使用量     | 連続領域  | 分散、ポインタ分多い")
    print("キャッシュ効率   | 良い      | 悪い")

    print("\n=== リストの使い分け ===")
    print("連結リストが適している場面:")
    print("- 頻繁な挿入・削除")
    print("- サイズが不明")
    print("- スタック・キューの実装")

    print("\n連結リストを避けるべき場面:")
    print("- ランダムアクセスが必要")
    print("- メモリ効率を重視")
    print("- キャッシュ性能が重要")

    print("\n=== パフォーマンス比較 ===")
    import time

    # 連結リストの先頭挿入テスト
    ll_test = LinkedList()
    start_time = time.time()
    for i in range(1000):
        ll_test.prepend(i)
    ll_time = time.time() - start_time

    # Pythonリストの先頭挿入テスト
    py_list = []
    start_time = time.time()
    for i in range(1000):
        py_list.insert(0, i)
    py_time = time.time() - start_time

    print(f"連結リスト先頭挿入1000回: {ll_time:.6f}秒")
    print(f"Pythonリスト先頭挿入1000回: {py_time:.6f}秒")
    print(f"連結リストが{py_time/ll_time:.1f}倍高速" if ll_time > 0 else "連結リストが高速")
