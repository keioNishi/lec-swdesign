"""
侵入検知システム（IDS）の実装
攻撃パターン検知、リアルタイム監視、セキュリティダッシュボード
"""

import time
import re
from collections import defaultdict, deque
from datetime import datetime, timedelta

# SimpleIDSクラスの実装
class SimpleIDS:
    def __init__(self):
        
        self.rules = [
            {'name': 'Port Scan Detection', 'pattern': r'port_scan', 'severity': 'HIGH'},
            {'name': 'SQL Injection', 'pattern': r'UNION.*SELECT|DROP.*TABLE', 'severity': 'CRITICAL'},
            {'name': 'XSS Attempt', 'pattern': r'<script.*?>|javascript:', 'severity': 'MEDIUM'},
            {'name': 'Brute Force', 'pattern': r'failed_login', 'severity': 'HIGH'},
            {'name': 'Directory Traversal', 'pattern': r'\.\./|\.\.\\\|%2e%2e%2f', 'severity': 'HIGH'},
            {'name': 'Command Injection', 'pattern': r';\s*(rm|del|format|shutdown)', 'severity': 'CRITICAL'}
        ]

        self.alerts = []
        
        self.connection_tracking = defaultdict(lambda: deque(maxlen=100))
        
        self.blocked_ips = set()

    # ネットワークイベントの分析
    def analyze_network_event(self, event_data):
        """ネットワークイベントの分析"""
        
        alerts_triggered = []

        for rule in self.rules:
            
            if re.search(rule['pattern'], event_data['payload'], re.IGNORECASE):
                
                alert = {
                    'timestamp': datetime.now(),
                    'rule_name': rule['name'],
                    'severity': rule['severity'],
                    'source_ip': event_data.get('source_ip'),
                    'event_data': event_data
                }
                alerts_triggered.append(alert)
                self.alerts.append(alert)

        source_ip = event_data.get('source_ip')
        
        if source_ip:
            self.connection_tracking[source_ip].append({
                'timestamp': time.time(),
                'event': event_data
            })

            recent_events = [e for e in self.connection_tracking[source_ip]
                           if time.time() - e['timestamp'] < 60]

            if len(recent_events) > 10:
                
                alert = {
                    'timestamp': datetime.now(),
                    'rule_name': 'High Frequency Access',
                    'severity': 'MEDIUM',
                    'source_ip': source_ip,
                    'event_count': len(recent_events)
                }
                alerts_triggered.append(alert)
                self.alerts.append(alert)

        return alerts_triggered

    # IPアドレスのブロック
    def block_ip(self, ip_address, reason="Manual block"):
        """IPアドレスのブロック"""
        self.blocked_ips.add(ip_address)
        
        alert = {
            'timestamp': datetime.now(),
            'rule_name': 'IP Blocked',
            'severity': 'HIGH',
            'source_ip': ip_address,
            'reason': reason
        }
        self.alerts.append(alert)
        
        print(f"IP {ip_address} をブロックしました: {reason}")

    # IPアドレスのブロック状態確認
    def is_ip_blocked(self, ip_address):
        """IPアドレスのブロック状態確認"""
        
        return ip_address in self.blocked_ips

    # セキュリティダッシュボード情報
    def get_security_dashboard(self):
        """セキュリティダッシュボード情報"""
        recent_alerts = [a for a in self.alerts
                        if datetime.now() - a['timestamp'] < timedelta(hours=24)]

        severity_count = defaultdict(int)
        for alert in recent_alerts:
            severity_count[alert['severity']] += 1

        return {
            'total_alerts_24h': len(recent_alerts),
            'alerts_by_severity': dict(severity_count),
            'top_source_ips': self._get_top_source_ips(),
            'recent_critical_alerts': [a for a in recent_alerts if a['severity'] == 'CRITICAL'],
            'blocked_ips': list(self.blocked_ips),
            'total_monitored_ips': len(self.connection_tracking)
        }

    # 最もアクティブなIPアドレスのトップ5
    def _get_top_source_ips(self):
        """最もアクティブなIPアドレスのトップ5"""
        
        ip_counts = defaultdict(int)
        for alert in self.alerts:
            
            if alert.get('source_ip'):
                ip_counts[alert['source_ip']] += 1

        return sorted(ip_counts.items(), key=lambda x: x[1], reverse=True)[:5]

    # インシデントレポート生成
    def generate_incident_report(self, hours=24):
        """インシデントレポート生成"""
        
        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent_alerts = [a for a in self.alerts if a['timestamp'] > cutoff_time]

        if not recent_alerts:
            
            return {"message": f"過去{hours}時間にアラートはありません"}

        severity_stats = defaultdict(int)
        
        ip_stats = defaultdict(int)
        
        attack_types = defaultdict(int)

        for alert in recent_alerts:
            severity_stats[alert['severity']] += 1
            
            if alert.get('source_ip'):
                ip_stats[alert['source_ip']] += 1
            attack_types[alert['rule_name']] += 1

        most_dangerous_ip = max(ip_stats.items(), key=lambda x: x[1]) if ip_stats else None

        return {
            'report_period': f"過去{hours}時間",
            'total_incidents': len(recent_alerts),
            'severity_breakdown': dict(severity_stats),
            'most_common_attacks': dict(sorted(attack_types.items(), key=lambda x: x[1], reverse=True)[:5]),
            'most_dangerous_ip': most_dangerous_ip,
            'recommendations': self._generate_recommendations(recent_alerts)
        }

    # セキュリティ推奨事項の生成
    def _generate_recommendations(self, alerts):
        """セキュリティ推奨事項の生成"""
        
        recommendations = []

        attack_types = [alert['rule_name'] for alert in alerts]

        if 'SQL Injection' in attack_types:
            recommendations.append("SQLインジェクション攻撃を検知: WAF（Web Application Firewall）の導入を推奨")

        if 'XSS Attempt' in attack_types:
            recommendations.append("XSS攻撃を検知: 入力値検証の強化とContent Security Policyの実装を推奨")

        if 'Port Scan Detection' in attack_types:
            recommendations.append("ポートスキャンを検知: ファイアウォール設定の見直しと不要ポートの閉鎖を推奨")

        if 'Brute Force' in attack_types:
            recommendations.append("ブルートフォース攻撃を検知: アカウントロック機能の強化とMFAの導入を推奨")

        critical_alerts = [a for a in alerts if a['severity'] == 'CRITICAL']
        
        if len(critical_alerts) > 5:
            recommendations.append("多数の重要度CRITICALアラート: 緊急対応チームの招集と システム隔離を検討")

        return recommendations

# demo_intrusion_detection関数 — 侵入検知システムデモ
def demo_intrusion_detection():
    """侵入検知システムデモ"""
    
    print("=== 侵入検知システム（IDS）デモ ===")

    ids = SimpleIDS()

    print("\n1. 正常トラフィックシミュレーション:")
    
    normal_events = [
        {'source_ip': '192.168.1.100', 'payload': 'GET /index.html HTTP/1.1'},
        {'source_ip': '192.168.1.101', 'payload': 'POST /api/users HTTP/1.1'},
        {'source_ip': '192.168.1.102', 'payload': 'GET /static/style.css HTTP/1.1'},
    ]

    for event in normal_events:
        
        alerts = ids.analyze_network_event(event)
        
        print(f"   {event['source_ip']}: {len(alerts)} アラート")

    print("\n2. 攻撃シミュレーション:")
    
    attack_events = [
        {'source_ip': '10.0.0.666', 'payload': 'GET /admin/users?id=1\' UNION SELECT * FROM passwords--'},
        {'source_ip': '10.0.0.666', 'payload': 'GET /search?q=<script>alert("XSS")</script>'},
        {'source_ip': '203.0.113.42', 'payload': 'port_scan detected on multiple ports'},
        {'source_ip': '203.0.113.42', 'payload': 'failed_login attempt #1'},
        {'source_ip': '203.0.113.42', 'payload': 'failed_login attempt #2'},
        {'source_ip': '203.0.113.42', 'payload': 'failed_login attempt #3'},
        {'source_ip': '198.51.100.10', 'payload': 'GET /../../../../etc/passwd HTTP/1.1'},
        {'source_ip': '198.51.100.10', 'payload': 'POST /cmd.php?cmd=rm -rf / HTTP/1.1'},
    ]

    for event in attack_events:
        
        alerts = ids.analyze_network_event(event)
        
        if alerts:
            print(f"   🚨 {event['source_ip']}: {len(alerts)} アラート検出")
            for alert in alerts:
                
                print(f"      - {alert['rule_name']} ({alert['severity']})")
        else:
            
            print(f"   ✓ {event['source_ip']}: アラートなし")

    print("\n3. 高頻度アクセス攻撃シミュレーション:")
    
    flood_ip = '192.0.2.100'
    for i in range(15):  # 1分間に15回のアクセス
        
        event = {'source_ip': flood_ip, 'payload': f'GET /api/data?request={i}'}
        
        alerts = ids.analyze_network_event(event)

    print(f"   {flood_ip} からの高頻度アクセス: {'検出' if alerts else '未検出'}")

    print("\n4. IPブロック機能:")
    
    suspicious_ip = '10.0.0.666'
    
    ids.block_ip(suspicious_ip, "多数のSQLインジェクション攻撃")

    blocked_status = ids.is_ip_blocked(suspicious_ip)
    
    print(f"   {suspicious_ip} のブロック状態: {'ブロック中' if blocked_status else '許可中'}")

    print("\n5. セキュリティダッシュボード:")
    
    dashboard = ids.get_security_dashboard()
    
    print(f"   24時間のアラート総数: {dashboard['total_alerts_24h']}")
    
    print(f"   重要度別分布: {dashboard['alerts_by_severity']}")
    
    print(f"   監視中IP数: {dashboard['total_monitored_ips']}")
    
    print(f"   ブロック済みIP数: {len(dashboard['blocked_ips'])}")

    if dashboard['top_source_ips']:
        
        print("   最もアクティブなIP（トップ3）:")
        for ip, count in dashboard['top_source_ips'][:3]:
            
            print(f"     {ip}: {count}回")

    if dashboard['recent_critical_alerts']:
        
        print(f"   重要度CRITICALアラート: {len(dashboard['recent_critical_alerts'])}件")

    print("\n6. インシデントレポート:")
    
    report = ids.generate_incident_report()
    
    print(f"   {report['report_period']}の総インシデント: {report['total_incidents']}件")
    
    print(f"   重要度分布: {report['severity_breakdown']}")

    if report['most_common_attacks']:
        
        print("   最も多い攻撃タイプ:")
        for attack_type, count in list(report['most_common_attacks'].items())[:3]:
            
            print(f"     {attack_type}: {count}回")

    if report['most_dangerous_ip']:
        
        ip, count = report['most_dangerous_ip']
        
        print(f"   最も危険なIP: {ip} ({count}回の攻撃)")

    print("\n7. セキュリティ推奨事項:")
    
    if report['recommendations']:
        for recommendation in report['recommendations']:
            print(f"   💡 {recommendation}")
    else:
        
        print("   ✓ 現在のところ特別な対策は不要です")

    print("\n8. システム統計:")
    
    print(f"   総ルール数: {len(ids.rules)}")
    
    print(f"   総アラート数: {len(ids.alerts)}")
    
    print(f"   追跡中接続数: {len(ids.connection_tracking)}")
    
    print(f"   ブロック済みIP数: {len(ids.blocked_ips)}")

if __name__ == "__main__":
    
    demo_intrusion_detection()
