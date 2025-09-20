"""
ネットワークパフォーマンスの測定と最適化

ネットワークパフォーマンスとは：
- スループット（データ転送速度）
- レイテンシ（遅延時間）
- パケットロス（パケット損失率）
- ジッター（遅延のばらつき）
- 帯域利用効率
"""

import socket
import time
import threading
import statistics
from datetime import datetime
import struct
import random


class NetworkPerformanceAnalyzer:
    """ネットワークパフォーマンス分析クラス"""

    def __init__(self):
        self.test_data_sizes = [1024, 4096, 16384, 65536]  # バイト
        self.test_iterations = 5
        self.results = {}

    def measure_latency(self, host, port, timeout=5):
        """レイテンシ（遅延時間）を測定"""
        print(f"=== レイテンシ測定: {host}:{port} ===")

        latencies = []

        for i in range(self.test_iterations):
            try:
                start_time = time.time()

                # TCP接続を確立
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(timeout)
                sock.connect((host, port))

                end_time = time.time()
                latency = (end_time - start_time) * 1000  # ミリ秒

                latencies.append(latency)
                sock.close()

                print(f"  試行 {i+1}: {latency:.2f} ms")

            except Exception as e:
                print(f"  試行 {i+1}: エラー - {e}")

        if latencies:
            avg_latency = statistics.mean(latencies)
            min_latency = min(latencies)
            max_latency = max(latencies)
            jitter = statistics.stdev(latencies) if len(latencies) > 1 else 0

            print(f"\\n結果:")
            print(f"  平均レイテンシ: {avg_latency:.2f} ms")
            print(f"  最小レイテンシ: {min_latency:.2f} ms")
            print(f"  最大レイテンシ: {max_latency:.2f} ms")
            print(f"  ジッター: {jitter:.2f} ms")

            return {
                'average': avg_latency,
                'minimum': min_latency,
                'maximum': max_latency,
                'jitter': jitter,
                'samples': latencies
            }

        return None

    def measure_throughput(self, host, port, data_size=1024*1024):
        """スループット（データ転送速度）を測定"""
        print(f"\\n=== スループット測定: {host}:{port} ===")
        print(f"データサイズ: {data_size:,} bytes ({data_size/1024/1024:.1f} MB)")

        try:
            # テストデータを生成
            test_data = b'A' * data_size

            # サーバーを別スレッドで起動
            server_thread = threading.Thread(
                target=self.throughput_server,
                args=(port, data_size)
            )
            server_thread.daemon = True
            server_thread.start()

            # サーバーの起動を待機
            time.sleep(0.5)

            # クライアントでスループット測定
            start_time = time.time()

            client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_sock.connect((host, port))

            # データを送信
            total_sent = 0
            while total_sent < data_size:
                sent = client_sock.send(test_data[total_sent:])
                total_sent += sent

            # 完了通知を受信
            client_sock.recv(1024)
            end_time = time.time()

            client_sock.close()

            # スループットを計算
            duration = end_time - start_time
            throughput_bps = data_size / duration  # bytes per second
            throughput_mbps = throughput_bps / (1024 * 1024)  # MB per second

            print(f"\\n結果:")
            print(f"  転送時間: {duration:.3f} 秒")
            print(f"  スループット: {throughput_bps:,.0f} bytes/sec")
            print(f"  スループット: {throughput_mbps:.2f} MB/sec")
            print(f"  スループット: {throughput_mbps * 8:.2f} Mbps")

            return {
                'duration': duration,
                'throughput_bps': throughput_bps,
                'throughput_mbps': throughput_mbps,
                'data_size': data_size
            }

        except Exception as e:
            print(f"✗ スループット測定エラー: {e}")
            return None

    def throughput_server(self, port, expected_size):
        """スループット測定用サーバー"""
        try:
            server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_sock.bind(('localhost', port))
            server_sock.listen(1)

            client_sock, addr = server_sock.accept()

            # データを受信
            total_received = 0
            while total_received < expected_size:
                data = client_sock.recv(65536)
                if not data:
                    break
                total_received += len(data)

            # 完了通知を送信
            client_sock.send(b"DONE")
            client_sock.close()
            server_sock.close()

        except Exception as e:
            print(f"スループット測定サーバーエラー: {e}")

    def measure_packet_loss(self, host, port, packet_count=100):
        """パケットロス率を測定（UDP使用）"""
        print(f"\\n=== パケットロス測定: {host}:{port} ===")
        print(f"送信パケット数: {packet_count}")

        try:
            # UDPサーバーを別スレッドで起動
            received_packets = []
            server_thread = threading.Thread(
                target=self.packet_loss_server,
                args=(port, packet_count, received_packets)
            )
            server_thread.daemon = True
            server_thread.start()

            # サーバーの起動を待機
            time.sleep(0.5)

            # UDPクライアントでパケットを送信
            client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            sent_packets = []
            for i in range(packet_count):
                packet_id = i
                timestamp = time.time()
                packet_data = struct.pack('!Id', packet_id, timestamp)

                client_sock.sendto(packet_data, (host, port))
                sent_packets.append(packet_id)

                # 送信間隔を調整（オーバーロードを防ぐ）
                time.sleep(0.01)

            client_sock.close()

            # 結果の収集を待機
            time.sleep(2)

            # パケットロス率を計算
            sent_count = len(sent_packets)
            received_count = len(received_packets)
            lost_count = sent_count - received_count
            loss_rate = (lost_count / sent_count) * 100

            print(f"\\n結果:")
            print(f"  送信パケット: {sent_count}")
            print(f"  受信パケット: {received_count}")
            print(f"  失われたパケット: {lost_count}")
            print(f"  パケットロス率: {loss_rate:.2f}%")

            return {
                'sent': sent_count,
                'received': received_count,
                'lost': lost_count,
                'loss_rate': loss_rate
            }

        except Exception as e:
            print(f"✗ パケットロス測定エラー: {e}")
            return None

    def packet_loss_server(self, port, expected_count, received_packets):
        """パケットロス測定用UDPサーバー"""
        try:
            server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            server_sock.bind(('localhost', port))
            server_sock.settimeout(5)  # 5秒でタイムアウト

            start_time = time.time()
            while len(received_packets) < expected_count:
                try:
                    data, addr = server_sock.recvfrom(1024)
                    packet_id, timestamp = struct.unpack('!Id', data)
                    received_packets.append(packet_id)

                    # タイムアウトチェック
                    if time.time() - start_time > 10:
                        break

                except socket.timeout:
                    break

            server_sock.close()

        except Exception as e:
            print(f"パケットロス測定サーバーエラー: {e}")

    def bandwidth_utilization_test(self):
        """帯域利用効率のテスト"""
        print("\\n=== 帯域利用効率テスト ===")

        # 異なるデータサイズでのスループット測定
        results = []

        for data_size in self.test_data_sizes:
            print(f"\\nデータサイズ: {data_size:,} bytes")

            # 空いているポートを見つける
            test_port = self.find_free_port()

            result = self.measure_throughput('localhost', test_port, data_size)
            if result:
                results.append({
                    'data_size': data_size,
                    'throughput_mbps': result['throughput_mbps'],
                    'duration': result['duration']
                })

        # 結果の分析
        if results:
            print("\\n=== 帯域利用効率分析 ===")
            for result in results:
                efficiency = result['throughput_mbps'] / max(r['throughput_mbps'] for r in results) * 100
                print(f"データサイズ {result['data_size']:6,} bytes: "
                      f"{result['throughput_mbps']:6.2f} MB/s (効率: {efficiency:5.1f}%)")

        return results

    def network_congestion_simulation(self):
        """ネットワーク輻輳のシミュレーション"""
        print("\\n=== ネットワーク輻輳シミュレーション ===")

        # 複数の同時接続でのパフォーマンス測定
        connection_counts = [1, 5, 10, 20]

        for conn_count in connection_counts:
            print(f"\\n同時接続数: {conn_count}")

            start_time = time.time()
            threads = []

            # 複数のクライアントを同時に起動
            for i in range(conn_count):
                thread = threading.Thread(
                    target=self.congestion_client,
                    args=(i, 1024)
                )
                threads.append(thread)
                thread.start()

            # 全スレッドの完了を待機
            for thread in threads:
                thread.join()

            end_time = time.time()
            total_duration = end_time - start_time

            print(f"  完了時間: {total_duration:.2f} 秒")
            print(f"  平均時間/接続: {total_duration/conn_count:.2f} 秒")

    def congestion_client(self, client_id, data_size):
        """輻輳テスト用クライアント"""
        try:
            # Google DNS への接続テスト（実際のネットワーク負荷テストではない）
            start_time = time.time()

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)

            # DNS クエリシミュレーション（実際には接続テストのみ）
            try:
                sock.connect(('8.8.8.8', 53))
                sock.close()
            except:
                pass

            end_time = time.time()
            duration = end_time - start_time

            print(f"    クライアント {client_id}: {duration:.3f} 秒")

        except Exception as e:
            print(f"    クライアント {client_id}: エラー - {e}")

    def find_free_port(self):
        """空いているポート番号を見つける"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('localhost', 0))
        port = sock.getsockname()[1]
        sock.close()
        return port

    def generate_performance_report(self):
        """パフォーマンス レポートを生成"""
        print("\\n=== ネットワークパフォーマンス レポート ===")

        print("\\n1. レイテンシ分析:")
        print("   - 接続確立時間の測定")
        print("   - ジッター（遅延のばらつき）の評価")
        print("   - RTT (Round Trip Time) の分析")

        print("\\n2. スループット分析:")
        print("   - データ転送速度の測定")
        print("   - 帯域幅利用効率の評価")
        print("   - 異なるデータサイズでの性能比較")

        print("\\n3. 信頼性分析:")
        print("   - パケットロス率の測定")
        print("   - 接続成功率の評価")
        print("   - エラー率の分析")

        print("\\n4. 負荷特性分析:")
        print("   - 同時接続数の影響")
        print("   - 輻輳制御の効果")
        print("   - スケーラビリティの評価")

        print("\\n最適化の推奨事項:")
        optimization_tips = [
            "1. TCP ウィンドウサイズの調整",
            "2. 送信バッファサイズの最適化",
            "3. Nagle アルゴリズムの設定調整",
            "4. キープアライブ設定の最適化",
            "5. 圧縮アルゴリズムの適用検討",
            "6. 接続プーリングの実装",
            "7. 非同期I/Oの活用",
            "8. ネットワーク品質監視の実装"
        ]

        for tip in optimization_tips:
            print(f"   {tip}")


def main():
    """メインデモ関数"""
    print("ネットワークパフォーマンス測定デモ")
    print("=" * 50)

    analyzer = NetworkPerformanceAnalyzer()

    # 1. レイテンシ測定（Google DNS）
    latency_result = analyzer.measure_latency('8.8.8.8', 53)

    # 2. 帯域利用効率テスト
    bandwidth_results = analyzer.bandwidth_utilization_test()

    # 3. ネットワーク輻輳シミュレーション
    analyzer.network_congestion_simulation()

    # 4. パフォーマンス レポート生成
    analyzer.generate_performance_report()

    print("\\n" + "=" * 50)
    print("ネットワークパフォーマンス測定完了")
    print("\\n重要なポイント:")
    print("- レイテンシとスループットは トレードオフの関係")
    print("- ネットワーク品質は環境により大きく変動")
    print("- 継続的な監視と最適化が重要")
    print("- アプリケーション要件に応じた調整が必要")


if __name__ == "__main__":
    main()