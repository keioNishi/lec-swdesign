"""
クライアント・サーバモデルの基本実装
TCP/IPソケットプログラミングの基礎
"""

import socket
import threading
import time

# TCP/IPサーバーの簡単な実装
class SimpleServer:
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
        self.running = False

    def start_server(self):
        """TCP/IPサーバーの開始"""
        try:
            # TCPソケットを作成
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.host, self.port))
            server_socket.listen(1)

            print(f"サーバが開始されました。接続を待機中... {self.host}:{self.port}")
            self.running = True

            # クライアントからの接続を待機
            while self.running:
                try:
                    server_socket.settimeout(1.0)
                    client_socket, addr = server_socket.accept()
                    print(f"クライアント {addr} が接続しました")

                    # データを受信してレスポンスを送信
                    data = client_socket.recv(1024).decode('utf-8')
                    print(f"受信: {data}")

                    response = "Hello from server!"
                    client_socket.send(response.encode('utf-8'))
                    client_socket.close()

                except socket.timeout:
                    continue
                except OSError:
                    break

        except Exception as e:
            print(f"サーバエラー: {e}")
        finally:
            server_socket.close()
            print("サーバが停止しました")

    def stop_server(self):
        """サーバの停止"""
        self.running = False

# TCP/IPクライアントの簡単な実装
class SimpleClient:
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port

    def connect_to_server(self, message="Hello from client!"):
        """サーバへの接続とデータ送信"""
        try:
            # TCPソケットでサーバに接続
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.host, self.port))

            # メッセージを送信してレスポンスを受信
            client_socket.send(message.encode('utf-8'))
            response = client_socket.recv(1024).decode('utf-8')
            print(f"サーバからの応答: {response}")

            client_socket.close()
            return True

        except Exception as e:
            print(f"クライアント接続エラー: {e}")
            return False

def demo_client_server():
    """クライアント・サーバデモ"""
    print("=== クライアント・サーバモデル デモ ===")

    # サーバーを別スレッドで起動
    server = SimpleServer()
    server_thread = threading.Thread(target=server.start_server)
    server_thread.daemon = True
    server_thread.start()

    # サーバーの起動を待つ
    time.sleep(0.5)

    client = SimpleClient()

    print("\n1. 基本的な接続テスト:")
    client.connect_to_server("Hello from client!")

    print("\n2. 異なるメッセージでの接続テスト:")
    client.connect_to_server("Custom message from client")

    print("\n3. 存在しないポートへの接続テスト:")
    client_fail = SimpleClient(port=9999)
    client_fail.connect_to_server("This should fail")

    server.stop_server()
    print("\n=== デモ完了 ===")

if __name__ == "__main__":
    demo_client_server()
