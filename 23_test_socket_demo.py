# -*- coding: utf-8 -*-
"""
23番 ソケットプログラミング基礎のテスト実行ファイル
文字エンコーディング対応版
"""

import sys
import os

# Windowsでの日本語出力対応
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())

# メインのデモファイルをインポート
from socket_programming_basics_23 import BasicSocketDemo


def main():
    """テスト実行メイン関数"""
    print("Socket Programming Basic Demo - Test Runner")
    print("=" * 50)

    demo = BasicSocketDemo()

    try:
        # 1. ソケット作成のデモ
        print("\n1. TCP Socket Creation Test:")
        demo.create_tcp_socket()

        print("\n2. UDP Socket Creation Test:")
        demo.create_udp_socket()

        # 3. ソケット情報の取得
        print("\n3. Socket Information Test:")
        demo.socket_info_demo()

        print("\n4. TCP Communication Test:")
        print("Starting TCP server and client demo...")

        # TCP通信テスト（簡略版）
        import threading
        import time

        # サーバーを別スレッドで起動
        server_thread = threading.Thread(target=demo.tcp_server_demo)
        server_thread.daemon = True
        server_thread.start()

        # サーバー起動待機
        time.sleep(0.5)

        # クライアント実行
        demo.tcp_client_demo()

        print("\n" + "=" * 50)
        print("All tests completed successfully!")

    except Exception as e:
        print(f"Test error: {e}")
        return False

    return True


if __name__ == "__main__":
    success = main()
    if success:
        print("Test: PASSED")
    else:
        print("Test: FAILED")