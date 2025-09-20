from abc import ABC, abstractmethod

# 抽象クラス：実装を強制するテンプレートクラス
class Shape(ABC):  # ABC(Abstract Base Class)を継承
    @abstractmethod  # デコレータ：子クラスで必ず実装が必要
    def area(self):
        pass  # 実装なし（子クラスで実装する）

    @abstractmethod
    def perimeter(self):
        pass

    # 共通メソッド：抽象メソッドを使って実装
    def description(self):
        return f"面積: {self.area()}, 周囲長: {self.perimeter()}"

# 抽象クラスを継承した具体クラス：長方形
class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    # 抽象メソッドの実装が必須
    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

# 抽象クラスを継承した具体クラス：円
class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14159 * self.radius ** 2  # 円の面積 = π × r²

    def perimeter(self):
        return 2 * 3.14159 * self.radius  # 円周 = 2 × π × r

if __name__ == "__main__":
    # 具体クラスのインスタンス作成と抽象メソッドの呼び出し
    rectangle = Rectangle(5, 3)
    circle = Circle(4)

    print("長方形:")
    print(f"面積: {rectangle.area()}")
    print(f"周囲長: {rectangle.perimeter()}")
    print(rectangle.description())  # 親クラスの共通メソッドを使用

    print("\n円:")
    print(f"面積: {circle.area()}")
    print(f"周囲長: {circle.perimeter()}")
    print(circle.description())

    # 抽象クラスは直接インスタンス化できないことを確認
    try:
        shape = Shape()  # TypeErrorが発生
    except TypeError as e:
        print(f"\n抽象クラスのインスタンス化エラー: {e}")
