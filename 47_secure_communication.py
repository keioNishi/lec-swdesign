"""
暗号化通信の実装
パスワードベース鍵導出、SSL/TLS、セキュア通信
"""

import ssl
import socket
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import base64
import os

# SecureCommunicationクラスの実装
class SecureCommunication:
    def __init__(self, password):
        self.password = password.encode()
        
        self.key = self._derive_key()
        
        self.cipher = Fernet(self.key)

    # パスワードから暗号化キーを導出
    def _derive_key(self):
        """パスワードから暗号化キーを導出"""
        
        salt = b'stable_salt_for_demo'  # 実際は random で生成
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        
        key = base64.urlsafe_b64encode(kdf.derive(self.password))
        
        return key

    # メッセージの暗号化
    def encrypt_message(self, message):
        """メッセージの暗号化"""
        return self.cipher.encrypt(message.encode())

    # メッセージの復号化
    def decrypt_message(self, encrypted_message):
        """メッセージの復号化"""
        return self.cipher.decrypt(encrypted_message).decode()

    # SSL/TLS サーバーの作成（概念的な例）
    def create_secure_server(self, host='localhost', port=8443):
        """SSL/TLS サーバーの作成（概念的な例）"""
        
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        
        return {
            'host': host,
            'port': port,
            'ssl_context': 'configured',
            'security_protocols': ['TLSv1.2', 'TLSv1.3']
        }

# SecureFileHandlerクラスの実装
class SecureFileHandler:
    def __init__(self, password):
        
        self.crypto = SecureCommunication(password)

    # ファイル内容の暗号化
    def encrypt_file_content(self, content):
        """ファイル内容の暗号化"""
        return self.crypto.encrypt_message(content)

    # ファイル内容の復号化
    def decrypt_file_content(self, encrypted_content):
        """ファイル内容の復号化"""
        return self.crypto.decrypt_message(encrypted_content)

    # セキュアファイル転送のシミュレーション
    def secure_file_transfer_simulation(self, filename, content):
        """セキュアファイル転送のシミュレーション"""
        
        print(f"セキュアファイル転送シミュレーション: {filename}")

        encrypted_content = self.encrypt_file_content(content)
        
        print(f"  ステップ1: ファイル暗号化完了 ({len(encrypted_content)} bytes)")

        transfer_success = self._simulate_transfer(encrypted_content)

        if transfer_success:
            
            decrypted_content = self.decrypt_file_content(encrypted_content)
            
            print(f"  ステップ2: ファイル転送完了")
            
            print(f"  ステップ3: 復号化完了")

            integrity_check = content == decrypted_content
            
            print(f"  ステップ4: 整合性確認 - {'✓ 成功' if integrity_check else '✗ 失敗'}")

            return {
                "success": True,
                "original_size": len(content),
                "encrypted_size": len(encrypted_content),
                "integrity_verified": integrity_check
            }
        else:
            
            return {"success": False, "error": "転送失敗"}

    # ファイル転送のシミュレーション
    def _simulate_transfer(self, data):
        """ファイル転送のシミュレーション"""
        import random
        
        return random.random() > 0.1

# demo_secure_communication関数 — セキュア通信デモの実行
def demo_secure_communication():
    """セキュア通信デモの実行"""
    
    print("=== 暗号化通信実装デモ ===")

    secure_comm = SecureCommunication("my_secure_password")

    print("\n1. 基本暗号化・復号化テスト:")
    
    test_messages = [
        "機密データを送信します",
        "パスワード: SuperSecret123!",
        "重要な業務情報"
    ]

    for i, message in enumerate(test_messages, 1):
        
        print(f"\n  テスト {i}:")
        
        print(f"    元のメッセージ: {message}")

        encrypted = secure_comm.encrypt_message(message)
        
        print(f"    暗号化済み: {str(encrypted)[:50]}...")

        decrypted = secure_comm.decrypt_message(encrypted)
        
        print(f"    復号化後: {decrypted}")

        verification = "✓ 正常" if message == decrypted else "✗ エラー"
        
        print(f"    検証: {verification}")

    print("\n2. セキュアファイル転送シミュレーション:")
    
    file_handler = SecureFileHandler("file_transfer_password")

    test_files = [
        ("config.txt", "server_ip=192.168.1.1\npassword=secret\napi_key=abc123"),
        ("data.csv", "名前,年齢,職業\n田中,30,エンジニア\n佐藤,25,デザイナー"),
        ("secret.json", '{"api_key": "secret123", "database_url": "localhost:5432"}')
    ]

    for filename, content in test_files:
        
        print(f"\n  ファイル: {filename}")
        
        result = file_handler.secure_file_transfer_simulation(filename, content)

        if result["success"]:
            
            print(f"    元のサイズ: {result['original_size']} bytes")
            
            print(f"    暗号化サイズ: {result['encrypted_size']} bytes")
            
            print(f"    整合性確認: {'✓ 成功' if result['integrity_verified'] else '✗ 失敗'}")
        else:
            
            print(f"    転送失敗: {result.get('error', '不明なエラー')}")

    print("\n3. SSL/TLS設定例:")
    
    ssl_config = secure_comm.create_secure_server()
    
    print(f"    ホスト: {ssl_config['host']}")
    
    print(f"    ポート: {ssl_config['port']}")
    
    print(f"    セキュリティプロトコル: {ssl_config['security_protocols']}")
    
    print(f"    SSL設定: {ssl_config['ssl_context']}")

    print("\n4. セキュリティベストプラクティス:")
    print("    ✓ PBKDF2を使用した安全な鍵導出（100,000回反復）")
    
    print("    ✓ Fernet（AES 128 + HMAC）による認証付き暗号化")
    
    print("    ✓ TLS 1.2/1.3 対応の SSL/TLS 設定")
    
    print("    ✓ 送信前暗号化・受信後復号化による end-to-end 暗号化")

if __name__ == "__main__":
    try:
        
        demo_secure_communication()
    
    except ImportError as e:
        
        print(f"必要なライブラリが見つかりません: {e}")
        
        print("以下のコマンドでインストールしてください:")
        
        print("pip install cryptography")

        print("\n=== 代替実装: 基本的なエンコーディング ===")
        import base64

        message = "テストメッセージ"
        encoded = base64.b64encode(message.encode()).decode()
        decoded = base64.b64decode(encoded).decode()

        print(f"元のメッセージ: {message}")
        
        print(f"エンコード後: {encoded}")
        
        print(f"デコード後: {decoded}")
        
        print(f"検証: {'✓ 成功' if message == decoded else '✗ 失敗'}")
