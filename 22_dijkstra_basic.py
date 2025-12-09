"""
ダイクストラ法 - 基本実装（優先度キューなし）

このプログラムは、ダイクストラ法の最も基本的な実装です。
- 全ノードを毎回チェックして最小距離のノードを探索
- 計算量: O(V²) （Vはノード数）
- 直感的でわかりやすい実装
"""

def dijkstra_basic(graph, start, goal):
    """
    基本的なダイクストラ法による最短経路探索

    Args:
        graph (dict): グラフ構造 {ノード: [(隣接ノード, 重み), ...]}
        start (str): 始点ノード
        goal (str): 目標ノード

    Returns:
        tuple: (最短経路のリスト, 総コスト)
    """
    # Step1: 初期化
    # すべてのノードの距離を無限大に設定
    distances = {node: float('inf') for node in graph}
    distances[start] = 0  # 始点のみ0に設定
    visited = set()  # 訪問済みノードの集合
    previous = {}  # 経路復元用の親ノード記録

    print(f"距離の初期化: {distances}\n")

    # Step2: 全ノードを訪問するまで繰り返し
    for step in range(len(graph)):
        # 未訪問ノードの中から最小距離のノードを探索
        min_distance = float('inf')
        min_node = None

        # 全ノードをチェック（ここがO(V)の操作）
        for node in graph:
            if node not in visited and distances[node] < min_distance:
                min_distance = distances[node]
                min_node = node

        # すべて訪問済みまたは到達不可能な場合は終了
        if min_node is None:
            break

        # 選択したノードを訪問済みに追加
        visited.add(min_node)
        print(f"ステップ {step+1}: 選択ノード: {min_node} (距離: {distances[min_node]})")

        # 目標に到達したら探索を終了
        if min_node == goal:
            print(f"目標ノード {goal} に到達！")
            break

        # Step3: 隣接ノードの距離を更新
        for neighbor, weight in graph[min_node]:
            # 現在のノードを経由した場合の新しい距離を計算
            new_distance = distances[min_node] + weight

            # より短い経路が見つかった場合、距離を更新
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = min_node  # 親ノードを記録
                print(f"  → {neighbor} への距離を更新: {distances[neighbor]}")

        print()  # 空行を追加

    # Step4: 経路を復元
    path = []
    node = goal

    # ゴールから始点まで逆順にたどる
    while node in previous:
        path.append(node)
        node = previous[node]
    path.append(start)
    path.reverse()  # 逆順にして始点→ゴールの順序にする

    return path, distances[goal]


def create_japan_road_network():
    """
    日本の主要都市間道路網を模した複雑なグラフを作成

    ノード数: 20都市
    エッジ数: 約40の接続
    重み: 都市間の距離（km単位を10で割った値）
    """
    # 実際の日本の主要都市間の概算距離（km）を基にしたグラフ
    graph = {
        '札幌': [('函館', 30), ('旭川', 14)],
        '函館': [('札幌', 30), ('青森', 11)],
        '旭川': [('札幌', 14)],
        '青森': [('函館', 11), ('秋田', 18), ('盛岡', 18)],
        '秋田': [('青森', 18), ('盛岡', 16), ('山形', 19)],
        '盛岡': [('青森', 18), ('秋田', 16), ('仙台', 18)],
        '山形': [('秋田', 19), ('仙台', 6), ('新潟', 17)],
        '仙台': [('盛岡', 18), ('山形', 6), ('福島', 9), ('新潟', 19)],
        '福島': [('仙台', 9), ('新潟', 20), ('宇都宮', 14)],
        '新潟': [('山形', 17), ('仙台', 19), ('福島', 20), ('長野', 24), ('富山', 23)],
        '宇都宮': [('福島', 14), ('東京', 10), ('水戸', 11)],
        '水戸': [('宇都宮', 11), ('東京', 12)],
        '東京': [('宇都宮', 10), ('水戸', 12), ('横浜', 3), ('静岡', 18), ('長野', 22)],
        '横浜': [('東京', 3), ('静岡', 16)],
        '長野': [('新潟', 24), ('東京', 22), ('富山', 16), ('名古屋', 20)],
        '富山': [('新潟', 23), ('長野', 16), ('金沢', 6), ('名古屋', 18)],
        '金沢': [('富山', 6), ('名古屋', 15), ('福井', 7)],
        '福井': [('金沢', 7), ('名古屋', 14), ('京都', 12)],
        '静岡': [('東京', 18), ('横浜', 16), ('名古屋', 18)],
        '名古屋': [('静岡', 18), ('長野', 20), ('富山', 18), ('金沢', 15), ('福井', 14), ('京都', 14), ('大阪', 16)],
        '京都': [('福井', 12), ('名古屋', 14), ('大阪', 5), ('神戸', 7)],
        '大阪': [('名古屋', 16), ('京都', 5), ('神戸', 3), ('和歌山', 10), ('岡山', 18)],
        '神戸': [('京都', 7), ('大阪', 3), ('岡山', 15)],
        '和歌山': [('大阪', 10)],
        '岡山': [('大阪', 18), ('神戸', 15), ('広島', 16), ('松山', 20)],
        '広島': [('岡山', 16), ('松山', 18), ('山口', 18)],
        '松山': [('岡山', 20), ('広島', 18), ('高知', 12)],
        '高知': [('松山', 12)],
        '山口': [('広島', 18), ('福岡', 18)],
        '福岡': [('山口', 18), ('長崎', 15), ('熊本', 11), ('大分', 13)],
        '長崎': [('福岡', 15), ('熊本', 12)],
        '熊本': [('福岡', 11), ('長崎', 12), ('大分', 12), ('宮崎', 13), ('鹿児島', 18)],
        '大分': [('福岡', 13), ('熊本', 12), ('宮崎', 13)],
        '宮崎': [('熊本', 13), ('大分', 13), ('鹿児島', 14)],
        '鹿児島': [('熊本', 18), ('宮崎', 14)]
    }
    return graph


def main():
    """
    メイン実行関数：複雑な道路網でダイクストラ法を実行
    """
    # 日本の道路網グラフを作成
    graph = create_japan_road_network()

    # グラフの統計情報を表示
    print("\n" + "=" * 60)
    print("グラフ構造: 日本主要都市道路網")
    print("=" * 60)
    node_count = len(graph)
    edge_count = sum(len(edges) for edges in graph.values()) // 2  # 無向グラフなので2で割る
    print(f"ノード数: {node_count} 都市")
    print(f"エッジ数: {edge_count} 接続")
    print(f"平均次数: {edge_count * 2 / node_count:.2f}")

    # 一部の接続を表示
    print("\n主要な接続の例:")
    sample_cities = ['東京', '大阪', '福岡', '札幌', '名古屋']
    for city in sample_cities:
        if city in graph:
            connections = ", ".join([f"{n}({w}×10km)" for n, w in graph[city]])
            print(f"  {city} → {connections}")

    print("\n" + "=" * 60)
    start_city = '東京'
    goal_city = '福岡'
    print(f"探索開始: {start_city} → {goal_city}")
    print("=" * 60 + "\n")

    # ダイクストラ法を実行
    path, cost = dijkstra_basic(graph, start_city, goal_city)

    # 結果を表示
    print("\n" + "=" * 60)
    print("結果")
    print("=" * 60)
    print(f"最短経路: {' → '.join(path)}")
    print(f"総距離: {cost * 10} km （コスト値: {cost}）")
    print(f"経由都市数: {len(path)} 都市")

    # 経路の詳細を表示
    print("\n経路の詳細:")
    for i in range(len(path) - 1):
        from_node = path[i]
        to_node = path[i + 1]
        # エッジの重みを見つける
        weight = next(w for n, w in graph[from_node] if n == to_node)
        print(f"  {from_node} → {to_node}: {weight * 10} km")

    print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    main()
