"""
暗号化の基本概念と実装
データ保護のための暗号化技術
"""

from cryptography.fernet import Fernet
import base64

# SimpleCryptoクラスの実装
class SimpleCrypto:
    # initをまとめる __init__ 関数では self を基に処理の流れを整理します。
    def __init__(self):
        
        self.key = Fernet.generate_key()
        
        self.cipher = Fernet(self.key)

    # メッセージの暗号化
    def encrypt_message(self, message):
        """メッセージの暗号化"""
        
        encrypted = self.cipher.encrypt(message.encode())
        # 求めた バイト列を文字列に戻します を呼び出し元へ返します。
        return base64.urlsafe_b64encode(encrypted).decode()

    # メッセージの復号化
    def decrypt_message(self, encrypted_message):
        """メッセージの復号化"""
        
        encrypted_bytes = base64.urlsafe_b64decode(encrypted_message.encode())
        
        decrypted = self.cipher.decrypt(encrypted_bytes)
        # 求めた バイト列を文字列に戻します を呼び出し元へ返します。
        return decrypted.decode()

    # 暗号化キーの取得（Base64エンコード）
    def get_key(self):
        """暗号化キーの取得（Base64エンコード）"""
        # 求めた バイト列を文字列に戻します を呼び出し元へ返します。
        return base64.urlsafe_b64encode(self.key).decode()

# demo_encryption関数 — 暗号化デモの実行
def demo_encryption():
    """暗号化デモの実行"""
    
    print("=== 暗号化の基本概念デモ ===")

    crypto = SimpleCrypto()

    test_messages = [
        "これは機密情報です",
        "パスワード: secret123",
        "クレジットカード: 1234-5678-9012-3456",
        "機密データを送信します"
    ]

    print("\n暗号化・復号化テスト:")
    
    print(f"使用暗号化キー: {crypto.get_key()[:20]}...")

    # enumerate(test_messages, 1) から要素を取り出し、順番に (i, message) に入れて処理します。
    for i, message in enumerate(test_messages, 1):
        
        print(f"\n{i}. テストメッセージ:")
        
        print(f"   元のメッセージ: {message}")

        encrypted = crypto.encrypt_message(message)
        
        print(f"   暗号化後: {encrypted[:50]}...")

        decrypted = crypto.decrypt_message(encrypted)
        
        print(f"   復号化後: {decrypted}")

        verification = "✓ 正常" if message == decrypted else "✗ エラー"
        
        print(f"   検証結果: {verification}")

    print("\n異なるキーでの復号化テスト:")
    
    crypto2 = SimpleCrypto()  # 異なるキーを持つインスタンス

    message = "テストメッセージ"
    
    encrypted_with_key1 = crypto.encrypt_message(message)

    # エラーの発生を監視しながら安全に処理を進めるための try ブロックです。
    try:
        
        decrypted_with_key2 = crypto2.decrypt_message(encrypted_with_key1)
        
        print("   復号化成功（予期しない結果）")
    
    except Exception as e:
        
        print("   復号化失敗（期待される結果）: 異なるキーでは復号化できません")

if __name__ == "__main__":
    # エラーの発生を監視しながら安全に処理を進めるための try ブロックです。
    try:
        
        demo_encryption()
    
    except ImportError:
        
        print("暗号化ライブラリが見つかりません。以下のコマンドでインストールしてください:")
        
        print("pip install cryptography")

        import hashlib

        print("\n=== 代替実装: ハッシュ化デモ ===")

        messages = ["機密データ1", "機密データ2", "重要な情報"]

        # messages から要素を取り出し、順番に message に入れて処理します。
        for message in messages:
            # ハッシュvalueを整えるために ハッシュ値を 16 進文字列で取り出します。hashlib モジュールは多様なハッシュ関数を提供します。
            hash_value = hashlib.sha256(message.encode()).hexdigest()
            
            print(f"メッセージ: {message}")
            
            print(f"ハッシュ値: {hash_value}")
            # print で空行を出力して区切りを入れます。
            print()
