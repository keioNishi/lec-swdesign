"""
DNS (Domain Name System) の基礎と名前解決

DNS とは：
- ドメイン名とIPアドレスを相互変換するシステム
- インターネットの電話帳のような役割
- 階層構造（ルート → TLD → 二次ドメイン → サブドメイン）
- 分散データベースシステム
"""

import socket
import struct
import random
import time
from urllib.parse import urlparse


class DNSResolver:
    """シンプルなDNS解決クラス（学習用）"""

    def __init__(self):
        # パブリックDNSサーバー
        self.dns_servers = [
            "8.8.8.8",        # Google DNS
            "8.8.4.4",        # Google DNS (Secondary)
            "1.1.1.1",        # Cloudflare DNS
            "208.67.222.222", # OpenDNS
        ]
        self.default_dns = "8.8.8.8"

    def resolve_hostname(self, hostname):
        """ホスト名をIPアドレスに解決（標準ライブラリ使用）"""
        print(f"=== ホスト名解決: {hostname} ===")

        try:
            # 基本的な名前解決
            ip_address = socket.gethostbyname(hostname)
            print(f"✓ {hostname} → {ip_address}")

            # 詳細情報を取得
            host_info = socket.gethostbyname_ex(hostname)
            hostname_canonical = host_info[0]
            aliases = host_info[1]
            ip_addresses = host_info[2]

            print(f"正式ホスト名: {hostname_canonical}")
            if aliases:
                print(f"エイリアス: {', '.join(aliases)}")
            print(f"IPアドレス一覧: {', '.join(ip_addresses)}")

            return ip_addresses

        except socket.gaierror as e:
            print(f"✗ 名前解決エラー: {e}")
            return None
        except Exception as e:
            print(f"✗ 予期しないエラー: {e}")
            return None

    def reverse_dns_lookup(self, ip_address):
        """IPアドレスからホスト名を逆引き"""
        print(f"\\n=== 逆引き DNS: {ip_address} ===")

        try:
            # 逆引き名前解決
            hostname = socket.gethostbyaddr(ip_address)
            print(f"✓ {ip_address} → {hostname[0]}")

            # 詳細情報
            canonical_name = hostname[0]
            aliases = hostname[1]
            addresses = hostname[2]

            print(f"正式ホスト名: {canonical_name}")
            if aliases:
                print(f"エイリアス: {', '.join(aliases)}")
            print(f"IPアドレス: {', '.join(addresses)}")

            return canonical_name

        except socket.herror as e:
            print(f"✗ 逆引きエラー: {e}")
            return None
        except Exception as e:
            print(f"✗ 予期しないエラー: {e}")
            return None

    def get_address_info(self, hostname, port=80):
        """アドレス情報の詳細取得"""
        print(f"\\n=== アドレス情報取得: {hostname}:{port} ===")

        try:
            # getaddrinfo を使用して詳細情報を取得
            addr_info = socket.getaddrinfo(hostname, port)

            print(f"アドレス情報の数: {len(addr_info)}")

            for i, (family, socktype, proto, canonname, sockaddr) in enumerate(addr_info):
                print(f"\\n情報 {i + 1}:")
                print(f"  アドレスファミリー: {self.get_family_name(family)}")
                print(f"  ソケットタイプ: {self.get_socktype_name(socktype)}")
                print(f"  プロトコル: {proto}")
                print(f"  正式名: {canonname}")
                print(f"  ソケットアドレス: {sockaddr}")

            return addr_info

        except socket.gaierror as e:
            print(f"✗ アドレス情報取得エラー: {e}")
            return None

    def get_family_name(self, family):
        """アドレスファミリー名を取得"""
        family_names = {
            socket.AF_INET: "IPv4 (AF_INET)",
            socket.AF_INET6: "IPv6 (AF_INET6)",
        }
        return family_names.get(family, f"Unknown ({family})")

    def get_socktype_name(self, socktype):
        """ソケットタイプ名を取得"""
        socktype_names = {
            socket.SOCK_STREAM: "TCP (SOCK_STREAM)",
            socket.SOCK_DGRAM: "UDP (SOCK_DGRAM)",
        }
        return socktype_names.get(socktype, f"Unknown ({socktype})")

    def test_dns_servers(self):
        """複数のDNSサーバーのテスト"""
        print("\\n=== DNSサーバーテスト ===")

        test_hostname = "google.com"

        for dns_server in self.dns_servers:
            print(f"\\nDNSサーバー: {dns_server}")

            try:
                # DNS サーバーに直接接続はできないが、
                # システムのDNS設定を確認
                start_time = time.time()
                result = socket.gethostbyname(test_hostname)
                end_time = time.time()

                response_time = (end_time - start_time) * 1000  # ミリ秒

                print(f"  テストホスト: {test_hostname}")
                print(f"  解決結果: {result}")
                print(f"  応答時間: {response_time:.2f} ms")

            except Exception as e:
                print(f"  ✗ エラー: {e}")

    def analyze_url(self, url):
        """URLからホスト名を抽出して解析"""
        print(f"\\n=== URL解析: {url} ===")

        try:
            # URLを解析
            parsed_url = urlparse(url)

            hostname = parsed_url.hostname
            port = parsed_url.port
            scheme = parsed_url.scheme

            print(f"スキーム: {scheme}")
            print(f"ホスト名: {hostname}")
            print(f"ポート: {port}")

            if hostname:
                # ホスト名を解決
                self.resolve_hostname(hostname)

                # デフォルトポートを設定
                if not port:
                    if scheme == 'http':
                        port = 80
                    elif scheme == 'https':
                        port = 443
                    elif scheme == 'ftp':
                        port = 21

                if port:
                    # アドレス情報を取得
                    self.get_address_info(hostname, port)

        except Exception as e:
            print(f"✗ URL解析エラー: {e}")

    def create_simple_dns_query(self, domain):
        """簡単なDNSクエリパケットを作成（教育目的）"""
        print(f"\\n=== DNS クエリパケット作成: {domain} ===")

        try:
            # DNS ヘッダー（12バイト）
            query_id = random.randint(1, 65535)  # クエリID
            flags = 0x0100  # 標準クエリ（再帰要求あり）
            questions = 1   # 質問セクションの数
            answer_rrs = 0  # 回答セクションの数
            auth_rrs = 0    # 権威セクションの数
            additional_rrs = 0  # 追加セクションの数

            # ヘッダーをバイナリ形式でパック
            header = struct.pack('!HHHHHH',
                                 query_id, flags, questions,
                                 answer_rrs, auth_rrs, additional_rrs)

            # 質問セクション
            question = b''

            # ドメイン名をDNS形式に変換
            # 例: "google.com" → "\\x06google\\x03com\\x00"
            for part in domain.split('.'):
                question += bytes([len(part)]) + part.encode('ascii')
            question += b'\\x00'  # 終端

            # クエリタイプ（A レコード = 1）とクラス（IN = 1）
            question += struct.pack('!HH', 1, 1)

            # 完全なクエリパケット
            dns_query = header + question

            print(f"クエリID: {query_id}")
            print(f"ドメイン: {domain}")
            print(f"パケットサイズ: {len(dns_query)} bytes")
            print(f"ヘッダー: {header.hex()}")
            print(f"質問部: {question.hex()}")

            return dns_query

        except Exception as e:
            print(f"✗ DNSクエリ作成エラー: {e}")
            return None

    def get_local_dns_info(self):
        """ローカルDNS設定情報を表示"""
        print("\\n=== ローカルDNS情報 ===")

        try:
            # ローカルホスト情報
            hostname = socket.gethostname()
            fqdn = socket.getfqdn()

            print(f"ローカルホスト名: {hostname}")
            print(f"完全修飾ドメイン名 (FQDN): {fqdn}")

            # ローカルIPアドレス
            local_ip = socket.gethostbyname(hostname)
            print(f"ローカルIP: {local_ip}")

            # ネットワークインターフェース情報（簡易版）
            print("\\n利用可能なアドレス:")
            test_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            test_socket.connect(("8.8.8.8", 80))
            local_address = test_socket.getsockname()[0]
            test_socket.close()
            print(f"外部接続用アドレス: {local_address}")

        except Exception as e:
            print(f"✗ ローカル情報取得エラー: {e}")


def main():
    """メインデモ関数"""
    print("DNS (Domain Name System) 基礎デモ")
    print("=" * 50)

    resolver = DNSResolver()

    # 1. 基本的なホスト名解決
    test_domains = [
        "google.com",
        "github.com",
        "stackoverflow.com",
        "localhost"
    ]

    for domain in test_domains:
        resolver.resolve_hostname(domain)

    # 2. 逆引きDNS
    test_ips = [
        "8.8.8.8",       # Google DNS
        "1.1.1.1",       # Cloudflare DNS
        "127.0.0.1"      # localhost
    ]

    for ip in test_ips:
        resolver.reverse_dns_lookup(ip)

    # 3. 詳細なアドレス情報取得
    resolver.get_address_info("google.com", 80)
    resolver.get_address_info("google.com", 443)

    # 4. URL解析
    test_urls = [
        "https://www.google.com",
        "http://github.com:80",
        "ftp://ftp.example.com"
    ]

    for url in test_urls:
        resolver.analyze_url(url)

    # 5. DNSサーバーテスト
    resolver.test_dns_servers()

    # 6. DNS クエリパケット作成（教育目的）
    resolver.create_simple_dns_query("example.com")

    # 7. ローカルDNS情報
    resolver.get_local_dns_info()

    print("\\n" + "=" * 50)
    print("DNS デモ完了")
    print("\\n学習ポイント:")
    print("- DNSは階層構造の分散データベース")
    print("- キャッシュによる高速化が重要")
    print("- セキュリティ（DNS over HTTPS, DNS over TLS）も重要")


if __name__ == "__main__":
    main()