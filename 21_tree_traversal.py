from collections import deque

# 二分木のノードを表現するクラス
class TreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

# 二分木のさまざまな走査アルゴリズムを実装
class BinaryTree:
    def __init__(self):
        self.root = None

    def inorder_traversal(self, node, result):
        # 中順走査（左・ルート・右）
        if node:
            self.inorder_traversal(node.left, result)
            result.append(node.data)
            self.inorder_traversal(node.right, result)

    def preorder_traversal(self, node, result):
        # 前順走査（ルート・左・右）
        if node:
            result.append(node.data)
            self.preorder_traversal(node.left, result)
            self.preorder_traversal(node.right, result)

    def postorder_traversal(self, node, result):
        # 後順走査（左・右・ルート）
        if node:
            self.postorder_traversal(node.left, result)
            self.postorder_traversal(node.right, result)
            result.append(node.data)

    def level_order_traversal(self):
        # レベル順走査（幅優先探索）
        if not self.root:
            return []
        result = []
        queue = deque([self.root])
        while queue:
            node = queue.popleft()
            result.append(node.data)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return result

# 深さ優先探索（DFS）の再帰実装
def dfs_recursive(node, visited=None):
    if visited is None:
        visited = []
    if node is None:
        return visited

    visited.append(node.data)
    print(f"訪問: {node.data}")
    dfs_recursive(node.left, visited)
    dfs_recursive(node.right, visited)
    return visited

if __name__ == "__main__":
    # サンプルの二分木を構築
    #       50
    #      /  \
    #     30   70
    #    / \   / \
    #   20 40 60 80
    root = TreeNode(50)
    root.left = TreeNode(30)
    root.right = TreeNode(70)
    root.left.left = TreeNode(20)
    root.left.right = TreeNode(40)
    root.right.left = TreeNode(60)
    root.right.right = TreeNode(80)

    tree = BinaryTree()
    tree.root = root

    print("=== 木の走査の例 ===")

    # 各種走査アルゴリズムで木を走査
    inorder_result = []
    tree.inorder_traversal(tree.root, inorder_result)
    print(f"中順走査（Inorder）: {inorder_result}")

    preorder_result = []
    tree.preorder_traversal(tree.root, preorder_result)
    print(f"前順走査（Preorder）: {preorder_result}")

    postorder_result = []
    tree.postorder_traversal(tree.root, postorder_result)
    print(f"後順走査（Postorder）: {postorder_result}")

    level_order_result = tree.level_order_traversal()
    print(f"幅優先探索（Level Order）: {level_order_result}")

    print("\n=== DFS（深さ優先探索）の例 ===")
    # 別の木でDFSをデモンストレーション
    #     A
    #    / \
    #   B   C
    #  /   / \
    # D   E   F
    dfs_root = TreeNode('A')
    dfs_root.left = TreeNode('B')
    dfs_root.right = TreeNode('C')
    dfs_root.left.left = TreeNode('D')
    dfs_root.right.left = TreeNode('E')
    dfs_root.right.right = TreeNode('F')

    result = dfs_recursive(dfs_root)
    print(f"訪問順序: {result}")

    print("\n=== DFS vs BFS 比較表 ===")
    print("特徴        | DFS           | BFS")
    print("-" * 40)
    print("探索順序    | 深さ優先      | 幅優先（レベル順）")
    print("データ構造  | スタック(LIFO)| キュー(FIFO)")
    print("最短パス    | 保証なし      | 保証あり（重みなし）")
    print("メモリ使用  | O(深さ)       | O(幅)")
    print("用途        | 全探索、パズル| 最短距離、レベル順処理")
