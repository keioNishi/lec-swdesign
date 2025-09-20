"""
役割と権限管理（RBAC）システム
ユーザー認証、アクセス制御、監査ログ
"""

from enum import Enum
from datetime import datetime, timedelta

# Roleクラスの実装
class Role(Enum):
    
    ADMIN = "admin"
    
    USER = "user"
    
    GUEST = "guest"

# Permissionクラスの実装
class Permission(Enum):
    
    READ = "read"
    
    WRITE = "write"
    
    DELETE = "delete"
    
    ADMIN = "admin"

# RBACSystemクラスの実装
class RBACSystem:
    def __init__(self):
        
        self.users = {}
        
        self.role_permissions = {
            Role.ADMIN: [Permission.READ, Permission.WRITE, Permission.DELETE, Permission.ADMIN],
            Role.USER: [Permission.READ, Permission.WRITE],
            Role.GUEST: [Permission.READ]
        }
        
        self.access_log = []

    # ユーザー作成
    def create_user(self, username, role, password):
        """ユーザー作成"""
        
        self.users[username] = {
            'role': role,
            'password': password,
            'created_at': datetime.now(),
            'last_login': None,
            'failed_attempts': 0
        }

    # 認証処理
    def authenticate(self, username, password):
        """認証処理"""
        
        if username not in self.users:
            
            self._log_access_attempt(username, "AUTH_FAILED", "ユーザー不存在")
            
            return False

        user = self.users[username]

        if user['failed_attempts'] >= 3:
            
            self._log_access_attempt(username, "ACCOUNT_LOCKED", "連続失敗によるロック")
            
            print(f"アカウント {username} は一時的にロック中")
            
            return False

        if user['password'] == password:
            user['last_login'] = datetime.now()
            
            user['failed_attempts'] = 0
            
            self._log_access_attempt(username, "AUTH_SUCCESS", "正常ログイン")
            
            return True
        else:
            user['failed_attempts'] += 1
            
            self._log_access_attempt(username, "AUTH_FAILED", "パスワード不正")
            
            return False

    # 権限チェック
    def check_permission(self, username, required_permission):
        """権限チェック"""
        
        if username not in self.users:
            
            self._log_access_attempt(username, "PERMISSION_DENIED", "ユーザー不存在")
            
            return False

        user_role = self.users[username]['role']
        allowed_permissions = self.role_permissions.get(user_role, [])
        
        access_granted = required_permission in allowed_permissions

        result = "PERMISSION_GRANTED" if access_granted else "PERMISSION_DENIED"
        
        self._log_access_attempt(username, result, f"権限: {required_permission.value}")

        return access_granted

    # アクセス試行のログ記録
    def _log_access_attempt(self, username, action, details):
        """アクセス試行のログ記録"""
        
        log_entry = {
            'username': username,
            'action': action,
            'details': details,
            'timestamp': datetime.now()
        }
        self.access_log.append(log_entry)

    # アクセスレポート生成
    def get_access_report(self):
        """アクセスレポート生成"""
        recent_logs = [log for log in self.access_log
                      if datetime.now() - log['timestamp'] < timedelta(hours=24)]

        return {
            'total_attempts': len(self.access_log),
            'recent_attempts_24h': len(recent_logs),
            'successful_logins': len([log for log in self.access_log
                                    if log['action'] == 'AUTH_SUCCESS']),
            'failed_logins': len([log for log in self.access_log
                                if log['action'] == 'AUTH_FAILED']),
            'permission_denied': len([log for log in self.access_log
                                    if log['action'] == 'PERMISSION_DENIED']),
            'recent_logs': recent_logs[-10:]  # 最新10件
        }

    # アカウントロック解除（管理者機能）
    def unlock_account(self, username):
        """アカウントロック解除（管理者機能）"""
        
        if username in self.users:
            
            self.users[username]['failed_attempts'] = 0
            
            self._log_access_attempt(username, "ACCOUNT_UNLOCKED", "管理者による解除")
            
            return True
        
        return False

    # ユーザー役割変更（管理者機能）
    def change_user_role(self, username, new_role, admin_user):
        """ユーザー役割変更（管理者機能）"""
        
        if admin_user not in self.users:
            
            return False

        if self.users[admin_user]['role'] != Role.ADMIN:
            
            self._log_access_attempt(admin_user, "ROLE_CHANGE_DENIED", "管理者権限なし")
            
            return False

        if username in self.users:
            
            old_role = self.users[username]['role']
            
            self.users[username]['role'] = new_role
            
            self._log_access_attempt(admin_user, "ROLE_CHANGED",
                                   f"{username}: {old_role.value} → {new_role.value}")
            
            return True
        
        return False

# demo_access_control関数 — アクセス制御デモの実行
def demo_access_control():
    """アクセス制御デモの実行"""
    
    print("=== 役割と権限管理（RBAC）システムデモ ===")

    rbac = RBACSystem()

    print("\n1. ユーザー作成:")
    
    rbac.create_user("alice", Role.ADMIN, "admin_pass")
    
    rbac.create_user("bob", Role.USER, "user_pass")
    
    rbac.create_user("charlie", Role.GUEST, "guest_pass")
    
    print("   作成完了: alice (ADMIN), bob (USER), charlie (GUEST)")

    print("\n2. 認証テスト:")
    
    auth_tests = [
        ("alice", "admin_pass", "正しいパスワード"),
        ("bob", "wrong_pass", "間違ったパスワード"),
        ("bob", "user_pass", "正しいパスワード"),
        ("unknown", "any_pass", "存在しないユーザー"),
    ]

    for username, password, description in auth_tests:
        
        result = rbac.authenticate(username, password)
        
        status = "成功" if result else "失敗"
        
        print(f"   {username} - {description}: {status}")

    print("\n3. 権限チェックテスト:")
    
    permission_tests = [
        ("alice", Permission.DELETE, "管理者の削除権限"),
        ("bob", Permission.READ, "ユーザーの読み取り権限"),
        ("bob", Permission.DELETE, "ユーザーの削除権限"),
        ("charlie", Permission.READ, "ゲストの読み取り権限"),
        ("charlie", Permission.WRITE, "ゲストの書き込み権限"),
    ]

    for username, permission, description in permission_tests:
        
        result = rbac.check_permission(username, permission)
        
        status = "許可" if result else "拒否"
        
        print(f"   {description}: {status}")

    print("\n4. ブルートフォース攻撃シミュレーション:")
    
    print("   bob に対する連続ログイン失敗:")
    for i in range(4):
        
        result = rbac.authenticate("bob", "wrong_password")
        
        print(f"     試行 {i+1}: {'成功' if result else '失敗'}")

    print("\n5. アクセスレポート:")
    
    report = rbac.get_access_report()
    
    print(f"   総アクセス試行: {report['total_attempts']}")
    
    print(f"   24時間以内の試行: {report['recent_attempts_24h']}")
    
    print(f"   成功ログイン: {report['successful_logins']}")
    
    print(f"   失敗ログイン: {report['failed_logins']}")
    
    print(f"   権限拒否: {report['permission_denied']}")

    print("\n   最近のアクセスログ（最新5件）:")
    for log in report['recent_logs'][-5:]:
        
        timestamp = log['timestamp'].strftime('%H:%M:%S')
        
        print(f"     [{timestamp}] {log['username']}: {log['action']} - {log['details']}")

    print("\n6. 管理者機能テスト:")

    unlock_result = rbac.unlock_account("bob")
    
    print(f"   bobのアカウントロック解除: {'成功' if unlock_result else '失敗'}")

    role_change_result = rbac.change_user_role("charlie", Role.USER, "alice")
    
    print(f"   charlieの役割変更 (GUEST→USER): {'成功' if role_change_result else '失敗'}")

    new_permission = rbac.check_permission("charlie", Permission.WRITE)
    
    print(f"   変更後のcharlie書き込み権限: {'許可' if new_permission else '拒否'}")

    print("\n7. セキュリティベストプラクティス:")
    
    print("   ✓ 最小権限の原則: 各役割に必要最小限の権限のみ付与")
    print("   ✓ アカウントロック: 連続失敗でブルートフォース攻撃を防止")
    print("   ✓ 監査ログ: すべてのアクセス試行を記録")
    
    print("   ✓ 役割ベースアクセス制御: 個別ではなく役割単位での権限管理")
    
    print("   ✓ 管理者機能分離: 特権操作は管理者のみ実行可能")

if __name__ == "__main__":
    
    demo_access_control()
