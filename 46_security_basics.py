"""
サイバーセキュリティの基本概念と実装
情報セキュリティの三大要素（CIA）とセキュリティデモ
"""

import hashlib
import base64

# 情報セキュリティの三大要素（CIA）をデモンストレーションするクラス
class SimpleSecurityDemo:
    def __init__(self):
        # サンプルユーザーデータ（実際のシステムではハッシュ化されている）
        self.users = {"admin": "password123", "user1": "mypass"}

    def authenticate(self, username, password):
        """機密性（Confidentiality）: 認可された者のみがアクセス"""
        if username in self.users and self.users[username] == password:
            return True
        return False

    def create_hash(self, data):
        """完全性（Integrity）: データが改ざんされていないことを確認"""
        return hashlib.sha256(data.encode()).hexdigest()

    def check_availability(self):
        """可用性（Availability）: 必要な時にシステムが利用できること"""
        return {"status": "online", "timestamp": "2024-03-15 10:00:00"}

def main():
    """セキュリティデモの実行"""
    demo = SimpleSecurityDemo()

    print("=== 情報セキュリティの三大要素（CIA）デモ ===")
    print(f"認証テスト (機密性): {demo.authenticate('admin', 'password123')}")
    print(f"データハッシュ (完全性): {demo.create_hash('重要なデータ')}")
    print(f"システム状態 (可用性): {demo.check_availability()}")

if __name__ == "__main__":
    main()
