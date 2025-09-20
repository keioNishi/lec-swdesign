# カプセル化の例：propertyyデコレータでデータへのアクセスを制御
class Temperature:
    def __init__(self, celsius=0):
        self._celsius = celsius  # アンダースコアは「非公開」を意味する規約

    @property  # getterデコレータ：メソッドを属性のように使える
    def celsius(self):
        return self._celsius

    @celsius.setter  # setterデコレータ：値の設定時にバリデーションを実行
    def celsius(self, value):
        if value < -273.15:  # 絶対零度以下のチェック
            raise ValueError("絶対零度以下は設定不可")
        self._celsius = value

    @property  # 読み取り専用プロパティ（setterなし）
    def fahrenheit(self):
        return (self._celsius * 9/5) + 32  # 摂氏から華氏への変換公式

# 遅延評価（lazy evaluation）の例：初回アクセス時のみ処理を実行
class DataProcessor:
    def __init__(self, data):
        self._data = data
        self._processed = None  # キャッシュ用の変数

    @property
    def processed_data(self):
        if self._processed is None:  # 初回アクセス時のみ処理を実行
            print("データを処理中...")
            self._processed = [x * 2 for x in self._data]  # リスト内包表記
        return self._processed

if __name__ == "__main__":
    # propertyを使ったカプセル化のデモ
    temp = Temperature(25)
    print(f"摂氏: {temp.celsius}度")  # getterが呼ばれる
    print(f"華氏: {temp.fahrenheit}度")  # 自動計算

    temp.celsius = 30  # setterが呼ばれ、バリデーションが実行される
    print(f"新しい華氏温度: {temp.fahrenheit}度")

    # 例外処理：try-except文でエラーを捕捉
    try:
        temp.celsius = -300  # setterのバリデーションでエラー発生
    except ValueError as e:  # 特定の例外型を捕捉
        print(f"エラー: {e}")

    print("\n=== データ処理の例 ===")
    processor = DataProcessor([1, 2, 3, 4, 5])
    print(processor.processed_data)  # 1回目：処理実行される
    print(processor.processed_data)  # 2回目：キャッシュされた結果を返す
