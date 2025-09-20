# -*- coding: utf-8 -*-

# グローバル変数としてサンプルデータを定義
student_name = "田中太郎"
student_age = 20
student_grade = "A"

# 手続き型プログラミングの例：単純な関数で学生情報を表示
def print_student_info(name, age, grade):
    print(f"名前: {name}, 年齢: {age}, 成績: {grade}")

# オブジェクト指向プログラミングの例：学生をクラスで表現
class Student:
    # コンストラクタ：オブジェクト作成時に呼ばれる特別なメソッド
    def __init__(self, name, age, grade):
        self.name = name
        self.age = age
        self.grade = grade

    def print_info(self):
        print(f"名前: {self.name}, 年齢: {self.age}, 成績: {self.grade}")

# スクリプトが直接実行された場合のみ以下を実行
if __name__ == "__main__":
    print("=== 手続き型プログラミング ===")
    print_student_info(student_name, student_age, student_grade)

    print("\n=== オブジェクト指向プログラミング ===")
    student1 = Student("田中太郎", 20, "A")
    student1.print_info()
