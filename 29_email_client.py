"""
電子メール（Email）プロトコルの基礎とクライアント実装

電子メールプロトコル：
- SMTP (Simple Mail Transfer Protocol): メール送信用プロトコル
- POP3 (Post Office Protocol 3): メール受信用プロトコル（ダウンロード型）
- IMAP (Internet Message Access Protocol): メール受信用プロトコル（サーバー型）
"""

import smtplib
import poplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import base64
import os


class EmailClient:
    """シンプルな電子メールクライアント（学習用）"""

    def __init__(self):
        # デモ用の設定（実際の使用時は適切な設定に変更）
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.pop3_server = "pop.gmail.com"
        self.pop3_port = 995
        self.imap_server = "imap.gmail.com"
        self.imap_port = 993

    def create_simple_email(self, sender, recipient, subject, body):
        """シンプルなテキストメールを作成"""
        print("=== シンプルなメール作成 ===")

        # MIMETextオブジェクトを作成（テキストメール）
        message = MIMEText(body, 'plain', 'utf-8')
        message['From'] = sender
        message['To'] = recipient
        message['Subject'] = subject

        print(f"送信者: {sender}")
        print(f"受信者: {recipient}")
        print(f"件名: {subject}")
        print(f"本文: {body[:50]}...")

        # メールの内容を文字列として取得
        email_content = message.as_string()
        print(f"\\nメールサイズ: {len(email_content)} bytes")

        return message

    def create_html_email(self, sender, recipient, subject, html_body):
        """HTMLメールを作成"""
        print("\\n=== HTMLメール作成 ===")

        # マルチパートメッセージを作成
        message = MIMEMultipart('alternative')
        message['From'] = sender
        message['To'] = recipient
        message['Subject'] = subject

        # HTMLコンテンツを追加
        html_part = MIMEText(html_body, 'html', 'utf-8')
        message.attach(html_part)

        print(f"HTMLメールが作成されました")
        print(f"件名: {subject}")

        return message

    def create_multipart_email(self, sender, recipient, subject, text_body, html_body):
        """テキストとHTMLの両方を含むマルチパートメールを作成"""
        print("\\n=== マルチパートメール作成 ===")

        # マルチパートメッセージを作成
        message = MIMEMultipart('alternative')
        message['From'] = sender
        message['To'] = recipient
        message['Subject'] = subject

        # テキスト版を追加
        text_part = MIMEText(text_body, 'plain', 'utf-8')
        message.attach(text_part)

        # HTML版を追加
        html_part = MIMEText(html_body, 'html', 'utf-8')
        message.attach(html_part)

        print(f"マルチパートメールが作成されました")
        print(f"テキスト部分: {len(text_body)} 文字")
        print(f"HTML部分: {len(html_body)} 文字")

        return message

    def add_attachment(self, message, file_path):
        """メールに添付ファイルを追加（仮想的な実装）"""
        print(f"\\n=== 添付ファイル追加（仮想）===")

        # 実際のファイルがない場合はダミーデータを作成
        if not os.path.exists(file_path):
            # ダミーテキストファイルの内容を作成
            dummy_content = "これは添付ファイルのダミーデータです。\\n実際の実装では、実在するファイルを使用します。"
            file_data = dummy_content.encode('utf-8')
            filename = os.path.basename(file_path)
        else:
            # 実際のファイルを読み込み
            with open(file_path, 'rb') as f:
                file_data = f.read()
            filename = os.path.basename(file_path)

        # 添付ファイル部分を作成
        attachment = MIMEBase('application', 'octet-stream')
        attachment.set_payload(file_data)
        encoders.encode_base64(attachment)

        # ヘッダーを設定
        attachment.add_header(
            'Content-Disposition',
            f'attachment; filename= {filename}'
        )

        # メッセージに添付
        if hasattr(message, 'attach'):
            message.attach(attachment)
        else:
            # シンプルなメッセージの場合、マルチパートに変換
            multipart_message = MIMEMultipart()
            multipart_message['From'] = message['From']
            multipart_message['To'] = message['To']
            multipart_message['Subject'] = message['Subject']
            multipart_message.attach(message)
            multipart_message.attach(attachment)
            message = multipart_message

        print(f"添付ファイル '{filename}' を追加しました")
        print(f"ファイルサイズ: {len(file_data)} bytes")

        return message

    def simulate_smtp_send(self, message):
        """SMTP送信のシミュレーション（実際には送信しない）"""
        print("\\n=== SMTP送信シミュレーション ===")

        try:
            # メール内容を表示
            email_content = message.as_string()

            print("--- メールヘッダー ---")
            print(f"From: {message['From']}")
            print(f"To: {message['To']}")
            print(f"Subject: {message['Subject']}")
            print(f"Date: {message.get('Date', 'Not set')}")

            print("\\n--- メール本文（最初の200文字）---")
            body_start = email_content.find('\\r\\n\\r\\n')
            if body_start != -1:
                body = email_content[body_start + 4:body_start + 204]
                print(body + "..." if len(body) == 200 else body)

            print(f"\\n総メールサイズ: {len(email_content)} bytes")
            print("✓ メール送信シミュレーション完了")

            return True

        except Exception as e:
            print(f"✗ 送信エラー: {e}")
            return False

    def simulate_pop3_receive(self):
        """POP3受信のシミュレーション"""
        print("\\n=== POP3受信シミュレーション ===")

        # ダミーメールデータを作成
        dummy_emails = [
            {
                'from': 'sender1@example.com',
                'subject': 'テストメール1',
                'body': 'これは最初のテストメールです。',
                'date': '2024-03-15 10:00:00'
            },
            {
                'from': 'sender2@example.com',
                'subject': '重要な連絡',
                'body': 'こちらは重要な連絡事項です。確認してください。',
                'date': '2024-03-15 11:30:00'
            },
            {
                'from': 'newsletter@example.com',
                'subject': 'ニュースレター',
                'body': '今月のニュースレターをお送りします。',
                'date': '2024-03-15 09:15:00'
            }
        ]

        print(f"受信メール数: {len(dummy_emails)}")
        print("\\n--- 受信メール一覧 ---")

        for i, mail in enumerate(dummy_emails, 1):
            print(f"\\nメール {i}:")
            print(f"  差出人: {mail['from']}")
            print(f"  件名: {mail['subject']}")
            print(f"  日時: {mail['date']}")
            print(f"  本文: {mail['body'][:30]}...")

        return dummy_emails

    def parse_email_headers(self, email_content):
        """メールヘッダーの解析デモ"""
        print("\\n=== メールヘッダー解析 ===")

        # サンプルメールを作成
        sample_email = """From: sender@example.com
To: recipient@example.com
Subject: =?UTF-8?B?44OG44K544OI44Oh44O844Or?=
Date: Fri, 15 Mar 2024 10:00:00 +0900
Message-ID: <12345@example.com>
Content-Type: text/plain; charset=utf-8

これはサンプルメールの本文です。
日本語のテキストも含まれています。
"""

        # メールオブジェクトを作成
        msg = email.message_from_string(sample_email)

        print("--- 解析結果 ---")
        print(f"差出人: {msg['From']}")
        print(f"宛先: {msg['To']}")
        print(f"件名: {email.header.decode_header(msg['Subject'])[0][0]}")
        print(f"日付: {msg['Date']}")
        print(f"メッセージID: {msg['Message-ID']}")
        print(f"Content-Type: {msg['Content-Type']}")

        # メール本文を取得
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode('utf-8')
                    print(f"\\n本文:\\n{body}")
                    break
        else:
            body = msg.get_payload(decode=True).decode('utf-8')
            print(f"\\n本文:\\n{body}")


def main():
    """メインデモ関数"""
    print("電子メールプロトコル基礎デモ")
    print("=" * 40)

    client = EmailClient()

    # 1. シンプルなテキストメール作成
    simple_mail = client.create_simple_email(
        sender="test@example.com",
        recipient="recipient@example.com",
        subject="テストメール",
        body="これはテストメールの本文です。\\n改行も含まれています。"
    )

    # 2. HTMLメール作成
    html_body = """
    <html>
    <body>
        <h1>HTMLメールのテスト</h1>
        <p>これは<strong>HTML形式</strong>のメールです。</p>
        <ul>
            <li>リスト項目1</li>
            <li>リスト項目2</li>
        </ul>
    </body>
    </html>
    """

    html_mail = client.create_html_email(
        sender="test@example.com",
        recipient="recipient@example.com",
        subject="HTMLテストメール",
        html_body=html_body
    )

    # 3. マルチパートメール作成
    text_body = "これはテキスト版のメールです。"
    multipart_mail = client.create_multipart_email(
        sender="test@example.com",
        recipient="recipient@example.com",
        subject="マルチパートテスト",
        text_body=text_body,
        html_body=html_body
    )

    # 4. 添付ファイル付きメール（仮想）
    attachment_mail = client.add_attachment(simple_mail, "dummy_file.txt")

    # 5. SMTP送信シミュレーション
    client.simulate_smtp_send(multipart_mail)

    # 6. POP3受信シミュレーション
    received_emails = client.simulate_pop3_receive()

    # 7. メールヘッダー解析
    client.parse_email_headers("")

    print("\\n" + "=" * 40)
    print("電子メールデモ完了")
    print("\\n注意: このデモは学習目的のシミュレーションです。")
    print("実際のメール送受信には適切な認証情報とセキュリティ設定が必要です。")


if __name__ == "__main__":
    main()