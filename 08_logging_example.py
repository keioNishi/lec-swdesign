import logging
from datetime import datetime

# ログ出力を統合管理するカスタムロガークラス
class ApplicationLogger:
    def __init__(self, name, level=logging.INFO):
        # 名前付きロガーを取得してアプリケーション固有のログ出力を設定
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # ログメッセージのフォーマットを定義 - %記法による文字列フォーマット
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        # ファイルハンドラー：ログをファイルに出力
        file_handler = logging.FileHandler('app.log')
        file_handler.setFormatter(formatter)

        # コンソールハンドラー：ログを標準出力に表示
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        # ロガーに複数のハンドラーを追加（ファイルとコンソールの両方に出力）
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    # ログレベル別のメソッド - ログレベルによって出力の重要度を分類
    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

    def warning(self, message):
        self.logger.warning(message)

    def debug(self, message):
        self.logger.debug(message)

# スクリプトが直接実行された場合のみ以下を実行
if __name__ == "__main__":
    # カスタムロガーのインスタンスを作成
    logger = ApplicationLogger("BankSystem")

    # 各ログレベルでのメッセージ出力例
    logger.info("システム開始")
    logger.info("ユーザーがログインしました")
    logger.warning("残高が不足しています")
    logger.error("エラーが発生しました")

    print("\nログファイル 'app.log' が作成されました。内容を確認してください。")
