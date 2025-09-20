"""
多要素認証（MFA）システム
OTPコード、バックアップコード、パスワードハッシュ化
"""

import random
import time
import hashlib

# MFASystemクラスの実装
class MFASystem:
    def __init__(self):
        self.users = {}
        
        self.otp_codes = {}
        
        self.backup_codes = {}

    # セキュアなユーザー登録
    def register_user(self, username, password, phone_number):
        """セキュアなユーザー登録"""
        
        self.users[username] = {
            'password': self._hash_password(password),
            'phone': phone_number,
            'mfa_enabled': True,
            'backup_codes': self._generate_backup_codes()
        }
        
        self.backup_codes[username] = self.users[username]['backup_codes'].copy()
        
        print(f"ユーザー {username} を登録しました")
        
        print(f"バックアップコード: {self.users[username]['backup_codes']}")

    # パスワードのハッシュ化
    def _hash_password(self, password):
        """パスワードのハッシュ化"""
        return hashlib.sha256(password.encode()).hexdigest()

    # バックアップコード生成
    def _generate_backup_codes(self):
        """バックアップコード生成"""
        
        return [f"{random.randint(100000, 999999):06d}" for _ in range(10)]

    # OTPコード送信
    def send_otp(self, username):
        """OTPコード送信"""
        
        if username not in self.users:
            
            return False

        otp_code = f"{random.randint(100000, 999999):06d}"
        
        self.otp_codes[username] = {
            'code': otp_code,
            'expires_at': time.time() + 300,  # 5分間有効
            'attempts': 0
        }

        print(f"OTP コード {otp_code} を {self.users[username]['phone']} に送信しました")
        
        return otp_code  # デモ用に実際のコードを返す

    # 多段階認証検証
    def verify_login(self, username, password, otp_code=None, backup_code=None):
        """多段階認証検証"""
        
        if username not in self.users:
            
            return {"success": False, "message": "ユーザーが存在しません"}

        user = self.users[username]

        if self._hash_password(password) != user['password']:
            
            return {"success": False, "message": "パスワードが間違っています"}

        if not user['mfa_enabled']:
            
            return {"success": True, "message": "ログイン成功"}

        if backup_code:
            
            if backup_code in self.backup_codes[username]:
                self.backup_codes[username].remove(backup_code)
                
                return {"success": True, "message": "バックアップコードでログイン成功"}
            else:
                
                return {"success": False, "message": "無効なバックアップコードです"}

        if username not in self.otp_codes:
            
            return {"success": False, "message": "OTP コードが未生成です"}

        otp_data = self.otp_codes[username]

        if time.time() > otp_data['expires_at']:
            
            return {"success": False, "message": "OTP コードの有効期限が切れました"}

        if otp_data['attempts'] >= 3:
            
            return {"success": False, "message": "OTP の試行回数上限に達しました"}

        if otp_code == otp_data['code']:
            del self.otp_codes[username]
            
            return {"success": True, "message": "2FA認証成功"}
        else:
            otp_data['attempts'] += 1
            
            return {"success": False, "message": f"OTP コードが間違っています（残り試行回数: {3 - otp_data['attempts']}）"}

    # MFA無効化
    def disable_mfa(self, username, password):
        """MFA無効化"""
        
        if username not in self.users:
            
            return False

        user = self.users[username]
        
        if self._hash_password(password) == user['password']:
            
            user['mfa_enabled'] = False
            
            return True
        
        return False

    # MFA有効化
    def enable_mfa(self, username, password, phone_number):
        """MFA有効化"""
        
        if username not in self.users:
            
            return False

        user = self.users[username]
        
        if self._hash_password(password) == user['password']:
            
            user['mfa_enabled'] = True
            
            user['phone'] = phone_number
            
            user['backup_codes'] = self._generate_backup_codes()
            
            self.backup_codes[username] = user['backup_codes'].copy()
            
            return True
        
        return False

    # バックアップコード取得
    def get_backup_codes(self, username):
        """バックアップコード取得"""
        
        if username in self.backup_codes:
            
            return self.backup_codes[username]
        
        return []

# demo_mfa_system関数 — 多要素認証システムデモ
def demo_mfa_system():
    """多要素認証システムデモ"""
    
    print("=== 多要素認証（MFA）システムデモ ===")

    mfa = MFASystem()

    print("\n1. ユーザー登録:")
    
    mfa.register_user("john", "secure_password", "+81-90-1234-5678")
    
    mfa.register_user("jane", "another_password", "+81-90-5678-1234")

    print("\n2. パスワードのみでのログイン試行:")
    
    result = mfa.verify_login("john", "secure_password")
    
    print(f"   結果: {result['message']}")

    print("\n3. OTP送信と多要素認証:")
    
    otp = mfa.send_otp("john")

    print(f"   正しいOTP ({otp}) でログイン:")
    
    result = mfa.verify_login("john", "secure_password", otp_code=otp)
    
    print(f"   結果: {result['message']}")

    print("\n4. 間違ったOTPでのログイン試行:")
    
    otp2 = mfa.send_otp("jane")
    
    wrong_attempts = ["123456", "654321", "000000"]

    for i, wrong_otp in enumerate(wrong_attempts, 1):
        
        result = mfa.verify_login("jane", "another_password", otp_code=wrong_otp)
        
        print(f"   試行 {i}: {result['message']}")

    print("\n5. バックアップコードでのログイン:")
    
    backup_codes = mfa.get_backup_codes("john")
    
    if backup_codes:
        
        backup_code = backup_codes[0]
        
        print(f"   バックアップコード ({backup_code}) でログイン:")
        
        result = mfa.verify_login("john", "secure_password", backup_code=backup_code)
        
        print(f"   結果: {result['message']}")

        print(f"   同じバックアップコード再使用:")
        
        result = mfa.verify_login("john", "secure_password", backup_code=backup_code)
        
        print(f"   結果: {result['message']}")

    print("\n6. MFA設定変更:")

    print("   MFA無効ユーザーを作成:")
    
    mfa.users["testuser"] = {
        'password': mfa._hash_password("testpass"),
        'phone': None,
        'mfa_enabled': False,
        'backup_codes': []
    }

    result = mfa.verify_login("testuser", "testpass")
    
    print(f"   MFA無効でログイン: {result['message']}")

    enable_result = mfa.enable_mfa("testuser", "testpass", "+81-90-9999-0000")
    
    if enable_result:
        
        print("   MFAを有効化しました")
        
        print(f"   新しいバックアップコード: {mfa.get_backup_codes('testuser')[:3]}...")

    print("\n7. セキュリティ統計:")
    
    total_users = len(mfa.users)
    
    mfa_enabled_users = sum(1 for user in mfa.users.values() if user['mfa_enabled'])
    
    active_otp_sessions = len(mfa.otp_codes)

    print(f"   総ユーザー数: {total_users}")
    
    print(f"   MFA有効ユーザー: {mfa_enabled_users}")
    
    print(f"   アクティブOTPセッション: {active_otp_sessions}")
    
    print(f"   MFA有効率: {(mfa_enabled_users/total_users*100):.1f}%")

    print("\n8. セキュリティベストプラクティス:")
    
    print("   ✓ パスワードハッシュ化: SHA-256による不可逆暗号化")
    
    print("   ✓ OTP有効期限: 5分間の時間制限")
    
    print("   ✓ 試行回数制限: 3回失敗でロック")
    
    print("   ✓ バックアップコード: デバイス紛失時の緊急アクセス")
    
    print("   ✓ 使い捨てコード: バックアップコードは一度のみ使用可能")

    print("\n9. 攻撃耐性テスト:")

    print("   OTP総当たり攻撃シミュレレーション:")
    
    otp3 = mfa.send_otp("john")
    
    attack_attempts = 0
    for guess in range(100000, 100010):  # 10回の推測
        
        result = mfa.verify_login("john", "secure_password", otp_code=str(guess).zfill(6))
        attack_attempts += 1
        
        if result['success']:
            
            print(f"     攻撃成功（{attack_attempts}回目）")
            break
        
        elif "試行回数上限" in result['message']:
            
            print(f"     攻撃阻止: {result['message']}")
            break

if __name__ == "__main__":
    
    demo_mfa_system()
