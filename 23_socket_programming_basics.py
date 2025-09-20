"""
ソケットプログラミングの基礎
TCP/UDPソケットの基本的な使い方と実装例

ソケット（Socket）とは：
- ネットワーク上でデータ通信を行うためのエンドポイント
- プロセス間通信の一種で、異なるマシン間でも通信可能
"""

import socket
import threading
import time


class BasicSocketDemo:
    """基本的なソケット通信のデモンストレーション"""

    def __init__(self):
        self.host = 'localhost'  # ローカルホスト（自分のマシン）
        self.tcp_port = 8001     # TCP用ポート番号
        self.udp_port = 8002     # UDP用ポート番号

    def create_tcp_socket(self):
        """TCP ソケットの作成と基本設定"""
        print("=== TCP ソケットの作成 ===")

        # TCP ソケットを作成（AF_INET=IPv4, SOCK_STREAM=TCP）
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("TCP ソケットが作成されました")

        # ソケット情報を表示
        print(f"ソケットタイプ: {tcp_socket.type}")
        print(f"ソケットファミリー: {tcp_socket.family}")

        tcp_socket.close()
        print("TCP ソケットを閉じました\n")

    def create_udp_socket(self):
        """UDP ソケットの作成と基本設定"""
        print("=== UDP ソケットの作成 ===")

        # UDP ソケットを作成（AF_INET=IPv4, SOCK_DGRAM=UDP）
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("UDP ソケットが作成されました")

        # ソケット情報を表示
        print(f"ソケットタイプ: {udp_socket.type}")
        print(f"ソケットファミリー: {udp_socket.family}")

        udp_socket.close()
        print("UDP ソケットを閉じました\n")

    def tcp_server_demo(self):
        """簡単なTCPサーバーのデモ"""
        print("=== TCP サーバーデモ ===")

        try:
            # サーバーソケットを作成してバインド
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.host, self.tcp_port))
            server_socket.listen(1)  # 接続待ちキューの最大サイズ

            print(f"TCPサーバーが {self.host}:{self.tcp_port} で待機中...")

            # タイムアウトを設定して一定時間待機
            server_socket.settimeout(2.0)

            try:
                client_socket, client_address = server_socket.accept()
                print(f"クライアント {client_address} から接続されました")

                # データを受信
                data = client_socket.recv(1024)  # 最大1024バイト受信
                print(f"受信データ: {data.decode('utf-8')}")

                # レスポンスを送信
                response = "Hello from TCP Server!"
                client_socket.send(response.encode('utf-8'))

                client_socket.close()

            except socket.timeout:
                print("タイムアウト: クライアントからの接続がありませんでした")

        except Exception as e:
            print(f"TCPサーバーエラー: {e}")
        finally:
            server_socket.close()
            print("TCPサーバーを終了しました\n")

    def tcp_client_demo(self):
        """簡単なTCPクライアントのデモ"""
        print("=== TCP クライアントデモ ===")

        try:
            # クライアントソケットを作成
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # サーバーに接続
            client_socket.connect((self.host, self.tcp_port))
            print(f"TCPサーバー {self.host}:{self.tcp_port} に接続しました")

            # データを送信
            message = "Hello from TCP Client!"
            client_socket.send(message.encode('utf-8'))
            print(f"送信データ: {message}")

            # レスポンスを受信
            response = client_socket.recv(1024)
            print(f"受信データ: {response.decode('utf-8')}")

        except Exception as e:
            print(f"TCPクライアントエラー: {e}")
        finally:
            client_socket.close()
            print("TCPクライアントを終了しました\n")

    def socket_info_demo(self):
        """ソケット情報の取得デモ"""
        print("=== ソケット情報の取得 ===")

        # ホスト情報を取得
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)

        print(f"ホスト名: {hostname}")
        print(f"ローカルIP: {local_ip}")

        # 外部サービスの情報を取得（例：Google DNS）
        try:
            google_ip = socket.gethostbyname('google.com')
            print(f"google.com のIP: {google_ip}")
        except Exception as e:
            print(f"外部ホスト名解決エラー: {e}")

        print()


def main():
    """メイン関数：各デモを実行"""
    print("ソケットプログラミング基礎デモ")
    print("=" * 40)

    demo = BasicSocketDemo()

    # 1. ソケット作成のデモ
    demo.create_tcp_socket()
    demo.create_udp_socket()

    # 2. ソケット情報の取得
    demo.socket_info_demo()

    # 3. TCP通信のデモ（サーバーを別スレッドで起動）
    print("TCP通信のデモを開始します...")

    # サーバーを別スレッドで起動
    server_thread = threading.Thread(target=demo.tcp_server_demo)
    server_thread.daemon = True
    server_thread.start()

    # サーバーの起動を少し待つ
    time.sleep(0.5)

    # クライアントを実行
    demo.tcp_client_demo()

    print("=" * 40)
    print("デモ完了")


if __name__ == "__main__":
    main()