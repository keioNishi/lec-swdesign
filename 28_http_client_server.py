"""
HTTP プロトコルの基礎とWebクライアント・サーバーの実装

HTTP（HyperText Transfer Protocol）とは：
- WebブラウザとWebサーバー間でデータを転送するためのプロトコル
- リクエスト・レスポンス型の通信方式
- ステートレス（状態を保持しない）プロトコル
"""

import socket
import threading
import time
from urllib.parse import urlparse
import json


class SimpleHTTPServer:
    """シンプルなHTTPサーバーの実装"""

    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
        self.running = False

    def create_http_response(self, status_code, content_type, body):
        """HTTP レスポンスを作成"""
        # HTTPステータスコードとメッセージのマッピング
        status_messages = {
            200: "OK",
            404: "Not Found",
            500: "Internal Server Error"
        }

        status_message = status_messages.get(status_code, "Unknown")

        # HTTPレスポンスヘッダーを構築
        response = f"HTTP/1.1 {status_code} {status_message}\\r\\n"
        response += f"Content-Type: {content_type}\\r\\n"
        response += f"Content-Length: {len(body.encode('utf-8'))}\\r\\n"
        response += f"Connection: close\\r\\n"
        response += "\\r\\n"  # ヘッダーとボディの区切り
        response += body

        return response.encode('utf-8')

    def handle_client(self, client_socket, client_address):
        """クライアントからのリクエストを処理"""
        try:
            # HTTPリクエストを受信
            request_data = client_socket.recv(1024).decode('utf-8')

            if not request_data:
                return

            print(f"\\n--- クライアント {client_address} からのリクエスト ---")
            print(request_data[:200] + "..." if len(request_data) > 200 else request_data)

            # リクエスト行を解析（例: "GET / HTTP/1.1"）
            request_lines = request_data.split('\\r\\n')
            if request_lines:
                request_line = request_lines[0]
                method, path, version = request_line.split(' ')

                print(f"メソッド: {method}, パス: {path}, バージョン: {version}")

                # 簡単なルーティング
                if path == '/' or path == '/index.html':
                    # ホームページ
                    html_content = self.create_homepage()
                    response = self.create_http_response(200, "text/html; charset=utf-8", html_content)

                elif path == '/api/data':
                    # JSON API エンドポイント
                    json_data = json.dumps({
                        "message": "Hello from HTTP Server!",
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "method": method
                    }, ensure_ascii=False)
                    response = self.create_http_response(200, "application/json; charset=utf-8", json_data)

                else:
                    # 404 Not Found
                    html_content = "<html><body><h1>404 Not Found</h1><p>ページが見つかりません</p></body></html>"
                    response = self.create_http_response(404, "text/html; charset=utf-8", html_content)

                # レスポンスを送信
                client_socket.send(response)

        except Exception as e:
            print(f"クライアント処理エラー: {e}")
            # エラーレスポンスを送信
            error_response = self.create_http_response(500, "text/plain", f"Internal Server Error: {str(e)}")
            client_socket.send(error_response)

        finally:
            client_socket.close()

    def create_homepage(self):
        """シンプルなHTMLホームページを作成"""
        html = """
        <!DOCTYPE html>
        <html lang="ja">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Simple HTTP Server</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                h1 { color: #333; }
                .info { background-color: #f0f0f0; padding: 20px; border-radius: 5px; }
            </style>
        </head>
        <body>
            <h1>Simple HTTP Server へようこそ</h1>
            <div class="info">
                <p>これはPythonで実装されたシンプルなHTTPサーバーです。</p>
                <p>現在時刻: """ + time.strftime("%Y-%m-%d %H:%M:%S") + """</p>
                <p><a href="/api/data">JSON API を試す</a></p>
            </div>
        </body>
        </html>
        """
        return html

    def start_server(self):
        """HTTPサーバーを開始"""
        try:
            # サーバーソケットを作成
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)  # 最大5つの接続を待機

            print(f"HTTPサーバーが開始されました: http://{self.host}:{self.port}")
            print("Ctrl+C で停止できます")

            self.running = True

            while self.running:
                try:
                    # クライアントからの接続を待機
                    client_socket, client_address = server_socket.accept()

                    # 各クライアントを別スレッドで処理
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, client_address)
                    )
                    client_thread.daemon = True
                    client_thread.start()

                except KeyboardInterrupt:
                    print("\\nサーバーを停止します...")
                    break
                except Exception as e:
                    print(f"サーバーエラー: {e}")

        except Exception as e:
            print(f"サーバー開始エラー: {e}")
        finally:
            server_socket.close()
            self.running = False
            print("HTTPサーバーが停止しました")


class SimpleHTTPClient:
    """シンプルなHTTPクライアントの実装"""

    def send_http_request(self, host, port, method='GET', path='/', headers=None):
        """HTTP リクエストを送信"""
        try:
            # クライアントソケットを作成
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(10)  # 10秒でタイムアウト

            # サーバーに接続
            client_socket.connect((host, port))

            # HTTPリクエストを構築
            request = f"{method} {path} HTTP/1.1\\r\\n"
            request += f"Host: {host}:{port}\\r\\n"
            request += "Connection: close\\r\\n"

            # 追加ヘッダーがある場合
            if headers:
                for key, value in headers.items():
                    request += f"{key}: {value}\\r\\n"

            request += "\\r\\n"  # ヘッダーとボディの区切り

            print(f"--- 送信するHTTPリクエスト ---")
            print(request)

            # リクエストを送信
            client_socket.send(request.encode('utf-8'))

            # レスポンスを受信
            response_data = b""
            while True:
                chunk = client_socket.recv(1024)
                if not chunk:
                    break
                response_data += chunk

            # レスポンスをデコード
            response = response_data.decode('utf-8', errors='ignore')

            print(f"--- 受信したHTTPレスポンス ---")
            print(response[:500] + "..." if len(response) > 500 else response)

            return response

        except Exception as e:
            print(f"HTTPクライアントエラー: {e}")
            return None
        finally:
            client_socket.close()


def demo_http_communication():
    """HTTP通信のデモンストレーション"""
    print("HTTP クライアント・サーバー通信デモ")
    print("=" * 50)

    # HTTPサーバーを別スレッドで起動
    server = SimpleHTTPServer()
    server_thread = threading.Thread(target=server.start_server)
    server_thread.daemon = True
    server_thread.start()

    # サーバーの起動を待機
    time.sleep(1)

    # HTTPクライアントでテスト
    client = SimpleHTTPClient()

    print("\\n1. ホームページへのGETリクエスト:")
    client.send_http_request('localhost', 8080, 'GET', '/')

    print("\\n2. JSON APIへのGETリクエスト:")
    client.send_http_request('localhost', 8080, 'GET', '/api/data')

    print("\\n3. 存在しないページへのリクエスト（404エラー）:")
    client.send_http_request('localhost', 8080, 'GET', '/nonexistent')

    # サーバーを停止
    server.running = False
    time.sleep(1)

    print("\\n" + "=" * 50)
    print("デモ完了")


if __name__ == "__main__":
    demo_http_communication()