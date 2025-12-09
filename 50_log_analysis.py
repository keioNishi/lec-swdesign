"""
ログ解析とセキュリティ監視
異常パターンの検知と分析
"""

import re
from datetime import datetime
from collections import Counter

# LogAnalyzerクラスの実装
class LogAnalyzer:
    # initをまとめる __init__ 関数では self を基に処理の流れを整理します。
    def __init__(self):
        
        self.suspicious_patterns = [
            r'(\d+\.\d+\.\d+\.\d+).*?GET /admin',  # 管理者ページへのアクセス
            r'(\d+\.\d+\.\d+\.\d+).*?[\'"].*?script',  # XSS攻撃の試行
            r'(\d+\.\d+\.\d+\.\d+).*?UNION.*?SELECT',  # SQLインジェクション
        ]

    # ログファイルの分析
    def analyze_log_file(self, log_entries):
        """ログファイルの分析"""
        
        results = {
            "total_entries": len(log_entries),
            "suspicious_activities": [],
            "ip_frequency": Counter(),
            "attack_patterns": Counter()
        }

        # log_entries から要素を取り出し、順番に entry に入れて処理します。
        for entry in log_entries:
            
            ip_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', entry)
            
            if ip_match:
                
                ip = ip_match.group(1)
                results["ip_frequency"][ip] += 1

            # self.suspicious_patterns から要素を取り出し、順番に pattern に入れて処理します。
            for pattern in self.suspicious_patterns:
                
                if re.search(pattern, entry, re.IGNORECASE):
                    # リストの末尾に要素を追加します。
                    results["suspicious_activities"].append(entry)
                    results["attack_patterns"]["suspicious"] += 1

        return results

    # ブルートフォース攻撃の検知
    def detect_brute_force(self, log_entries, threshold=5):
        """ブルートフォース攻撃の検知"""
        
        failed_login_pattern = r'(\d+\.\d+\.\d+\.\d+).*?(401|403|failed|invalid)'
        
        failed_attempts = Counter()

        # log_entries から要素を取り出し、順番に entry に入れて処理します。
        for entry in log_entries:
            
            match = re.search(failed_login_pattern, entry, re.IGNORECASE)
            
            if match:
                
                ip = match.group(1)
                failed_attempts[ip] += 1

        # suspiciousipsを failed_attempts.items() から count >= threshold を満たす要素を取り出し、キー ip と値 count の辞書を作ります。
        suspicious_ips = {ip: count for ip, count in failed_attempts.items()
                         if count >= threshold}

        return suspicious_ips

    # アクセスパターンの分析
    def analyze_access_patterns(self, log_entries):
        """アクセスパターンの分析"""
        
        patterns = {
            "total_requests": len(log_entries),
            "unique_ips": set(),
            "status_codes": Counter(),
            "request_methods": Counter(),
            "popular_paths": Counter()
        }

        # log_entries から要素を取り出し、順番に entry に入れて処理します。
        for entry in log_entries:
            
            ip_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', entry)
            
            if ip_match:
                # 集合に要素を追加します。
                patterns["unique_ips"].add(ip_match.group(1))

            status_match = re.search(r'\s(\d{3})\s', entry)
            
            if status_match:
                patterns["status_codes"][status_match.group(1)] += 1

            method_match = re.search(r'"(GET|POST|PUT|DELETE|HEAD)', entry)
            
            if method_match:
                patterns["request_methods"][method_match.group(1)] += 1

            path_match = re.search(r'"[A-Z]+\s([^\s]+)', entry)
            
            if path_match:
                patterns["popular_paths"][path_match.group(1)] += 1

        patterns["unique_ips"] = len(patterns["unique_ips"])
        
        return patterns

# demo_log_analysis関数 — ログ解析デモの実行
def demo_log_analysis():
    """ログ解析デモの実行"""
    
    print("=== ログ解析・セキュリティ監視デモ ===")

    sample_logs = [
        "192.168.1.100 - - [15/Mar/2024:10:00:01] \"GET /index.html\" 200",
        "10.0.0.50 - - [15/Mar/2024:10:00:02] \"GET /admin/login\" 401",
        "192.168.1.100 - - [15/Mar/2024:10:00:03] \"GET /search?q=<script>alert('xss')</script>\" 200",
        "203.0.113.42 - - [15/Mar/2024:10:00:04] \"POST /login\" 200",
        "203.0.113.42 - - [15/Mar/2024:10:00:05] \"POST /login\" 401",
        "203.0.113.42 - - [15/Mar/2024:10:00:06] \"POST /login\" 401",
        "203.0.113.42 - - [15/Mar/2024:10:00:07] \"POST /login\" 401",
        "192.168.1.200 - - [15/Mar/2024:10:00:08] \"GET /data?id=1' UNION SELECT * FROM users--\" 500",
        "10.0.0.50 - - [15/Mar/2024:10:00:09] \"GET /admin/users\" 401",
        "192.168.1.100 - - [15/Mar/2024:10:00:10] \"GET /profile\" 200"
    ]

    analyzer = LogAnalyzer()

    print("\n1. 基本ログ分析:")
    
    results = analyzer.analyze_log_file(sample_logs)
    
    print(f"   総エントリ数: {results['total_entries']}")
    
    print(f"   疑わしい活動: {len(results['suspicious_activities'])}件")
    
    print(f"   IP別アクセス頻度: {dict(results['ip_frequency'])}")

    if results['suspicious_activities']:
        
        print("\n   検出された疑わしい活動:")
        # results['suspicious_activities'] から要素を取り出し、順番に activity に入れて処理します。
        for activity in results['suspicious_activities']:
            
            print(f"     {activity}")

    print("\n2. ブルートフォース攻撃検知:")
    
    brute_force_ips = analyzer.detect_brute_force(sample_logs, threshold=3)
    
    if brute_force_ips:
        
        print("   検出された疑わしいIP:")
        # brute_force_ips.items() から要素を取り出し、順番に (ip, count) に入れて処理します。
        for ip, count in brute_force_ips.items():
            
            print(f"     {ip}: {count}回の失敗")
    else:
        
        print("   ブルートフォース攻撃は検出されませんでした")

    print("\n3. アクセスパターン分析:")
    
    patterns = analyzer.analyze_access_patterns(sample_logs)
    
    print(f"   総リクエスト数: {patterns['total_requests']}")
    
    print(f"   ユニークIP数: {patterns['unique_ips']}")
    
    print(f"   ステータスコード分布: {dict(patterns['status_codes'])}")
    
    print(f"   HTTPメソッド分布: {dict(patterns['request_methods'])}")
    
    print(f"   人気パス（トップ3）: {dict(patterns['popular_paths'].most_common(3))}")

    print("\n4. セキュリティ推奨事項:")
    
    if '401' in patterns['status_codes'] and patterns['status_codes']['401'] > 2:
        
        print("   ⚠️  多数の認証失敗が検出されました - アカウントロック機能の導入を推奨")

    if results['attack_patterns']['suspicious'] > 0:
        
        print("   ⚠️  攻撃パターンが検出されました - WAF（Web Application Firewall）の導入を推奨")

    if patterns['unique_ips'] > 5:
        
        print("   ℹ️  多数のIPからのアクセスがあります - 正常な動作と思われます")

if __name__ == "__main__":
    
    demo_log_analysis()
