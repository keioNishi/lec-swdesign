# カスタム例外クラス：独自の例外を定義してより具体的なエラー情報を提供
class InsufficientFundsError(Exception):  # Exception クラスを継承
    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount
        # 親クラスのコンストラクタにエラーメッセージを渡す
        super().__init__(f"残高不足: 残高{balance}, 引出額{amount}")

class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance

    def withdraw(self, amount):
        # 入力値検証：不正な値に対してはValueErrorを発生
        if amount <= 0:
            raise ValueError("引出額は正の数である必要があります")
        # ビジネスロジック検証：残高不足にはカスタム例外を発生
        if amount > self.balance:
            raise InsufficientFundsError(self.balance, amount)
        self.balance -= amount

if __name__ == "__main__":
    account = BankAccount(1000)

    # 複数の例外型を個別に処理する例
    try:
        account.withdraw(1500)  # 残高不足エラーを発生させる
    except InsufficientFundsError as e:  # カスタム例外をキャッチ
        print(f"エラー: {e}")
    except ValueError as e:  # 標準例外をキャッチ
        print(f"入力エラー: {e}")

    # 負の値での引き出し試行
    try:
        account.withdraw(-100)
    except ValueError as e:
        print(f"入力エラー: {e}")

    # 正常なケース
    try:
        account.withdraw(500)
        print(f"引き出し成功。残高: {account.balance}")
    except Exception as e:  # 想定外のエラーをキャッチする最終手段
        print(f"予期しないエラー: {e}")
