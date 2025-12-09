"""
Webスクレイピングの基礎とHTTPクライアント実装

Webスクレイピングとは：
- Webサイトからデータを自動取得する技術
- HTTPリクエストを送信してHTMLを解析
- robots.txt の遵守とレート制限が重要
- 著作権と利用規約の遵守が必須
"""

import socket
import re
import time
import json
from urllib.parse import urljoin, urlparse
from html.parser import HTMLParser


class SimpleHTTPClient:
    """シンプルなHTTPクライアント（学習用）"""

    def __init__(self):
        self.user_agent = "Simple-HTTP-Client/1.0 (Educational Purpose)"
        self.timeout = 30

    def send_http_request(self, url, method='GET', headers=None, data=None):
        """HTTPリクエストを送信してレスポンスを取得"""
        print(f"=== HTTP リクエスト送信: {url} ===")

        try:
            # URLを解析
            parsed_url = urlparse(url)
            host = parsed_url.hostname
            port = parsed_url.port
            path = parsed_url.path if parsed_url.path else '/'

            # クエリパラメータがある場合は追加
            if parsed_url.query:
                path += '?' + parsed_url.query

            # デフォルトポートを設定
            if not port:
                if parsed_url.scheme == 'https':
                    port = 443
                else:
                    port = 80

            print(f"接続先: {host}:{port}")
            print(f"パス: {path}")

            # HTTPリクエストを構築
            request_lines = [
                f"{method} {path} HTTP/1.1",
                f"Host: {host}",
                f"User-Agent: {self.user_agent}",
                "Connection: close"
            ]

            # 追加ヘッダー
            if headers:
                for key, value in headers.items():
                    request_lines.append(f"{key}: {value}")

            # リクエストボディがある場合
            if data:
                request_lines.append(f"Content-Length: {len(data)}")
                request_lines.append("")  # 空行
                request_lines.append(data)
            else:
                request_lines.append("")  # 空行

            request = "\\r\\n".join(request_lines)

            # ソケット接続（HTTPSは非対応、学習目的のため）
            if parsed_url.scheme == 'https':
                print("注意: HTTPS接続はこの実装では対応していません")
                print("実際の実装ではSSL/TLSライブラリが必要です")
                return None

            # TCP接続を確立
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            sock.connect((host, port))

            # リクエストを送信
            sock.send(request.encode('utf-8'))

            # レスポンスを受信
            response_data = b""
            while True:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                response_data += chunk

            sock.close()

            # レスポンスをデコード
            response = response_data.decode('utf-8', errors='ignore')
            print(f"✓ レスポンス受信完了: {len(response)} 文字")

            return self.parse_http_response(response)

        except Exception as e:
            print(f"✗ HTTPリクエストエラー: {e}")
            return None

    def parse_http_response(self, response):
        """HTTPレスポンスを解析"""
        print("\\n--- HTTPレスポンス解析 ---")

        try:
            # ヘッダーとボディを分離
            header_end = response.find("\\r\\n\\r\\n")
            if header_end == -1:
                header_end = response.find("\\n\\n")
                if header_end == -1:
                    print("✗ 無効なHTTPレスポンス")
                    return None

            headers_section = response[:header_end]
            body = response[header_end + 4:]  # \\r\\n\\r\\n をスキップ

            # ステータス行を解析
            header_lines = headers_section.split('\\n')
            status_line = header_lines[0].strip()

            # ステータスコードを抽出
            status_parts = status_line.split(' ', 2)
            if len(status_parts) >= 2:
                status_code = status_parts[1]
                status_message = status_parts[2] if len(status_parts) > 2 else ""
            else:
                status_code = "Unknown"
                status_message = ""

            print(f"ステータス: {status_code} {status_message}")

            # ヘッダーを解析
            headers = {}
            for line in header_lines[1:]:
                line = line.strip()
                if ':' in line:
                    key, value = line.split(':', 1)
                    headers[key.strip().lower()] = value.strip()

            # 重要なヘッダー情報を表示
            content_type = headers.get('content-type', 'unknown')
            content_length = headers.get('content-length', 'unknown')

            print(f"Content-Type: {content_type}")
            print(f"Content-Length: {content_length}")
            print(f"本文サイズ: {len(body)} 文字")

            return {
                'status_code': status_code,
                'status_message': status_message,
                'headers': headers,
                'body': body
            }

        except Exception as e:
            print(f"✗ レスポンス解析エラー: {e}")
            return None


class SimpleHTMLParser(HTMLParser):
    """シンプルなHTMLパーサー（学習用）"""

    def __init__(self):
        super().__init__()
        self.title = ""
        self.links = []
        self.text_content = []
        self.images = []
        self.current_tag = None
        self.in_title = False

    def handle_starttag(self, tag, attrs):
        """開始タグの処理"""
        self.current_tag = tag

        if tag == 'title':
            self.in_title = True

        elif tag == 'a':
            # リンクを抽出
            for attr_name, attr_value in attrs:
                if attr_name == 'href':
                    self.links.append({
                        'url': attr_value,
                        'tag': tag
                    })

        elif tag == 'img':
            # 画像を抽出
            src = ""
            alt = ""
            for attr_name, attr_value in attrs:
                if attr_name == 'src':
                    src = attr_value
                elif attr_name == 'alt':
                    alt = attr_value

            if src:
                self.images.append({
                    'src': src,
                    'alt': alt
                })

    def handle_endtag(self, tag):
        """終了タグの処理"""
        if tag == 'title':
            self.in_title = False
        self.current_tag = None

    def handle_data(self, data):
        """テキストデータの処理"""
        data = data.strip()
        if data:
            if self.in_title:
                self.title += data
            else:
                # スクリプトやスタイルタグ内のテキストは除外
                if self.current_tag not in ['script', 'style']:
                    self.text_content.append(data)


class WebScraper:
    """Webスクレイピング クラス"""

    def __init__(self):
        self.http_client = SimpleHTTPClient()
        self.request_delay = 1  # リクエスト間の遅延（秒）

    def scrape_website(self, url):
        """Webサイトをスクレイピング"""
        print(f"=== Webスクレイピング開始: {url} ===")

        # robots.txt の確認（簡易版）
        self.check_robots_txt(url)

        # HTTPリクエストを送信
        response = self.http_client.send_http_request(url)

        if not response:
            print("✗ スクレイピング失敗")
            return None

        if response['status_code'] != '200':
            print(f"✗ HTTPエラー: {response['status_code']} {response['status_message']}")
            return None

        # HTMLを解析
        html_content = response['body']
        parsed_data = self.parse_html(html_content)

        # 結果を表示
        self.display_scraped_data(parsed_data)

        return parsed_data

    def check_robots_txt(self, url):
        """robots.txt の確認（簡易版）"""
        print("\\n--- robots.txt 確認 ---")

        try:
            parsed_url = urlparse(url)
            robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"

            print(f"robots.txt URL: {robots_url}")
            print("注意: 実際のスクレイピングでは robots.txt の内容を確認し、遵守してください")

            # 実際の実装では robots.txt を取得して解析
            # この例では教育目的のため省略

        except Exception as e:
            print(f"robots.txt 確認エラー: {e}")

    def parse_html(self, html_content):
        """HTMLコンテンツを解析"""
        print("\\n--- HTML解析 ---")

        # カスタムHTMLパーサーを使用
        parser = SimpleHTMLParser()
        parser.feed(html_content)

        # 解析結果をまとめる
        parsed_data = {
            'title': parser.title,
            'links': parser.links,
            'images': parser.images,
            'text_content': parser.text_content[:10],  # 最初の10個のテキスト要素
            'total_text_elements': len(parser.text_content)
        }

        return parsed_data

    def display_scraped_data(self, parsed_data):
        """スクレイピング結果を表示"""
        print("\\n=== スクレイピング結果 ===")

        print(f"タイトル: {parsed_data['title']}")
        print(f"リンク数: {len(parsed_data['links'])}")
        print(f"画像数: {len(parsed_data['images'])}")
        print(f"テキスト要素数: {parsed_data['total_text_elements']}")

        # リンク情報を表示
        if parsed_data['links']:
            print("\\n--- リンク（最初の5個）---")
            for i, link in enumerate(parsed_data['links'][:5]):
                print(f"{i+1}. {link['url']}")

        # 画像情報を表示
        if parsed_data['images']:
            print("\\n--- 画像（最初の5個）---")
            for i, img in enumerate(parsed_data['images'][:5]):
                print(f"{i+1}. {img['src']} (alt: {img['alt']})")

        # テキスト内容を表示
        if parsed_data['text_content']:
            print("\\n--- テキスト内容（抜粋）---")
            for i, text in enumerate(parsed_data['text_content'][:5]):
                if len(text) > 50:
                    text = text[:50] + "..."
                print(f"{i+1}. {text}")

    def extract_data_with_regex(self, html_content):
        """正規表現を使用したデータ抽出"""
        print("\\n=== 正規表現によるデータ抽出 ===")

        # メールアドレスを抽出
        email_pattern = r'\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b'
        emails = re.findall(email_pattern, html_content)

        # 電話番号を抽出（簡易パターン）
        phone_pattern = r'\\b\\d{3}-\\d{4}-\\d{4}\\b|\\b\\d{3}\\s\\d{4}\\s\\d{4}\\b'
        phones = re.findall(phone_pattern, html_content)

        # URLを抽出
        url_pattern = r'https?://[\\w\\.-]+\\.[a-zA-Z]{2,}[\\w\\.-]*/?[\\w\\.-]*'
        urls = re.findall(url_pattern, html_content)

        print(f"メールアドレス: {len(emails)} 個発見")
        for email in emails[:5]:  # 最初の5個を表示
            print(f"  - {email}")

        print(f"\\n電話番号: {len(phones)} 個発見")
        for phone in phones[:5]:
            print(f"  - {phone}")

        print(f"\\nURL: {len(urls)} 個発見")
        for url in urls[:5]:
            print(f"  - {url}")

        return {
            'emails': emails,
            'phones': phones,
            'urls': urls
        }

    def save_scraped_data(self, data, filename):
        """スクレイピングデータをファイルに保存"""
        print(f"\\n=== データ保存: {filename} ===")

        try:
            # JSONファイルとして保存
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            print(f"✓ データを {filename} に保存しました")

        except Exception as e:
            print(f"✗ ファイル保存エラー: {e}")


def demo_web_scraping():
    """Webスクレイピングのデモンストレーション"""
    print("Webスクレイピング基礎デモ")
    print("=" * 50)

    scraper = WebScraper()

    # 注意: 実際のWebサイトではなく、教育目的のデモ
    print("注意: このデモは教育目的です。")
    print("実際のスクレイピングでは以下を遵守してください:")
    print("1. robots.txt の確認と遵守")
    print("2. リクエスト頻度の制限")
    print("3. 利用規約の確認")
    print("4. 著作権の尊重")
    print("5. サーバーへの負荷配慮")

    # サンプルHTMLでのデモ
    sample_html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>サンプルWebページ</title>
    </head>
    <body>
        <h1>ウェルカム</h1>
        <p>これはサンプルページです。</p>
        <a href="https://example.com">外部リンク</a>
        <a href="/internal">内部リンク</a>
        <img src="/image1.jpg" alt="サンプル画像1">
        <img src="/image2.png" alt="サンプル画像2">
        <p>連絡先: contact@example.com</p>
        <p>電話: 03-1234-5678</p>
        <script>console.log("JavaScript code");</script>
    </body>
    </html>
    '''

    print("\\n=== サンプルHTMLでのデモ ===")

    # HTMLを解析
    parsed_data = scraper.parse_html(sample_html)
    scraper.display_scraped_data(parsed_data)

    # 正規表現での抽出
    regex_data = scraper.extract_data_with_regex(sample_html)

    # データを保存（仮想）
    all_data = {
        'parsed_data': parsed_data,
        'regex_data': regex_data,
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    }

    scraper.save_scraped_data(all_data, 'scraped_data.json')

    print("\\n" + "=" * 50)
    print("Webスクレイピングデモ完了")
    print("\\n重要な注意事項:")
    print("- 必ず robots.txt を確認してください")
    print("- サイトの利用規約を遵守してください")
    print("- 適切なレート制限を設けてください")
    print("- 個人情報の取り扱いに注意してください")


if __name__ == "__main__":
    demo_web_scraping()