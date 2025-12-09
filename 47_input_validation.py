"""
入力検証とセキュリティ脆弱性対策
XSS、SQLインジェクション攻撃の防止
"""

import re

# InputValidatorクラスの実装
class InputValidator:
    @staticmethod
    # メールアドレスの形式検証
    def validate_email(email):
        """メールアドレスの形式検証"""
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        return re.match(pattern, email) is not None

    @staticmethod
    # 危険な文字列のサニタイズ（XSS対策）
    def sanitize_input(user_input):
        """危険な文字列のサニタイズ（XSS対策）"""
        
        dangerous_chars = ['<', '>', '"', "'", ';', '&']
        
        sanitized = user_input
        # dangerous_chars から要素を取り出し、順番に char に入れて処理します。
        for char in dangerous_chars:
            # sanitizedを整えるために 指定部分を別の文字列に置き換えます。
            sanitized = sanitized.replace(char, '')
        
        return sanitized

    @staticmethod
    # パスワード強度チェック
    def validate_password_strength(password):
        """パスワード強度チェック"""
        
        checks = {
            "length": len(password) >= 8,
            "uppercase": any(c.isupper() for c in password),
            "lowercase": any(c.islower() for c in password),
            "digit": any(c.isdigit() for c in password),
            "special": any(c in "!@#$%^&*" for c in password)
        }
        
        return sum(checks.values()) >= 4, checks

    @staticmethod
    # SQLインジェクション対策（基本的な検証）
    def prevent_sql_injection(user_input):
        """SQLインジェクション対策（基本的な検証）"""
        
        dangerous_patterns = [
            r"union\s+select",
            r"drop\s+table",
            r"insert\s+into",
            r"delete\s+from",
            r"update\s+set",
            r"exec\s*\(",
            r"script\s*>",
        ]

        # cleaned入力を整えるために 文字列を小文字に変換します。
        cleaned_input = user_input.lower()
        # dangerous_patterns から要素を取り出し、順番に pattern に入れて処理します。
        for pattern in dangerous_patterns:
            
            if re.search(pattern, cleaned_input, re.IGNORECASE):
                
                return False, f"危険なパターンが検出されました: {pattern}"

        return True, "入力は安全です"

# demo_input_validation関数 — 入力検証デモの実行
def demo_input_validation():
    """入力検証デモの実行"""
    
    validator = InputValidator()

    print("=== 入力検証・セキュリティ対策デモ ===")

    test_emails = [
        "user@example.com",
        "invalid.email",
        "test@domain",
        "valid.email@company.co.jp"
    ]

    print("\n1. メールアドレス検証:")
    # test_emails から要素を取り出し、順番に email に入れて処理します。
    for email in test_emails:
        
        result = validator.validate_email(email)
        
        print(f"  {email}: {'有効' if result else '無効'}")

    test_inputs = [
        "Hello<script>alert('XSS')</script>",
        "Normal text input",
        "<img src='x' onerror='alert(1)'>",
        "Safe & clean input"
    ]

    print("\n2. 入力サニタイズ（XSS対策）:")
    # test_inputs から要素を取り出し、順番に test_input に入れて処理します。
    for test_input in test_inputs:
        
        sanitized = validator.sanitize_input(test_input)
        
        print(f"  元: {test_input}")
        
        print(f"  後: {sanitized}")

    test_passwords = [
        "password",
        "MyPass123!",
        "weak",
        "StrongP@ssw0rd",
        "12345"
    ]

    print("\n3. パスワード強度チェック:")
    # test_passwords から要素を取り出し、順番に password に入れて処理します。
    for password in test_passwords:
        
        is_strong, checks = validator.validate_password_strength(password)
        
        print(f"  {password}: {'強い' if is_strong else '弱い'}")
        
        print(f"    詳細: {checks}")

    test_sql_inputs = [
        "normal user input",
        "1' UNION SELECT * FROM users--",
        "Robert'; DROP TABLE students;--",
        "safe search term",
        "admin' OR '1'='1"
    ]

    print("\n4. SQLインジェクション対策:")
    # test_sql_inputs から要素を取り出し、順番に sql_input に入れて処理します。
    for sql_input in test_sql_inputs:
        
        is_safe, message = validator.prevent_sql_injection(sql_input)
        
        status = "安全" if is_safe else "危険"
        
        print(f"  {sql_input}: {status}")
        
        if not is_safe:
            
            print(f"    理由: {message}")

if __name__ == "__main__":
    
    demo_input_validation()
