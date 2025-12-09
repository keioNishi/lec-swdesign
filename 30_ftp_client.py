"""
FTP (File Transfer Protocol) の基礎とクライアント実装

FTP とは：
- ファイル転送プロトコル
- クライアント・サーバー型のファイル共有システム
- コマンドポート（通常21番）とデータポート（通常20番）を使用
- アクティブモードとパッシブモードがある
"""

import socket
import os
import threading
import time
from datetime import datetime


class SimpleFTPClient:
    """シンプルなFTPクライアント（学習用実装）"""

    def __init__(self):
        self.control_socket = None
        self.connected = False
        self.current_directory = "/"
        self.passive_mode = True  # パッシブモード使用

    def connect(self, host, port=21):
        """FTPサーバーに接続"""
        print(f"=== FTPサーバーに接続: {host}:{port} ===")

        try:
            # コントロール接続を確立
            self.control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.control_socket.settimeout(30)
            self.control_socket.connect((host, port))

            # サーバーからの応答を受信
            response = self.receive_response()
            print(f"サーバー応答: {response}")

            if response.startswith('220'):
                self.connected = True
                print("✓ 接続成功")
                return True
            else:
                print("✗ 接続失敗")
                return False

        except Exception as e:
            print(f"✗ 接続エラー: {e}")
            return False

    def send_command(self, command):
        """FTPコマンドを送信"""
        if not self.connected or not self.control_socket:
            print("✗ サーバーに接続されていません")
            return None

        try:
            # コマンドを送信（CRLFで終端）
            full_command = command + "\\r\\n"
            self.control_socket.send(full_command.encode('ascii'))
            print(f"送信コマンド: {command}")

            # レスポンスを受信
            response = self.receive_response()
            print(f"サーバー応答: {response}")

            return response

        except Exception as e:
            print(f"✗ コマンド送信エラー: {e}")
            return None

    def receive_response(self):
        """サーバーからのレスポンスを受信"""
        try:
            response = ""
            while True:
                data = self.control_socket.recv(1024).decode('ascii', errors='ignore')
                response += data

                # 複数行レスポンスの処理
                lines = response.split('\\r\\n')
                if len(lines) >= 2 and lines[-2]:
                    # 最後の行が空でない場合、完全なレスポンスを受信
                    break

            return response.strip()

        except Exception as e:
            print(f"✗ レスポンス受信エラー: {e}")
            return ""

    def login(self, username="anonymous", password="anonymous@example.com"):
        """FTPサーバーにログイン"""
        print(f"\\n=== ログイン: {username} ===")

        # USERコマンドを送信
        response = self.send_command(f"USER {username}")
        if not response or not response.startswith('331'):
            print("✗ ユーザー名が受け入れられませんでした")
            return False

        # PASSコマンドを送信
        response = self.send_command(f"PASS {password}")
        if response and response.startswith('230'):
            print("✓ ログイン成功")
            return True
        else:
            print("✗ ログイン失敗")
            return False

    def pwd(self):
        """現在のディレクトリを取得（PWDコマンド）"""
        print("\\n=== 現在のディレクトリ取得 ===")
        response = self.send_command("PWD")

        if response and response.startswith('257'):
            # レスポンスからディレクトリパスを抽出
            # 例: 257 "/home/user" is current directory
            start = response.find('"')
            end = response.find('"', start + 1)
            if start != -1 and end != -1:
                directory = response[start + 1:end]
                self.current_directory = directory
                print(f"現在のディレクトリ: {directory}")
                return directory

        return None

    def list_directory(self):
        """ディレクトリの内容を一覧表示（LISTコマンド）"""
        print("\\n=== ディレクトリ一覧 ===")

        # パッシブモードでデータ接続を確立
        data_socket = self.enter_passive_mode()
        if not data_socket:
            return False

        # LISTコマンドを送信
        response = self.send_command("LIST")

        if response and (response.startswith('150') or response.startswith('125')):
            # データを受信
            directory_data = b""
            try:
                while True:
                    chunk = data_socket.recv(1024)
                    if not chunk:
                        break
                    directory_data += chunk

                # データ接続を閉じる
                data_socket.close()

                # 転送完了の応答を受信
                completion_response = self.receive_response()
                print(f"転送完了: {completion_response}")

                # ディレクトリ内容を表示
                if directory_data:
                    directory_listing = directory_data.decode('ascii', errors='ignore')
                    print("--- ディレクトリ内容 ---")
                    for line in directory_listing.split('\\n'):
                        if line.strip():
                            print(line.strip())
                    return True

            except Exception as e:
                print(f"✗ データ受信エラー: {e}")
                data_socket.close()

        return False

    def enter_passive_mode(self):
        """パッシブモードでデータ接続を確立"""
        print("パッシブモードでデータ接続を確立中...")

        # PASVコマンドを送信
        response = self.send_command("PASV")

        if response and response.startswith('227'):
            # レスポンスからIPアドレスとポート番号を抽出
            # 例: 227 Entering Passive Mode (192,168,1,1,20,21)
            start = response.find('(')
            end = response.find(')')
            if start != -1 and end != -1:
                params = response[start + 1:end].split(',')
                if len(params) == 6:
                    # IPアドレスを構築
                    ip = '.'.join(params[:4])
                    # ポート番号を計算（上位バイト * 256 + 下位バイト）
                    port = int(params[4]) * 256 + int(params[5])

                    print(f"データポート: {ip}:{port}")

                    # データ接続を確立
                    try:
                        data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        data_socket.settimeout(30)
                        data_socket.connect((ip, port))
                        print("✓ データ接続確立")
                        return data_socket

                    except Exception as e:
                        print(f"✗ データ接続エラー: {e}")

        return None

    def change_directory(self, directory):
        """ディレクトリを変更（CDコマンド）"""
        print(f"\\n=== ディレクトリ変更: {directory} ===")

        response = self.send_command(f"CWD {directory}")
        if response and response.startswith('250'):
            print(f"✓ ディレクトリ変更成功: {directory}")
            self.current_directory = directory
            return True
        else:
            print(f"✗ ディレクトリ変更失敗")
            return False

    def simulate_file_download(self, filename):
        """ファイルダウンロードのシミュレーション"""
        print(f"\\n=== ファイルダウンロード（シミュレーション）: {filename} ===")

        # パッシブモードでデータ接続を確立
        data_socket = self.enter_passive_mode()
        if not data_socket:
            return False

        # RETRコマンドを送信
        response = self.send_command(f"RETR {filename}")

        if response and (response.startswith('150') or response.startswith('125')):
            print(f"ダウンロード開始: {filename}")

            # ダミーデータを生成（実際の実装ではサーバーからデータを受信）
            dummy_data = f"これは {filename} のダミーデータです。\\n"
            dummy_data += f"ダウンロード日時: {datetime.now()}\\n"
            dummy_data += "実際の実装では、サーバーから実際のファイルデータを受信します。\\n"

            print(f"受信データ（サンプル）:\\n{dummy_data}")
            print(f"✓ ダウンロード完了: {len(dummy_data)} bytes")

            data_socket.close()

            # 転送完了の応答を受信
            completion_response = self.receive_response()
            print(f"転送完了: {completion_response}")

            return True

        else:
            print(f"✗ ファイルダウンロード失敗")
            data_socket.close()
            return False

    def quit(self):
        """FTP接続を終了"""
        print("\\n=== FTP接続終了 ===")

        if self.connected and self.control_socket:
            # QUITコマンドを送信
            response = self.send_command("QUIT")
            print(f"終了応答: {response}")

            # 接続を閉じる
            self.control_socket.close()
            self.connected = False
            print("✓ 接続を閉じました")

        else:
            print("接続されていません")


class SimpleFTPServer:
    """シンプルなFTPサーバー（デモ用）"""

    def __init__(self, host='localhost', port=2121):  # 非特権ポートを使用
        self.host = host
        self.port = port
        self.running = False
        self.current_dir = "/virtual_root"

    def start_server(self):
        """FTPサーバーを開始（簡易実装）"""
        print(f"=== FTPサーバー開始: {self.host}:{self.port} ===")

        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.host, self.port))
            server_socket.listen(1)

            print(f"FTPサーバーが {self.host}:{self.port} で待機中...")
            self.running = True

            # 簡単なFTPサーバーの実装（デモ用）
            server_socket.settimeout(5)

            try:
                client_socket, client_address = server_socket.accept()
                print(f"クライアント {client_address} が接続しました")

                # 接続応答を送信
                welcome_msg = "220 Simple FTP Server Ready\\r\\n"
                client_socket.send(welcome_msg.encode('ascii'))

                # 簡単なコマンド処理（デモ用）
                while self.running:
                    try:
                        client_socket.settimeout(2)
                        data = client_socket.recv(1024).decode('ascii', errors='ignore')
                        if not data:
                            break

                        command = data.strip()
                        print(f"受信コマンド: {command}")

                        # 簡単なコマンド応答
                        if command.startswith('USER'):
                            response = "331 Password required\\r\\n"
                        elif command.startswith('PASS'):
                            response = "230 Login successful\\r\\n"
                        elif command.startswith('PWD'):
                            response = f'257 "{self.current_dir}" is current directory\\r\\n'
                        elif command.startswith('QUIT'):
                            response = "221 Goodbye\\r\\n"
                            client_socket.send(response.encode('ascii'))
                            break
                        else:
                            response = "502 Command not implemented\\r\\n"

                        client_socket.send(response.encode('ascii'))

                    except socket.timeout:
                        continue

                client_socket.close()

            except socket.timeout:
                print("タイムアウト: クライアントからの接続がありませんでした")

        except Exception as e:
            print(f"FTPサーバーエラー: {e}")
        finally:
            server_socket.close()
            self.running = False
            print("FTPサーバーを停止しました")


def demo_ftp_client():
    """FTPクライアントのデモンストレーション"""
    print("FTP (File Transfer Protocol) 基礎デモ")
    print("=" * 50)

    # FTPサーバーを別スレッドで起動
    server = SimpleFTPServer()
    server_thread = threading.Thread(target=server.start_server)
    server_thread.daemon = True
    server_thread.start()

    # サーバーの起動を待機
    time.sleep(1)

    # FTPクライアントでテスト
    client = SimpleFTPClient()

    # 1. サーバーに接続
    if client.connect('localhost', 2121):
        # 2. ログイン
        if client.login('testuser', 'testpass'):
            # 3. 現在のディレクトリを取得
            client.pwd()

            # 4. ディレクトリ一覧（実際のサーバーでないので動作しない）
            print("\\n--- 注意: 以下は実際のFTPサーバーでのみ動作します ---")
            print("ディレクトリ一覧の取得は実際のFTPサーバーが必要です")

        # 5. 接続終了
        client.quit()

    # サーバーを停止
    server.running = False
    time.sleep(1)

    print("\\n" + "=" * 50)
    print("FTPデモ完了")
    print("\\n注意事項:")
    print("- このデモは学習目的の簡易実装です")
    print("- 実際のFTPサーバーとの通信には、より詳細な実装が必要です")
    print("- セキュリティ上の理由から、現在はSFTP（SSH File Transfer Protocol）の使用が推奨されます")


if __name__ == "__main__":
    demo_ftp_client()