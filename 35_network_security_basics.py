"""
ネットワークセキュリティの基礎

ネットワークセキュリティとは：
- ネットワーク上での情報資産の保護
- 不正アクセス、盗聴、改ざん、なりすましの防止
- 暗号化、認証、アクセス制御の実装
- ファイアウォール、IDS/IPS、VPNなどの技術
"""

import socket
import ssl
import hashlib
import hmac
import base64
import os
import time
from datetime import datetime
import threading


class NetworkSecurityDemo:
    """ネットワークセキュリティのデモンストレーション"""

    def __init__(self):
        self.security_threats = {
            'Eavesdropping': '盗聴 - 通信内容の不正傍受',
            'Man-in-the-Middle': '中間者攻撃 - 通信の中継・改ざん',
            'Replay Attack': 'リプレイ攻撃 - 過去の通信の再送',
            'IP Spoofing': 'IPスプーフィング - 送信元IPの偽装',
            'Port Scanning': 'ポートスキャン - 開放ポートの探索',
            'DDoS': 'DDoS攻撃 - 大量リクエストによるサービス停止'
        }

    def explain_security_threats(self):
        """ネットワークセキュリティ脅威の説明"""
        print("=== ネットワークセキュリティ脅威 ===")

        for threat, description in self.security_threats.items():
            print(f"{threat}:")
            print(f"  {description}")
            print()

    def demonstrate_encryption(self):
        """暗号化のデモンストレーション"""
        print("=== 暗号化デモ ===")

        # 1. ハッシュ関数（一方向暗号化）
        print("1. ハッシュ関数 (SHA-256):")
        original_data = "重要な機密データ"
        hash_object = hashlib.sha256(original_data.encode('utf-8'))
        hash_hex = hash_object.hexdigest()

        print(f"  元データ: {original_data}")
        print(f"  SHA-256: {hash_hex}")
        print(f"  ハッシュ長: {len(hash_hex)} 文字")

        # 2. HMAC（メッセージ認証コード）
        print("\\n2. HMAC (Hash-based Message Authentication Code):")
        secret_key = b"secret_key_12345"
        message = "認証が必要なメッセージ"

        hmac_object = hmac.new(secret_key, message.encode('utf-8'), hashlib.sha256)
        hmac_hex = hmac_object.hexdigest()

        print(f"  メッセージ: {message}")
        print(f"  HMAC: {hmac_hex}")
        print(f"  用途: メッセージの完全性確認")

        # 3. Base64エンコーディング（暗号化ではないが、データエンコーディング）
        print("\\n3. Base64 エンコーディング:")
        data = "バイナリデータのエンコード例"
        encoded = base64.b64encode(data.encode('utf-8')).decode('ascii')
        decoded = base64.b64decode(encoded).decode('utf-8')

        print(f"  元データ: {data}")
        print(f"  Base64: {encoded}")
        print(f"  デコード: {decoded}")

    def demonstrate_secure_socket(self):
        """セキュアソケット (SSL/TLS) のデモ"""
        print("\\n=== SSL/TLS セキュア通信デモ ===")

        print("SSL/TLS の特徴:")
        print("- 通信の暗号化")
        print("- サーバー認証（証明書検証）")
        print("- データの完全性保証")
        print("- 鍵交換の安全性")

        # 実際のSSL接続のデモ（外部サービスへの接続）
        self.ssl_connection_demo()

    def ssl_connection_demo(self):
        """SSL接続のデモンストレーション"""
        print("\\n--- SSL接続デモ ---")

        try:
            # HTTPSサイトへのSSL接続
            hostname = "httpbin.org"
            port = 443

            print(f"SSL接続先: {hostname}:{port}")

            # SSL コンテキストを作成
            context = ssl.create_default_context()

            # 通常のソケットを作成
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)

            # SSL でラップ
            ssl_sock = context.wrap_socket(sock, server_hostname=hostname)

            # SSL 接続を確立
            ssl_sock.connect((hostname, port))

            print(f"✓ SSL接続確立成功")

            # SSL証明書情報を取得
            cert = ssl_sock.getpeercert()
            print(f"証明書情報:")
            print(f"  Subject: {dict(x[0] for x in cert['subject'])}")
            print(f"  Issuer: {dict(x[0] for x in cert['issuer'])}")
            print(f"  Version: {cert.get('version', 'N/A')}")
            print(f"  Serial Number: {cert.get('serialNumber', 'N/A')}")

            # 暗号化スイート情報
            cipher = ssl_sock.cipher()
            if cipher:
                print(f"暗号化スイート: {cipher[0]}")
                print(f"プロトコル: {cipher[1]}")
                print(f"暗号強度: {cipher[2]} bits")

            # 簡単なHTTPS リクエストを送信
            request = "GET /get HTTP/1.1\\r\\nHost: httpbin.org\\r\\nConnection: close\\r\\n\\r\\n"
            ssl_sock.send(request.encode())

            # レスポンスを受信（一部のみ）
            response = ssl_sock.recv(1024).decode('utf-8', errors='ignore')
            print(f"\\nHTTPS レスポンス（抜粋）:")
            print(response[:200] + "..." if len(response) > 200 else response)

            ssl_sock.close()

        except Exception as e:
            print(f"✗ SSL接続エラー: {e}")

    def demonstrate_authentication(self):
        """認証メカニズムのデモ"""
        print("\\n=== 認証メカニズムデモ ===")

        # 1. パスワードハッシュ化
        print("1. パスワードハッシュ化:")
        password = "user_password_123"
        salt = os.urandom(16)  # ランダムソルト

        # PBKDF2 を使用したパスワードハッシュ化
        hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)

        print(f"  元パスワード: {password}")
        print(f"  ソルト: {salt.hex()}")
        print(f"  ハッシュ: {hashed_password.hex()}")

        # 2. パスワード検証
        print("\\n2. パスワード検証:")
        input_password = "user_password_123"
        verify_hash = hashlib.pbkdf2_hmac('sha256', input_password.encode(), salt, 100000)

        if verify_hash == hashed_password:
            print(f"  ✓ パスワード認証成功")
        else:
            print(f"  ✗ パスワード認証失敗")

        # 3. ワンタイムパスワード（TOTP風）の簡易実装
        print("\\n3. 時間ベースワンタイムパスワード（簡易版）:")
        current_time = int(time.time())
        time_step = 30  # 30秒間隔

        # 現在時刻を30秒単位で区切る
        time_counter = current_time // time_step

        # 簡易的なTOTP
        secret = b"shared_secret_key"
        totp_hash = hmac.new(secret, str(time_counter).encode(), hashlib.sha256)
        totp_code = int(totp_hash.hexdigest()[-6:], 16) % 1000000

        print(f"  現在時刻: {datetime.fromtimestamp(current_time)}")
        print(f"  時間カウンター: {time_counter}")
        print(f"  TOTP コード: {totp_code:06d}")
        print(f"  有効時間: {time_step}秒間")

    def demonstrate_firewall_simulation(self):
        """ファイアウォールのシミュレーション"""
        print("\\n=== ファイアウォール シミュレーション ===")

        # 簡易ファイアウォール ルール
        firewall_rules = [
            {'action': 'ALLOW', 'src': '192.168.1.0/24', 'dst_port': 80, 'protocol': 'TCP'},
            {'action': 'ALLOW', 'src': '192.168.1.0/24', 'dst_port': 443, 'protocol': 'TCP'},
            {'action': 'ALLOW', 'src': '192.168.1.0/24', 'dst_port': 53, 'protocol': 'UDP'},
            {'action': 'DENY', 'src': '0.0.0.0/0', 'dst_port': 22, 'protocol': 'TCP'},
            {'action': 'DENY', 'src': '0.0.0.0/0', 'dst_port': 3389, 'protocol': 'TCP'},
            {'action': 'ALLOW', 'src': '0.0.0.0/0', 'dst_port': 0, 'protocol': 'ICMP'}
        ]

        print("ファイアウォール ルール:")
        for i, rule in enumerate(firewall_rules, 1):
            print(f"  ルール {i}: {rule['action']} {rule['src']} → Port {rule['dst_port']} ({rule['protocol']})")

        # パケット検査シミュレーション
        print("\\nパケット検査シミュレーション:")
        test_packets = [
            {'src_ip': '192.168.1.100', 'dst_port': 80, 'protocol': 'TCP'},
            {'src_ip': '10.0.0.1', 'dst_port': 22, 'protocol': 'TCP'},
            {'src_ip': '192.168.1.50', 'dst_port': 443, 'protocol': 'TCP'},
            {'src_ip': '203.0.113.1', 'dst_port': 3389, 'protocol': 'TCP'}
        ]

        for packet in test_packets:
            result = self.check_firewall_rules(packet, firewall_rules)
            print(f"  {packet['src_ip']}:{packet['dst_port']} ({packet['protocol']}) → {result}")

    def check_firewall_rules(self, packet, rules):
        """ファイアウォール ルールをチェック"""
        src_ip = packet['src_ip']
        dst_port = packet['dst_port']
        protocol = packet['protocol']

        # 簡易的なルール マッチング
        for rule in rules:
            if rule['protocol'] == protocol or rule['protocol'] == 'ANY':
                if rule['dst_port'] == dst_port or rule['dst_port'] == 0:
                    # 簡易的なIP範囲チェック（実際はもっと複雑）
                    if (rule['src'] == '0.0.0.0/0' or
                            (rule['src'] == '192.168.1.0/24' and src_ip.startswith('192.168.1.'))):
                        return rule['action']

        return 'DENY'  # デフォルト拒否

    def demonstrate_intrusion_detection(self):
        """侵入検知システム（IDS）のシミュレーション"""
        print("\\n=== 侵入検知システム（IDS）シミュレーション ===")

        # 不審なアクティビティのパターン
        suspicious_patterns = [
            {'name': 'Port Scan', 'pattern': 'Multiple connections to different ports'},
            {'name': 'Brute Force', 'pattern': 'Multiple failed login attempts'},
            {'name': 'SQL Injection', 'pattern': "SQL keywords in HTTP requests"},
            {'name': 'DDoS', 'pattern': 'High volume of requests from single source'}
        ]

        print("監視対象の不審パターン:")
        for pattern in suspicious_patterns:
            print(f"  {pattern['name']}: {pattern['pattern']}")

        # ログ分析シミュレーション
        print("\\nログ分析シミュレーション:")
        sample_logs = [
            "2024-03-15 10:00:01 192.168.1.100 → 10.0.0.1:22 TCP CONNECT",
            "2024-03-15 10:00:02 192.168.1.100 → 10.0.0.1:23 TCP CONNECT",
            "2024-03-15 10:00:03 192.168.1.100 → 10.0.0.1:80 TCP CONNECT",
            "2024-03-15 10:00:04 203.0.113.1 → 10.0.0.1:22 SSH LOGIN_FAILED",
            "2024-03-15 10:00:05 203.0.113.1 → 10.0.0.1:22 SSH LOGIN_FAILED",
            "2024-03-15 10:00:06 203.0.113.1 → 10.0.0.1:22 SSH LOGIN_FAILED"
        ]

        for log in sample_logs:
            threat_detected = self.analyze_log_entry(log)
            status = "🚨 ALERT" if threat_detected else "✓ NORMAL"
            print(f"  {status}: {log}")

    def analyze_log_entry(self, log_entry):
        """ログエントリを分析して脅威を検知"""
        # 簡易的な脅威検知ロジック
        if "LOGIN_FAILED" in log_entry:
            return True  # ブルートフォース攻撃の可能性

        # ポートスキャンの検知（実際はより複雑な分析が必要）
        if any(port in log_entry for port in [":22", ":23", ":80"]):
            # 複数ポートへの接続パターンをチェック（簡略化）
            return False  # この例では簡単のため False

        return False

    def network_security_best_practices(self):
        """ネットワークセキュリティのベストプラクティス"""
        print("\\n=== ネットワークセキュリティ ベストプラクティス ===")

        best_practices = [
            "1. 多層防御（Defense in Depth）の実装",
            "2. 最小権限の原則（Principle of Least Privilege）",
            "3. 定期的なセキュリティ監査とペネトレーションテスト",
            "4. セキュリティパッチの迅速な適用",
            "5. 強力な認証メカニズム（多要素認証）の導入",
            "6. ネットワークセグメンテーションの実装",
            "7. 暗号化通信（SSL/TLS）の徹底",
            "8. ログ監視と異常検知システムの導入",
            "9. 従業員のセキュリティ教育",
            "10. インシデント対応計画の策定と訓練"
        ]

        for practice in best_practices:
            print(f"  {practice}")


def main():
    """メインデモ関数"""
    print("ネットワークセキュリティ基礎デモ")
    print("=" * 50)

    demo = NetworkSecurityDemo()

    # 1. セキュリティ脅威の説明
    demo.explain_security_threats()

    # 2. 暗号化のデモ
    demo.demonstrate_encryption()

    # 3. SSL/TLS セキュア通信
    demo.demonstrate_secure_socket()

    # 4. 認証メカニズム
    demo.demonstrate_authentication()

    # 5. ファイアウォール シミュレーション
    demo.demonstrate_firewall_simulation()

    # 6. 侵入検知システム
    demo.demonstrate_intrusion_detection()

    # 7. ベストプラクティス
    demo.network_security_best_practices()

    print("\\n" + "=" * 50)
    print("ネットワークセキュリティデモ完了")
    print("\\n重要なポイント:")
    print("- セキュリティは多層的に実装する")
    print("- 暗号化と認証は基本中の基本")
    print("- 継続的な監視と対応が重要")
    print("- 人的要因も含めた総合的な対策が必要")


if __name__ == "__main__":
    main()