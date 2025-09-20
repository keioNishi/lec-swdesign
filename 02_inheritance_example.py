# -*- coding: utf-8 -*-

# 継承の例：親クラス（基底クラス）としての乗り物
class Vehicle:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model

    def start(self):
        print(f"{self.brand} {self.model} のエンジンを始動")

    def stop(self):
        print(f"{self.brand} {self.model} のエンジンを停止")

# Vehicleを継承した子クラス：自動車
class Car(Vehicle):  # 継承の構文：class 子クラス(親クラス)
    def __init__(self, brand, model, doors):
        super().__init__(brand, model)  # 親クラスのコンストラクタを呼び出し
        self.doors = doors

    def open_trunk(self):
        print("トランクを開きます")

# Vehicleを継承した子クラス：バイク
class Motorcycle(Vehicle):
    def __init__(self, brand, model, engine_size):
        super().__init__(brand, model)
        self.engine_size = engine_size

    def wheelie(self):
        print("ウィリーします")

if __name__ == "__main__":
    # オブジェクトの作成：継承したクラスからインスタンスを作成
    car = Car("Toyota", "Prius", 4)
    bike = Motorcycle("Honda", "CBR", 600)

    # 継承したメソッド（start, stop）と子クラスの独自メソッドを使用
    car.start()  # 親クラスから継承したメソッド
    car.open_trunk()  # Carクラス独自のメソッド

    bike.start()  # 親クラスから継承したメソッド
    bike.wheelie()  # Motorcycleクラス独自のメソッド

    car.stop()
    bike.stop()
