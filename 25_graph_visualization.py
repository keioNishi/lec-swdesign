"""
グラフ探索アルゴリズムの可視化

このプログラムは、ダイクストラ法とA*アルゴリズムを可視化します。
- ネットワークグラフの可視化
- アルゴリズム比較の可視化
- グリッド迷路での経路探索の可視化
- 画像ファイルとして結果を出力
"""

import heapq
import math
from typing import Dict, List, Tuple, Optional
import matplotlib.pyplot as plt
import networkx as nx


class Graph:
    """グラフデータ構造を管理するクラス"""

    def __init__(self):
        self.edges: Dict[str, List[Tuple[str, float]]] = {}
        self.positions: Dict[str, Tuple[float, float]] = {}

    def add_node(self, node: str):
        """ノードを追加"""
        if node not in self.edges:
            self.edges[node] = []

    def add_edge(self, node1: str, node2: str, weight: float):
        """双方向エッジを追加（無向グラフ）"""
        self.add_node(node1)
        self.add_node(node2)
        self.edges[node1].append((node2, weight))
        self.edges[node2].append((node1, weight))

    def set_position(self, node: str, x: float, y: float):
        """ノードの位置を設定（可視化用）"""
        self.positions[node] = (x, y)

    def get_neighbors(self, node: str) -> List[Tuple[str, float]]:
        """隣接ノードのリストを取得"""
        return self.edges.get(node, [])

    def heuristic(self, node1: str, node2: str) -> float:
        """ユークリッド距離に基づくヒューリスティック関数"""
        if node1 not in self.positions or node2 not in self.positions:
            return 0.0
        x1, y1 = self.positions[node1]
        x2, y2 = self.positions[node2]
        return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)


def dijkstra(graph: Graph, start: str, goal: str) -> Tuple[Optional[List[str]], float, int]:
    """
    ダイクストラ法による最短経路探索

    Returns:
        tuple: (経路, コスト, 探索ノード数)
    """
    distances = {start: 0}
    # すべてのノードの距離を初期化
    for node in graph.edges:
        if node != start:
            distances[node] = float('infinity')

    previous_nodes: Dict[str, Optional[str]] = {node: None for node in graph.edges}
    priority_queue = [(0, start)]
    explored_count = 0

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        explored_count += 1

        if current_distance > distances[current_node]:
            continue

        if current_node == goal:
            break

        for neighbor, weight in graph.get_neighbors(current_node):
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))

    # 経路を復元
    path: List[str] = []
    current = goal
    if distances[goal] == float('infinity'):
        return None, float('infinity'), explored_count

    while current is not None:
        path.insert(0, current)
        current = previous_nodes[current]

    return path, distances[goal], explored_count


def a_star(graph: Graph, start: str, goal: str) -> Tuple[Optional[List[str]], float, int]:
    """
    A*アルゴリズムによる最短経路探索

    Returns:
        tuple: (経路, コスト, 探索ノード数)
    """
    g_score = {node: float('infinity') for node in graph.edges}
    g_score[start] = 0

    f_score = {node: float('infinity') for node in graph.edges}
    f_score[start] = graph.heuristic(start, goal)

    previous_nodes: Dict[str, Optional[str]] = {node: None for node in graph.edges}
    priority_queue = [(f_score[start], start)]
    explored_count = 0

    while priority_queue:
        current_f_score, current_node = heapq.heappop(priority_queue)
        explored_count += 1

        if current_node == goal:
            path: List[str] = []
            current = goal
            while current is not None:
                path.insert(0, current)
                current = previous_nodes[current]
            return path, g_score[goal], explored_count

        for neighbor, weight in graph.get_neighbors(current_node):
            tentative_g_score = g_score[current_node] + weight
            if tentative_g_score < g_score[neighbor]:
                previous_nodes[neighbor] = current_node
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + graph.heuristic(neighbor, goal)
                heapq.heappush(priority_queue, (f_score[neighbor], neighbor))

    return None, float('infinity'), explored_count


def create_sample_graph() -> Graph:
    """
    より複雑なサンプルグラフを作成

    20ノード、35エッジの中規模ネットワーク
    複数の経路と迂回路を持つリアルな構造
    """
    graph = Graph()

    # ノードの位置を設定（5x4のグリッド状に配置）
    positions = {
        'A': (0, 0), 'B': (1, 0), 'C': (2, 0), 'D': (3, 0), 'E': (4, 0),
        'F': (0, 1), 'G': (1, 1), 'H': (2, 1), 'I': (3, 1), 'J': (4, 1),
        'K': (0, 2), 'L': (1, 2), 'M': (2, 2), 'N': (3, 2), 'O': (4, 2),
        'P': (0, 3), 'Q': (1, 3), 'R': (2, 3), 'S': (3, 3), 'T': (4, 3)
    }

    for node, (x, y) in positions.items():
        graph.set_position(node, x, y)

    # エッジを追加（複数の経路を持つ複雑な構造）
    edges = [
        # 横方向の接続
        ('A', 'B', 1.2), ('B', 'C', 1.5), ('C', 'D', 1.3), ('D', 'E', 1.8),
        ('F', 'G', 1.4), ('G', 'H', 1.1), ('H', 'I', 1.6), ('I', 'J', 1.3),
        ('K', 'L', 1.3), ('L', 'M', 1.5), ('M', 'N', 1.4), ('N', 'O', 1.7),
        ('P', 'Q', 1.6), ('Q', 'R', 1.2), ('R', 'S', 1.5), ('S', 'T', 1.4),
        # 縦方向の接続
        ('A', 'F', 1.5), ('F', 'K', 1.4), ('K', 'P', 1.6),
        ('B', 'G', 1.3), ('G', 'L', 1.7), ('L', 'Q', 1.3),
        ('C', 'H', 1.6), ('H', 'M', 1.2), ('M', 'R', 1.5),
        ('D', 'I', 1.4), ('I', 'N', 1.5), ('N', 'S', 1.3),
        ('E', 'J', 1.7), ('J', 'O', 1.6), ('O', 'T', 1.4),
        # 斜め方向の接続（ショートカット）
        ('A', 'G', 2.0), ('B', 'H', 1.8), ('C', 'I', 2.1),
        ('F', 'L', 1.9), ('G', 'M', 2.0), ('H', 'N', 1.7),
        ('K', 'Q', 2.2), ('L', 'R', 1.8), ('M', 'S', 2.0)
    ]

    for u, v, w in edges:
        graph.add_edge(u, v, w)

    return graph


def compare_search_visualization(graph: Graph, start: str, goal: str):
    """ダイクストラ法とA*アルゴリズムの比較可視化"""
    # 両方のアルゴリズムを実行
    path_dijkstra, cost_d, explored_d = dijkstra(graph, start, goal)
    path_astar, cost_a, explored_a = a_star(graph, start, goal)

    # 2つのサブプロットを作成
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))

    # NetworkXグラフに変換
    G = nx.Graph()
    for node in graph.edges.keys():
        G.add_node(node)

    for node, neighbors in graph.edges.items():
        for neighbor, weight in neighbors:
            if not G.has_edge(node, neighbor):
                G.add_edge(node, neighbor, weight=weight)

    pos = graph.positions

    # エッジラベルを作成
    edge_labels = {}
    for node, neighbors in graph.edges.items():
        for neighbor, weight in neighbors:
            if (node, neighbor) not in edge_labels and (neighbor, node) not in edge_labels:
                edge_labels[(node, neighbor)] = f"{weight:.1f}"

    # ダイクストラの結果を描画
    plt.sca(ax1)
    nx.draw_networkx_nodes(G, pos, node_color='lightblue',
                          node_size=1000, alpha=0.9, ax=ax1)
    nx.draw_networkx_edges(G, pos, width=2, alpha=0.5,
                          edge_color='gray', ax=ax1)

    if path_dijkstra:
        path_edges = [(path_dijkstra[i], path_dijkstra[i+1])
                     for i in range(len(path_dijkstra)-1)]
        nx.draw_networkx_edges(G, pos, edgelist=path_edges,
                              width=4, edge_color='blue', alpha=0.8, ax=ax1)
        nx.draw_networkx_nodes(G, pos, nodelist=[path_dijkstra[0]],
                              node_color='green', node_size=1200, alpha=0.9, ax=ax1)
        nx.draw_networkx_nodes(G, pos, nodelist=[path_dijkstra[-1]],
                              node_color='orange', node_size=1200, alpha=0.9, ax=ax1)

    nx.draw_networkx_labels(G, pos, font_size=14, font_weight='bold', ax=ax1)
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=9, ax=ax1)
    ax1.set_title(f'Dijkstra\'s algorithm\nNumber of search nodes: {explored_d}, Cost: {cost_d:.2f}',
                 fontsize=14, fontweight='bold', pad=20)
    ax1.axis('off')

    # A*の結果を描画
    plt.sca(ax2)
    nx.draw_networkx_nodes(G, pos, node_color='lightblue',
                          node_size=1000, alpha=0.9, ax=ax2)
    nx.draw_networkx_edges(G, pos, width=2, alpha=0.5,
                          edge_color='gray', ax=ax2)

    if path_astar:
        path_edges = [(path_astar[i], path_astar[i+1])
                     for i in range(len(path_astar)-1)]
        nx.draw_networkx_edges(G, pos, edgelist=path_edges,
                              width=4, edge_color='red', alpha=0.8, ax=ax2)
        nx.draw_networkx_nodes(G, pos, nodelist=[path_astar[0]],
                              node_color='green', node_size=1200, alpha=0.9, ax=ax2)
        nx.draw_networkx_nodes(G, pos, nodelist=[path_astar[-1]],
                              node_color='orange', node_size=1200, alpha=0.9, ax=ax2)

    nx.draw_networkx_labels(G, pos, font_size=14, font_weight='bold', ax=ax2)
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=9, ax=ax2)
    ax2.set_title(f'A* Algorithm\nNumber of search nodes: {explored_a}, Cost: {cost_a:.2f}',
                 fontsize=14, fontweight='bold', pad=20)
    ax2.axis('off')

    # 効率改善を表示
    if path_dijkstra and path_astar:
        efficiency = (1 - explored_a / explored_d) * 100 if explored_d > 0 else 0
        fig.suptitle(f'Comparison of Search Algorithms: {start} → {goal}\n' +
                    f'A* improvement: {efficiency:.1f}% reduction',
                    fontsize=16, fontweight='bold')

    plt.tight_layout()
    return plt


def create_grid_graph(width: int, height: int, obstacles: List[Tuple[int, int]] = None) -> Graph:
    """グリッドグラフを作成（迷路探索用）"""
    graph = Graph()
    obstacles = obstacles or []

    # すべてのノードの位置を設定
    for y in range(height):
        for x in range(width):
            if (x, y) not in obstacles:
                node_name = f"{x},{y}"
                graph.set_position(node_name, x, y)

    # エッジを追加（上下左右の移動）
    for y in range(height):
        for x in range(width):
            if (x, y) in obstacles:
                continue

            current = f"{x},{y}"

            # 右
            if x + 1 < width and (x + 1, y) not in obstacles:
                neighbor = f"{x+1},{y}"
                graph.add_edge(current, neighbor, 1.0)

            # 下
            if y + 1 < height and (x, y + 1) not in obstacles:
                neighbor = f"{x},{y+1}"
                graph.add_edge(current, neighbor, 1.0)

    return graph


def visualize_grid_search(graph: Graph, width: int, height: int,
                         obstacles: List[Tuple[int, int]],
                         path: List[str], title: str):
    """グリッド迷路の探索結果を可視化"""
    plt.figure(figsize=(10, 10))

    # グリッドを描画
    for y in range(height):
        for x in range(width):
            if (x, y) in obstacles:
                plt.fill([x, x+1, x+1, x], [y, y, y+1, y+1], 'black', alpha=0.7)
            else:
                plt.fill([x, x+1, x+1, x], [y, y, y+1, y+1], 'white',
                        edgecolor='gray', linewidth=0.5)

    # 経路を描画
    if path:
        path_coords = []
        for node in path:
            x, y = map(int, node.split(','))
            path_coords.append((x + 0.5, y + 0.5))

        xs, ys = zip(*path_coords)
        plt.plot(xs, ys, 'r-', linewidth=3, alpha=0.7, label='Route')
        plt.plot(xs, ys, 'ro', markersize=8)
        plt.plot(xs[0], ys[0], 'go', markersize=15, label='Start')
        plt.plot(xs[-1], ys[-1], 'o', color='orange', markersize=15, label='Goal')

    plt.xlim(0, width)
    plt.ylim(0, height)
    plt.gca().set_aspect('equal')
    plt.gca().invert_yaxis()
    plt.title(title, fontsize=16, fontweight='bold', pad=20)
    plt.legend(loc='upper right', fontsize=12)
    plt.grid(False)

    return plt


def main():
    """メイン実行関数"""
    print("=" * 60)
    print("グラフ探索アルゴリズムの可視化")
    print("=" * 60)
    print("\n視覚化を生成中...")

    # matplotlib日本語フォント設定（必要に応じて）
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False

    # 1. 複雑なサンプルグラフの比較視覚化
    print("\n[1] アルゴリズム比較の可視化を生成中...")
    print("    - 20ノード、35エッジの複雑なネットワーク")
    graph = create_sample_graph()
    plt1 = compare_search_visualization(graph, 'A', 'T')
    plt1.savefig('algorithm_comparison.png', dpi=150, bbox_inches='tight')
    print("[OK] algorithm_comparison.png を保存しました")
    plt.close()

    # 2. より大きなグリッド迷路の例
    print("\n[2] グリッド迷路の例を生成中...")
    print("    - 15x15の大規模グリッド")
    # より複雑な障害物パターンを作成
    obstacles = []
    # 垂直の壁
    for i in range(1, 8):
        obstacles.append((3, i))
    for i in range(5, 12):
        obstacles.append((7, i))
    for i in range(2, 9):
        obstacles.append((11, i))
    # 水平の壁
    for i in range(5, 11):
        obstacles.append((i, 10))
    for i in range(8, 14):
        obstacles.append((i, 5))

    grid_graph = create_grid_graph(15, 15, obstacles)
    path_grid, _, explored = a_star(grid_graph, '0,0', '14,14')
    plt2 = visualize_grid_search(grid_graph, 15, 15, obstacles, path_grid,
                                 f'A* search (Explored: {explored} nodes)')
    plt2.savefig('maze_solution.png', dpi=150, bbox_inches='tight')
    print("[OK] maze_solution.png を保存しました")
    plt.close()

    print("\n" + "=" * 60)
    print("全ての視覚化が完了しました!")
    print("=" * 60)
    print("\n生成されたファイル:")
    print("  - algorithm_comparison.png (20ノードの複雑なネットワーク比較)")
    print("  - maze_solution.png (15x15グリッド迷路の解)")
    print("\n各アルゴリズムの特性:")
    print("  - ダイクストラ法: 全方位探索、最適解保証")
    print("  - A*アルゴリズム: ヒューリスティック使用、効率的探索")
    print()


if __name__ == "__main__":
    main()
