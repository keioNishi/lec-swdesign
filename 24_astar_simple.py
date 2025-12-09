"""
A*アルゴリズム - ヒューリスティック探索

このプログラムは、A*アルゴリズムの実装です。
- ヒューリスティック関数を使用して目標方向を優先的に探索
- 評価関数: f(n) = g(n) + h(n)
  - g(n): 始点からの実コスト
  - h(n): 目標までの推定コスト（ヒューリスティック）
- ダイクストラ法より効率的に特定の目標への経路を発見
- ユークリッド距離を使った地理的ヒューリスティック
"""

import heapq
import math


def astar_simple(graph, start, goal, heuristic):
    """
    A*アルゴリズムによる最短経路探索

    Args:
        graph (dict): グラフ構造 {ノード: [(隣接ノード, 重み), ...]}
        start (str): 始点ノード
        goal (str): 目標ノード
        heuristic (function): ヒューリスティック関数 h(node, goal)

    Returns:
        tuple: (最短経路のリスト, 総コスト)
    """
    # ステップ1: 初期化
    distances = {start: 0}  # 始点からの実際の距離（g値）
    previous = {}  # 経路復元用の親ノード
    unvisited = []  # 優先度キュー

    # 【ダイクストラとの違い】始点を優先度キューに追加 (f値, ノード)
    # f値 = g値 + h値
    f_value = 0 + heuristic(start, goal)
    heapq.heappush(unvisited, (f_value, start))

    print(f"探索開始: {start} → {goal}")
    print("-" * 40)

    # ステップ2: 探索ループ
    while unvisited:
        # 【ダイクストラとの違い】最小f値のノードを取り出す
        current_f, current_node = heapq.heappop(unvisited)
        current_distance = distances[current_node]  # g値を取得

        # 探索状況を表示
        h_value = heuristic(current_node, goal)
        print(f"現在のノード: {current_node}")
        print(f"  g値(実コスト): {current_distance}")
        print(f"  h値(推定コスト): {h_value}")
        print(f"  f値(総推定): {current_f}")

        # 目標に到達したら終了
        if current_node == goal:
            print(f"\n目標に到達！")
            break

        # すでに処理済みの場合はスキップ
        if current_distance > distances.get(current_node, float('inf')):
            continue

        # ステップ3: 隣接ノードの距離を更新
        for neighbor, weight in graph.get(current_node, []):
            # g値（始点からの実コスト）を計算
            distance = current_distance + weight

            # より短い経路が見つかった場合
            if distance < distances.get(neighbor, float('inf')):
                distances[neighbor] = distance
                previous[neighbor] = current_node

                # 【ダイクストラとの違い】f値を計算して優先度キューに追加
                # f値 = g値 + h値（ヒューリスティック）
                h_value = heuristic(neighbor, goal)
                f_value = distance + h_value
                heapq.heappush(unvisited, (f_value, neighbor))

                print(f"  → {neighbor}への距離を更新:")
                print(f"     g={distance}, h={h_value}, f={f_value}")

    # ステップ4: 経路を復元
    path = []
    node = goal

    # ゴールから始点まで逆順にたどる
    while node in previous:
        path.append(node)
        node = previous[node]
    path.append(start)
    path.reverse()  # 逆順にして始点→ゴールの順序にする

    return path, distances.get(goal, float('inf'))


def create_usa_network_with_coordinates():
    """
    アメリカ主要都市間の道路網を模した複雑なグラフを作成

    ノード数: 30都市
    エッジ数: 約45の接続
    重み: 都市間の距離（100km単位）
    座標: 緯度・経度を簡易化した座標（相対位置）
    """
    # 都市の座標（相対位置、実際の地理的位置を簡略化）
    coordinates = {
        'シアトル': (0, 100), 'ポートランド': (5, 95),
        'サンフランシスコ': (10, 75), 'ロサンゼルス': (15, 65),
        'サンディエゴ': (18, 60), 'ラスベガス': (22, 68),
        'フェニックス': (25, 60), 'デンバー': (40, 75),
        'ソルトレイクシティ': (30, 80), 'ボイシ': (20, 85),
        'ビリングス': (35, 92), 'ミネアポリス': (60, 90),
        'シカゴ': (70, 82), 'デトロイト': (75, 85),
        'カンザスシティ': (55, 75), 'セントルイス': (65, 75),
        'ダラス': (55, 60), 'ヒューストン': (58, 55),
        'ニューオーリンズ': (68, 55), 'アトランタ': (75, 62),
        'マイアミ': (82, 50), 'シャーロット': (80, 68),
        'ワシントンDC': (85, 75), 'フィラデルフィア': (87, 77),
        'ニューヨーク': (90, 80), 'ボストン': (92, 85),
        'ピッツバーグ': (80, 78), 'ナッシュビル': (70, 68),
        'メンフィス': (65, 65), 'オクラホマシティ': (52, 68)
    }

    # 都市間の接続と距離
    connections = {
        'シアトル': [('ポートランド', 2.8), ('ボイシ', 8.0), ('ビリングス', 11.0)],
        'ポートランド': [('シアトル', 2.8), ('サンフランシスコ', 10.5), ('ボイシ', 7.0)],
        'サンフランシスコ': [('ポートランド', 10.5), ('ロサンゼルス', 6.2), ('ラスベガス', 9.0)],
        'ロサンゼルス': [('サンフランシスコ', 6.2), ('サンディエゴ', 2.0), ('ラスベガス', 4.5), ('フェニックス', 6.0)],
        'サンディエゴ': [('ロサンゼルス', 2.0), ('フェニックス', 5.8)],
        'ラスベガス': [('サンフランシスコ', 9.0), ('ロサンゼルス', 4.5), ('ソルトレイクシティ', 6.7), ('フェニックス', 4.8)],
        'フェニックス': [('サンディエゴ', 5.8), ('ロサンゼルス', 6.0), ('ラスベガス', 4.8), ('ダラス', 16.0)],
        'ボイシ': [('シアトル', 8.0), ('ポートランド', 7.0), ('ソルトレイクシティ', 5.5), ('ビリングス', 8.5)],
        'ソルトレイクシティ': [('ボイシ', 5.5), ('ラスベガス', 6.7), ('デンバー', 8.5)],
        'ビリングス': [('シアトル', 11.0), ('ボイシ', 8.5), ('ミネアポリス', 13.5), ('デンバー', 9.0)],
        'デンバー': [('ソルトレイクシティ', 8.5), ('ビリングス', 9.0), ('カンザスシティ', 9.5), ('オクラホマシティ', 10.5)],
        'ミネアポリス': [('ビリングス', 13.5), ('シカゴ', 6.5), ('カンザスシティ', 7.5)],
        'シカゴ': [('ミネアポリス', 6.5), ('デトロイト', 4.5), ('セントルイス', 4.8), ('ピッツバーグ', 7.5)],
        'デトロイト': [('シカゴ', 4.5), ('ピッツバーグ', 4.5), ('ニューヨーク', 10.0)],
        'カンザスシティ': [('ミネアポリス', 7.5), ('デンバー', 9.5), ('セントルイス', 4.0), ('オクラホマシティ', 5.5)],
        'セントルイス': [('シカゴ', 4.8), ('カンザスシティ', 4.0), ('メンフィス', 4.5), ('ナッシュビル', 5.0)],
        'オクラホマシティ': [('デンバー', 10.5), ('カンザスシティ', 5.5), ('ダラス', 3.5)],
        'ダラス': [('オクラホマシティ', 3.5), ('フェニックス', 16.0), ('ヒューストン', 4.0), ('メンフィス', 7.5)],
        'ヒューストン': [('ダラス', 4.0), ('ニューオーリンズ', 5.5)],
        'ニューオーリンズ': [('ヒューストン', 5.5), ('アトランタ', 7.5), ('メンフィス', 6.5)],
        'メンフィス': [('セントルイス', 4.5), ('ダラス', 7.5), ('ニューオーリンズ', 6.5), ('ナッシュビル', 3.5), ('アトランタ', 6.3)],
        'ナッシュビル': [('セントルイス', 5.0), ('メンフィス', 3.5), ('アトランタ', 4.0), ('シャーロット', 6.5)],
        'アトランタ': [('ニューオーリンズ', 7.5), ('メンフィス', 6.3), ('ナッシュビル', 4.0), ('シャーロット', 4.0), ('マイアミ', 10.5)],
        'マイアミ': [('アトランタ', 10.5)],
        'シャーロット': [('ナッシュビル', 6.5), ('アトランタ', 4.0), ('ワシントンDC', 6.5)],
        'ワシントンDC': [('シャーロット', 6.5), ('ピッツバーグ', 3.8), ('フィラデルフィア', 2.3)],
        'フィラデルフィア': [('ワシントンDC', 2.3), ('ニューヨーク', 1.5), ('ピッツバーグ', 4.8)],
        'ニューヨーク': [('フィラデルフィア', 1.5), ('デトロイト', 10.0), ('ボストン', 3.5)],
        'ボストン': [('ニューヨーク', 3.5)],
        'ピッツバーグ': [('シカゴ', 7.5), ('デトロイト', 4.5), ('ワシントンDC', 3.8), ('フィラデルフィア', 4.8)]
    }

    return connections, coordinates


def euclidean_heuristic(node, goal, coordinates):
    """
    ユークリッド距離に基づくヒューリスティック関数

    地理的な直線距離を推定コストとして使用。
    許容的ヒューリスティック（実際のコスト以下）を保証。

    Args:
        node (str): 現在のノード
        goal (str): 目標ノード
        coordinates (dict): 各都市の座標

    Returns:
        float: 推定コスト（直線距離）
    """
    if node not in coordinates or goal not in coordinates:
        return 0.0

    x1, y1 = coordinates[node]
    x2, y2 = coordinates[goal]

    # ユークリッド距離を計算（スケールを調整）
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance * 0.15  # 距離単位を調整


def main():
    """
    メイン実行関数：複雑な道路網でA*アルゴリズムを実行
    """
    # アメリカ道路網グラフと座標を作成
    graph, coordinates = create_usa_network_with_coordinates()

    # グラフの統計情報を表示
    print("\n" + "=" * 60)
    print("グラフ構造: アメリカ主要都市道路網")
    print("=" * 60)
    node_count = len(graph)
    edge_count = sum(len(edges) for edges in graph.values()) // 2
    print(f"ノード数: {node_count} 都市")
    print(f"エッジ数: {edge_count} 接続")
    print(f"平均次数: {edge_count * 2 / node_count:.2f}")

    # 一部の接続を表示
    print("\n主要な接続の例:")
    sample_cities = ['ニューヨーク', 'ロサンゼルス', 'シカゴ', 'ヒューストン']
    for city in sample_cities:
        if city in graph:
            connections = ", ".join([f"{n}({w*100:.0f}km)" for n, w in graph[city]])
            print(f"  {city} → {connections}")

    print("\n" + "=" * 60)
    start_city = 'ニューヨーク'
    goal_city = 'ロサンゼルス'
    print(f"探索開始: {start_city} → {goal_city}")

    # 直線距離を表示
    straight_distance = euclidean_heuristic(start_city, goal_city, coordinates) * 100
    print(f"直線距離（推定）: {straight_distance:.0f} km")
    print("=" * 60 + "\n")

    # ヒューリスティック関数を定義（座標情報を含む）
    def heuristic(node, goal):
        return euclidean_heuristic(node, goal, coordinates)

    # A*アルゴリズムを実行
    path, cost = astar_simple(graph, start_city, goal_city, heuristic)

    # 結果を表示
    print("\n" + "=" * 60)
    print("結果")
    print("=" * 60)
    print(f"最短経路: {' → '.join(path)}")
    print(f"総距離: {cost * 100:.0f} km （コスト値: {cost:.1f}）")
    print(f"経由都市数: {len(path)} 都市")

    # 経路の詳細を表示
    print("\n経路の詳細:")
    for i in range(len(path) - 1):
        from_node = path[i]
        to_node = path[i + 1]
        weight = next(w for n, w in graph[from_node] if n == to_node)
        print(f"  {from_node} → {to_node}: {weight * 100:.0f} km")

    print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    main()
