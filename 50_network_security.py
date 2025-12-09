"""
ネットワークセキュリティの基礎
ポートスキャン、IP評判チェック、接続監視
"""

import socket
import threading
import time
from collections import defaultdict

# NetworkSecurityDemoクラスの実装
class NetworkSecurityDemo:
    def __init__(self):
        
        self.allowed_ips = ['127.0.0.1', '192.168.1.0/24']
        
        self.connection_log = []

    # 基本的なポートスキャン機能
    def simple_port_scanner(self, target_host, ports):
        """基本的なポートスキャン機能"""
        
        open_ports = []
        
        print(f"ポートスキャン実行中: {target_host}")

        for port in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                
                result = sock.connect_ex((target_host, port))
                
                if result == 0:
                    open_ports.append(port)
                    
                    print(f"  ポート {port}: 開いている")
                sock.close()
            
            except Exception as e:
                
                print(f"  ポート {port}: エラー - {e}")
                pass

        return open_ports

    # IP アドレスの評判チェック（シミュレーション）
    def check_ip_reputation(self, ip_address):
        """IP アドレスの評判チェック（シミュレーション）"""
        
        suspicious_ips = ['10.0.0.666', '192.168.999.1', '1.2.3.4']

        if ip_address in suspicious_ips:
            
            return {
                "status": "suspicious",
                "reason": "既知の悪意あるIPアドレス",
                "risk_level": "HIGH"
            }
        else:
            
            return {
                "status": "clean",
                "reason": "問題のないIPアドレス",
                "risk_level": "LOW"
            }

    # 接続ログの記録
    def log_connection(self, ip, port, action):
        """接続ログの記録"""
        
        log_entry = {
            'timestamp': time.time(),
            'ip': ip,
            'port': port,
            'action': action,
            'formatted_time': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        self.connection_log.append(log_entry)
        
        return log_entry

    # 接続パターンの分析
    def analyze_connection_patterns(self):
        """接続パターンの分析"""
        
        if not self.connection_log:
            
            return {"message": "ログデータがありません"}

        ip_counts = defaultdict(int)
        
        port_counts = defaultdict(int)
        
        recent_connections = []

        current_time = time.time()

        for log in self.connection_log:
            ip_counts[log['ip']] += 1
            port_counts[log['port']] += 1

            if current_time - log['timestamp'] < 300:
                recent_connections.append(log)

        return {
            "total_connections": len(self.connection_log),
            "unique_ips": len(ip_counts),
            "most_active_ip": max(ip_counts.items(), key=lambda x: x[1]) if ip_counts else None,
            "most_targeted_port": max(port_counts.items(), key=lambda x: x[1]) if port_counts else None,
            "recent_connections": len(recent_connections)
        }

    # ネットワーク監視のシミュレーション
    def simulate_network_monitoring(self):
        """ネットワーク監視のシミュレーション"""
        print("ネットワーク監視を開始します...")

        simulated_events = [
            ('192.168.1.100', 80, 'HTTP_REQUEST'),
            ('10.0.0.50', 22, 'SSH_ATTEMPT'),
            ('192.168.1.200', 443, 'HTTPS_REQUEST'),
            ('1.2.3.4', 3389, 'RDP_ATTEMPT'),  # 疑わしいIP
            ('192.168.1.100', 8080, 'WEB_REQUEST'),
        ]

        for ip, port, action in simulated_events:
            
            log_entry = self.log_connection(ip, port, action)
            
            print(f"[{log_entry['formatted_time']}] {ip}:{port} - {action}")

            reputation = self.check_ip_reputation(ip)
            
            if reputation['status'] == 'suspicious':
                
                print(f"  ⚠️  警告: {ip} は疑わしいIPアドレスです - {reputation['reason']}")

            time.sleep(0.1)  # シミュレーション用の待機

# demo_network_security関数 — ネットワークセキュリティデモの実行
def demo_network_security():
    """ネットワークセキュリティデモの実行"""
    
    print("=== ネットワークセキュリティ基礎デモ ===")

    security = NetworkSecurityDemo()

    print("\n1. ローカルホストのポートスキャン:")
    
    common_ports = [22, 80, 443, 3389, 5432]
    
    open_ports = security.simple_port_scanner('127.0.0.1', common_ports)
    
    print(f"   開いているポート: {open_ports}")

    print("\n2. IP評判チェック:")
    
    test_ips = ['192.168.1.100', '1.2.3.4', '8.8.8.8']

    for ip in test_ips:
        
        reputation = security.check_ip_reputation(ip)
        
        print(f"   {ip}: {reputation['status']} (リスクレベル: {reputation['risk_level']})")
        
        print(f"     理由: {reputation['reason']}")

    print("\n3. ネットワーク監視シミュレーション:")
    
    security.simulate_network_monitoring()

    print("\n4. 接続パターン分析:")
    
    analysis = security.analyze_connection_patterns()
    
    print(f"   総接続数: {analysis['total_connections']}")
    
    print(f"   ユニークIP数: {analysis['unique_ips']}")

    if analysis['most_active_ip']:
        
        ip, count = analysis['most_active_ip']
        
        print(f"   最もアクティブなIP: {ip} ({count}回)")

    if analysis['most_targeted_port']:
        
        port, count = analysis['most_targeted_port']
        
        print(f"   最も狙われたポート: {port} ({count}回)")

    print(f"   過去5分間の接続: {analysis['recent_connections']}件")

    print("\n5. セキュリティ推奨事項:")
    
    if analysis['total_connections'] > 3:
        print("   ℹ️  接続ログを定期的に監視してください")

    if open_ports:
        
        print(f"   ⚠️  開いているポート ({open_ports}) のセキュリティを確認してください")

    print("   💡 ファイアウォールの設定を確認し、不要なポートを閉じることを推奨します")
    print("   💡 侵入検知システム（IDS）の導入を検討してください")

if __name__ == "__main__":
    
    demo_network_security()
