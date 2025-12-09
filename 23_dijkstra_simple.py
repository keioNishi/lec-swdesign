"""
ダイクストラ法 - 優先度キュー使用版

このプログラムは、ヒープ（優先度キュー）を使用した効率的なダイクストラ法の実装です。
- ヒープを使用して最小距離のノードを高速に取得
- 計算量: O((V+E)log V) （Vはノード数、Eはエッジ数）
- 大規模グラフでも高速に動作
"""

import heapq


def dijkstra_simple(graph, start, goal):
    """
    優先度キューを使用したダイクストラ法による最短経路探索

    Args:
        graph (dict): グラフ構造 {ノード: [(隣接ノード, 重み), ...]}
        start (str): 始点ノード
        goal (str): 目標ノード

    Returns:
        tuple: (最短経路のリスト, 総コスト)
    """
    # ステップ1: 初期化
    distances = {start: 0}  # 始点からの距離（それ以外は辞書に存在しない=無限大扱い）
    previous = {}  # 経路復元用の親ノード
    unvisited = []  # 優先度キュー（ヒープ）

    # 始点を優先度キューに追加 (距離, ノード) のタプル形式
    heapq.heappush(unvisited, (0, start))

    print(f"探索開始: {start} → {goal}")
    print("-" * 40)

    # ステップ2: 探索ループ
    while unvisited:
        # 最小距離のノードを取り出す（O(log V)の操作）
        current_distance, current_node = heapq.heappop(unvisited)

        print(f"現在のノード: {current_node} (距離: {current_distance})")

        # 目標に到達したら終了
        if current_node == goal:
            print(f"\n目標に到達！")
            break

        # すでに処理済みの場合はスキップ
        # （同じノードが複数回キューに入ることがあるため）
        if current_distance > distances.get(current_node, float('inf')):
            continue

        # ステップ3: 隣接ノードの距離を更新
        for neighbor, weight in graph.get(current_node, []):
            # 現在のノードを経由した場合の距離を計算
            distance = current_distance + weight

            # より短い経路が見つかった場合
            if distance < distances.get(neighbor, float('inf')):
                distances[neighbor] = distance
                previous[neighbor] = current_node
                # 新しい距離でヒープに追加
                heapq.heappush(unvisited, (distance, neighbor))
                print(f"  → {neighbor}への距離を更新: {distance}")

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


def create_europe_network():
    """
    ヨーロッパ主要都市間の鉄道網を模した複雑なグラフを作成

    ノード数: 25都市
    エッジ数: 約50の接続
    重み: 都市間の移動時間（時間単位）
    """
    # ヨーロッパの主要都市間の鉄道移動時間（時間）を基にしたグラフ
    graph = {
        'ロンドン': [('パリ', 2.5), ('ブリュッセル', 2.0), ('アムステルダム', 4.0)],
        'パリ': [('ロンドン', 2.5), ('ブリュッセル', 1.5), ('リヨン', 2.0), ('フランクフルト', 4.0), ('バルセロナ', 6.5)],
        'ブリュッセル': [('ロンドン', 2.0), ('パリ', 1.5), ('アムステルダム', 2.0), ('ケルン', 2.0)],
        'アムステルダム': [('ロンドン', 4.0), ('ブリュッセル', 2.0), ('ケルン', 3.0), ('ベルリン', 6.0), ('コペンハーゲン', 8.0)],
        'ケルン': [('ブリュッセル', 2.0), ('アムステルダム', 3.0), ('フランクフルト', 1.5), ('ミュンヘン', 4.5)],
        'フランクフルト': [('パリ', 4.0), ('ケルン', 1.5), ('ミュンヘン', 3.5), ('プラハ', 6.0), ('チューリッヒ', 4.0)],
        'ミュンヘン': [('ケルン', 4.5), ('フランクフルト', 3.5), ('チューリッヒ', 4.5), ('ウィーン', 4.0), ('プラハ', 5.5)],
        'ベルリン': [('アムステルダム', 6.0), ('プラハ', 4.5), ('ワルシャワ', 5.5), ('コペンハーゲン', 7.0)],
        'コペンハーゲン': [('アムステルダム', 8.0), ('ベルリン', 7.0), ('ストックホルム', 5.0), ('オスロ', 8.0)],
        'ストックホルム': [('コペンハーゲン', 5.0), ('オスロ', 6.0)],
        'オスロ': [('コペンハーゲン', 8.0), ('ストックホルム', 6.0)],
        'ワルシャワ': [('ベルリン', 5.5), ('プラハ', 7.0), ('ウィーン', 7.0)],
        'プラハ': [('フランクフルト', 6.0), ('ミュンヘン', 5.5), ('ベルリン', 4.5), ('ワルシャワ', 7.0), ('ウィーン', 4.0), ('ブダペスト', 7.0)],
        'ウィーン': [('ミュンヘン', 4.0), ('ワルシャワ', 7.0), ('プラハ', 4.0), ('ブダペスト', 2.5), ('ザグレブ', 6.0)],
        'ブダペスト': [('プラハ', 7.0), ('ウィーン', 2.5), ('ザグレブ', 5.0), ('ブカレスト', 14.0)],
        'ザグレブ': [('ウィーン', 6.0), ('ブダペスト', 5.0), ('ミラノ', 7.0)],
        'ブカレスト': [('ブダペスト', 14.0), ('ソフィア', 7.0), ('イスタンブール', 15.0)],
        'ソフィア': [('ブカレスト', 7.0), ('イスタンブール', 9.0), ('アテネ', 12.0)],
        'イスタンブール': [('ブカレスト', 15.0), ('ソフィア', 9.0), ('アテネ', 13.0)],
        'アテネ': [('ソフィア', 12.0), ('イスタンブール', 13.0)],
        'チューリッヒ': [('フランクフルト', 4.0), ('ミュンヘン', 4.5), ('ミラノ', 3.5)],
        'ミラノ': [('チューリッヒ', 3.5), ('ザグレブ', 7.0), ('リヨン', 5.5), ('ローマ', 3.0)],
        'ローマ': [('ミラノ', 3.0), ('ナポリ', 1.5)],
        'ナポリ': [('ローマ', 1.5)],
        'リヨン': [('パリ', 2.0), ('ミラノ', 5.5), ('バルセロナ', 5.0)],
        'バルセロナ': [('パリ', 6.5), ('リヨン', 5.0), ('マドリード', 3.0)],
        'マドリード': [('バルセロナ', 3.0), ('リスボン', 10.0)],
        'リスボン': [('マドリード', 10.0)]
    }
    return graph


def main():
    """
    メイン実行関数：複雑な鉄道網でダイクストラ法を実行
    """
    # ヨーロッパ鉄道網グラフを作成
    graph = create_europe_network()

    # グラフの統計情報を表示
    print("\n" + "=" * 60)
    print("グラフ構造: ヨーロッパ主要都市鉄道網")
    print("=" * 60)
    node_count = len(graph)
    edge_count = sum(len(edges) for edges in graph.values()) // 2
    print(f"ノード数: {node_count} 都市")
    print(f"エッジ数: {edge_count} 接続")
    print(f"平均次数: {edge_count * 2 / node_count:.2f}")

    # 一部の接続を表示
    print("\n主要な接続の例:")
    sample_cities = ['パリ', 'ベルリン', 'ローマ', 'ロンドン']
    for city in sample_cities:
        if city in graph:
            connections = ", ".join([f"{n}({w}h)" for n, w in graph[city][:3]])
            if len(graph[city]) > 3:
                connections += "..."
            print(f"  {city} → {connections}")

    print("\n" + "=" * 60)
    start_city = 'ロンドン'
    goal_city = 'アテネ'
    print(f"探索開始: {start_city} → {goal_city}")
    print("=" * 60 + "\n")

    # ダイクストラ法を実行
    path, total_cost = dijkstra_simple(graph, start_city, goal_city)

    # 結果を表示
    print("\n" + "=" * 60)
    print("結果")
    print("=" * 60)
    print(f"最短経路: {' → '.join(path)}")
    print(f"総移動時間: {total_cost:.1f} 時間")
    print(f"経由都市数: {len(path)} 都市")

    # 経路の詳細を表示
    print("\n経路の詳細:")
    for i in range(len(path) - 1):
        from_node = path[i]
        to_node = path[i + 1]
        weight = next(w for n, w in graph[from_node] if n == to_node)
        print(f"  {from_node} → {to_node}: {weight:.1f} 時間")

    print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    main()
