"""
ネットワークプロトコルの基礎と実装

ネットワークプロトコルとは：
- コンピュータ間の通信規約
- OSI 7層モデル / TCP/IP 4層モデル
- 各層での役割と責任分離
- プロトコルスタックの理解
"""

import socket
import struct
import time
import threading
from datetime import datetime


class NetworkProtocolDemo:
    """ネットワークプロトコルのデモンストレーション"""

    def __init__(self):
        self.protocols_info = {
            'TCP': {
                'layer': 4,
                'description': 'Transmission Control Protocol - 信頼性のある接続型プロトコル',
                'features': ['接続指向', '順序保証', 'エラー訂正', 'フロー制御']
            },
            'UDP': {
                'layer': 4,
                'description': 'User Datagram Protocol - 高速な非接続型プロトコル',
                'features': ['非接続型', '高速', 'オーバーヘッド小', 'リアルタイム通信向け']
            },
            'IP': {
                'layer': 3,
                'description': 'Internet Protocol - パケット配送プロトコル',
                'features': ['アドレッシング', 'ルーティング', 'パケット分割', 'TTL管理']
            },
            'HTTP': {
                'layer': 7,
                'description': 'HyperText Transfer Protocol - Web通信プロトコル',
                'features': ['リクエスト/レスポンス', 'ステートレス', 'テキストベース', 'ポート80/443']
            }
        }

    def explain_osi_model(self):
        """OSI 7層モデルの説明"""
        print("=== OSI 7層モデル ===")

        osi_layers = [
            (7, "アプリケーション層", "HTTP, FTP, SMTP, DNS", "アプリケーション固有のプロトコル"),
            (6, "プレゼンテーション層", "SSL/TLS, 暗号化, 圧縮", "データの表現形式変換"),
            (5, "セッション層", "NetBIOS, RPC", "セッション管理と同期"),
            (4, "トランスポート層", "TCP, UDP", "エンドツーエンドの信頼性保証"),
            (3, "ネットワーク層", "IP, ICMP, ARP", "ルーティングとアドレッシング"),
            (2, "データリンク層", "Ethernet, Wi-Fi", "フレーム転送とエラー検出"),
            (1, "物理層", "ケーブル, 光ファイバー", "物理的な信号の送受信")
        ]

        for layer_num, layer_name, examples, description in osi_layers:
            print(f"第{layer_num}層: {layer_name}")
            print(f"  例: {examples}")
            print(f"  役割: {description}")
            print()

    def explain_tcpip_model(self):
        """TCP/IP 4層モデルの説明"""
        print("=== TCP/IP 4層モデル ===")

        tcpip_layers = [
            (4, "アプリケーション層", "HTTP, FTP, SMTP, DNS, SSH"),
            (3, "トランスポート層", "TCP, UDP"),
            (2, "インターネット層", "IP, ICMP, ARP"),
            (1, "ネットワークアクセス層", "Ethernet, Wi-Fi, PPP")
        ]

        for layer_num, layer_name, examples in tcpip_layers:
            print(f"第{layer_num}層: {layer_name}")
            print(f"  プロトコル例: {examples}")
            print()

    def demonstrate_tcp_features(self):
        """TCPの特徴をデモンストレーション"""
        print("=== TCP (Transmission Control Protocol) の特徴 ===")

        print("1. 接続確立（3-way handshake）:")
        print("   クライアント → サーバー: SYN")
        print("   サーバー → クライアント: SYN-ACK")
        print("   クライアント → サーバー: ACK")

        print("\\n2. 信頼性の保証:")
        print("   - シーケンス番号による順序保証")
        print("   - 確認応答（ACK）による到達確認")
        print("   - タイムアウト・再送による信頼性")

        print("\\n3. フロー制御:")
        print("   - ウィンドウサイズによる送信量制御")
        print("   - 受信バッファの状況に応じた調整")

        # 実際のTCP接続でのデモ
        self.tcp_connection_demo()

    def tcp_connection_demo(self):
        """TCP接続のデモンストレーション"""
        print("\\n--- TCP接続デモ ---")

        try:
            # TCPサーバーソケットを作成
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind(('localhost', 0))  # 空いているポートを自動選択
            port = server_socket.getsockname()[1]
            server_socket.listen(1)

            print(f"TCPサーバーがポート {port} で待機中...")

            # サーバーを別スレッドで起動
            def server_handler():
                try:
                    server_socket.settimeout(3)
                    client_socket, address = server_socket.accept()
                    print(f"  サーバー: クライアント {address} が接続しました")

                    # データを受信
                    data = client_socket.recv(1024)
                    print(f"  サーバー: 受信データ '{data.decode()}'")

                    # レスポンスを送信
                    response = "TCP接続成功！"
                    client_socket.send(response.encode())
                    print(f"  サーバー: レスポンス送信 '{response}'")

                    client_socket.close()
                except socket.timeout:
                    print("  サーバー: タイムアウト")
                except Exception as e:
                    print(f"  サーバーエラー: {e}")

            server_thread = threading.Thread(target=server_handler)
            server_thread.daemon = True
            server_thread.start()

            # 短い待機
            time.sleep(0.1)

            # TCPクライアントで接続
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(('localhost', port))
            print(f"  クライアント: サーバーに接続しました")

            # データを送信
            message = "Hello TCP Server"
            client_socket.send(message.encode())
            print(f"  クライアント: メッセージ送信 '{message}'")

            # レスポンスを受信
            response = client_socket.recv(1024)
            print(f"  クライアント: レスポンス受信 '{response.decode()}'")

            client_socket.close()
            server_socket.close()

            print("✓ TCP接続デモ完了")

        except Exception as e:
            print(f"✗ TCP接続デモエラー: {e}")

    def demonstrate_udp_features(self):
        """UDPの特徴をデモンストレーション"""
        print("\\n=== UDP (User Datagram Protocol) の特徴 ===")

        print("1. 非接続型通信:")
        print("   - 事前の接続確立が不要")
        print("   - 各パケットが独立")

        print("\\n2. 高速性:")
        print("   - オーバーヘッドが小さい")
        print("   - リアルタイム通信に適している")

        print("\\n3. 信頼性なし:")
        print("   - パケット到達保証なし")
        print("   - 順序保証なし")
        print("   - 重複チェックなし")

        # 実際のUDP通信でのデモ
        self.udp_communication_demo()

    def udp_communication_demo(self):
        """UDP通信のデモンストレーション"""
        print("\\n--- UDP通信デモ ---")

        try:
            # UDPサーバーソケットを作成
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            server_socket.bind(('localhost', 0))  # 空いているポートを自動選択
            port = server_socket.getsockname()[1]

            print(f"UDPサーバーがポート {port} で待機中...")

            # サーバーを別スレッドで起動
            def udp_server_handler():
                try:
                    server_socket.settimeout(3)
                    data, address = server_socket.recvfrom(1024)
                    print(f"  サーバー: {address} からデータ受信 '{data.decode()}'")

                    # レスポンスを送信
                    response = "UDP通信成功！"
                    server_socket.sendto(response.encode(), address)
                    print(f"  サーバー: レスポンス送信 '{response}'")

                except socket.timeout:
                    print("  サーバー: タイムアウト")
                except Exception as e:
                    print(f"  UDPサーバーエラー: {e}")

            server_thread = threading.Thread(target=udp_server_handler)
            server_thread.daemon = True
            server_thread.start()

            # 短い待機
            time.sleep(0.1)

            # UDPクライアントで通信
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            # データを送信
            message = "Hello UDP Server"
            client_socket.sendto(message.encode(), ('localhost', port))
            print(f"  クライアント: メッセージ送信 '{message}'")

            # レスポンスを受信
            client_socket.settimeout(3)
            response, server_address = client_socket.recvfrom(1024)
            print(f"  クライアント: レスポンス受信 '{response.decode()}'")

            client_socket.close()
            server_socket.close()

            print("✓ UDP通信デモ完了")

        except Exception as e:
            print(f"✗ UDP通信デモエラー: {e}")

    def analyze_packet_structure(self):
        """パケット構造の分析"""
        print("\\n=== パケット構造の分析 ===")

        print("1. Ethernetフレーム構造:")
        print("   [宛先MAC][送信元MAC][タイプ][データ][FCS]")

        print("\\n2. IPヘッダー構造（IPv4）:")
        print("   [バージョン][ヘッダ長][サービスタイプ][全長]")
        print("   [識別子][フラグ][フラグメントオフセット]")
        print("   [TTL][プロトコル][ヘッダチェックサム]")
        print("   [送信元IPアドレス][宛先IPアドレス]")

        print("\\n3. TCPヘッダー構造:")
        print("   [送信元ポート][宛先ポート]")
        print("   [シーケンス番号][確認応答番号]")
        print("   [ヘッダ長][フラグ][ウィンドウサイズ]")
        print("   [チェックサム][緊急ポインタ]")

        # 簡単なパケット構造のデモ
        self.create_dummy_packet()

    def create_dummy_packet(self):
        """ダミーパケットの作成"""
        print("\\n--- ダミーパケット作成デモ ---")

        try:
            # 簡単なUDPパケットヘッダーを作成
            source_port = 12345
            dest_port = 80
            length = 8 + len("Hello")  # ヘッダ8バイト + データ
            checksum = 0  # 簡略化のため0

            # UDPヘッダーをバイナリ形式で作成
            udp_header = struct.pack('!HHHH',
                                     source_port,  # 送信元ポート
                                     dest_port,    # 宛先ポート
                                     length,       # 長さ
                                     checksum      # チェックサム
                                     )

            payload = b"Hello"
            udp_packet = udp_header + payload

            print(f"作成されたUDPパケット:")
            print(f"  送信元ポート: {source_port}")
            print(f"  宛先ポート: {dest_port}")
            print(f"  長さ: {length} bytes")
            print(f"  ペイロード: {payload.decode()}")
            print(f"  パケット全体: {udp_packet.hex()}")

        except Exception as e:
            print(f"✗ パケット作成エラー: {e}")

    def demonstrate_protocol_stack(self):
        """プロトコルスタックのデモンストレーション"""
        print("\\n=== プロトコルスタック動作デモ ===")

        print("HTTP リクエスト送信時のプロトコルスタック:")
        print("\\n1. アプリケーション層:")
        print("   → HTTP リクエストを作成")
        print("   → 'GET / HTTP/1.1\\\\r\\\\nHost: example.com\\\\r\\\\n\\\\r\\\\n'")

        print("\\n2. トランスポート層 (TCP):")
        print("   → TCPヘッダーを追加")
        print("   → ポート番号設定 (送信元:ランダム, 宛先:80)")
        print("   → シーケンス番号、確認応答番号設定")

        print("\\n3. ネットワーク層 (IP):")
        print("   → IPヘッダーを追加")
        print("   → 送信元・宛先IPアドレス設定")
        print("   → TTL設定、パケット識別子設定")

        print("\\n4. データリンク層 (Ethernet):")
        print("   → Ethernetヘッダーを追加")
        print("   → 送信元・宛先MACアドレス設定")
        print("   → フレームチェックシーケンス追加")

        print("\\n5. 物理層:")
        print("   → 電気信号に変換して送信")

    def get_network_info(self):
        """ネットワーク情報の取得"""
        print("\\n=== ネットワーク情報取得 ===")

        try:
            # ホスト名とIPアドレス
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)

            print(f"ホスト名: {hostname}")
            print(f"ローカルIP: {local_ip}")

            # 外部接続時のローカルアドレス
            test_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            test_socket.connect(("8.8.8.8", 80))
            external_ip = test_socket.getsockname()[0]
            test_socket.close()

            print(f"外部接続用IP: {external_ip}")

            # DNS サーバー情報（簡易版）
            print("\\nよく使用されるDNSサーバー:")
            dns_servers = [
                ("Google DNS", "8.8.8.8"),
                ("Cloudflare DNS", "1.1.1.1"),
                ("OpenDNS", "208.67.222.222")
            ]

            for name, ip in dns_servers:
                print(f"  {name}: {ip}")

        except Exception as e:
            print(f"✗ ネットワーク情報取得エラー: {e}")


def main():
    """メインデモ関数"""
    print("ネットワークプロトコル基礎デモ")
    print("=" * 50)

    demo = NetworkProtocolDemo()

    # 1. OSI 7層モデルの説明
    demo.explain_osi_model()

    # 2. TCP/IP 4層モデルの説明
    demo.explain_tcpip_model()

    # 3. TCP の特徴とデモ
    demo.demonstrate_tcp_features()

    # 4. UDP の特徴とデモ
    demo.demonstrate_udp_features()

    # 5. パケット構造の分析
    demo.analyze_packet_structure()

    # 6. プロトコルスタックの動作
    demo.demonstrate_protocol_stack()

    # 7. ネットワーク情報の取得
    demo.get_network_info()

    print("\\n" + "=" * 50)
    print("ネットワークプロトコルデモ完了")
    print("\\n学習ポイント:")
    print("- 各層の役割と責任の分離")
    print("- TCP vs UDP の使い分け")
    print("- プロトコルスタックの理解")
    print("- パケット構造の基本知識")


if __name__ == "__main__":
    main()