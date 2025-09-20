# 二分探索木のノードを表現するクラス
class TreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None   # 左の子ノード
        self.right = None  # 右の子ノード

# 二分探索木（BST）の実装
class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, data):
        # データを木に挿入
        if not self.root:
            self.root = TreeNode(data)
        else:
            self._insert_recursive(self.root, data)

    def _insert_recursive(self, node, data):
        # 再帰的にデータを挿入（BSTの性質を維持）
        if data < node.data:
            if node.left is None:
                node.left = TreeNode(data)
            else:
                self._insert_recursive(node.left, data)
        elif data > node.data:
            if node.right is None:
                node.right = TreeNode(data)
            else:
                self._insert_recursive(node.right, data)

    def search(self, data):
        # 指定されたデータを探索
        return self._search_recursive(self.root, data)

    def _search_recursive(self, node, data):
        # 再帰的にデータを探索
        if not node or node.data == data:
            return node is not None
        if data < node.data:
            return self._search_recursive(node.left, data)
        return self._search_recursive(node.right, data)

    def inorder_traversal(self):
        # 中順走査（左・ルート・右）で昇順ソートされた結果を取得
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node, result):
        # 中順走査の再帰実装
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.data)
            self._inorder_recursive(node.right, result)

    def preorder_traversal(self):
        # 前順走査（ルート・左・右）で結果を取得
        result = []
        self._preorder_recursive(self.root, result)
        return result

    def _preorder_recursive(self, node, result):
        # 前順走査の再帰実装
        if node:
            result.append(node.data)
            self._preorder_recursive(node.left, result)
            self._preorder_recursive(node.right, result)

if __name__ == "__main__":
    print("=== 二分探索木のテスト ===")
    bst = BinarySearchTree()
    values = [50, 30, 70, 20, 40, 60, 80]
    print(f"挿入する値: {values}")

    # データを二分探索木に挿入
    for value in values:
        bst.insert(value)

    # 探索テスト
    print(f"40を検索: {bst.search(40)}")
    print(f"25を検索: {bst.search(25)}")

    # 木の走査結果を表示
    print(f"\n中順走査（昇順ソート）: {bst.inorder_traversal()}")
    print(f"前順走査: {bst.preorder_traversal()}")

    print("\n=== 二分探索木の特徴 ===")
    print("利点:")
    print("- 探索：O(log n)（平均）")
    print("- 挿入：O(log n)（平均）")
    print("- 削除：O(log n)（平均）")
    print("- ソート済みデータの出力が容易")

    print("\n欠点:")
    print("- 最悪時：O(n)（一直線になる場合）")
    print("- バランス維持が困難")

    print("\n=== 最悪ケース（一直線）の例 ===")
    worst_bst = BinarySearchTree()
    worst_values = [1, 2, 3, 4, 5]  # 昇順に挿入

    for value in worst_values:
        worst_bst.insert(value)

    print(f"昇順挿入: {worst_values}")
    print(f"中順走査結果: {worst_bst.inorder_traversal()}")
    print("この場合、木が一直線になり効率が悪くなります")
