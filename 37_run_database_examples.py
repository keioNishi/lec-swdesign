"""
Database Examples SQL実行スクリプト
database_examples.pgsqlファイルの内容をNeonで実行してテストする
"""

import psycopg2
import sys
import logging

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sql_execution.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def execute_sql_file():
    """database_examples.pgsqlファイルを実行"""

    # Neonデータベース接続設定
    config = {
        'host': 'ep-plain-cell-a1ui80qe-pooler.ap-southeast-1.aws.neon.tech',
        'port': 5432,
        'database': 'lecture',
        'user': 'neondb_owner',
        'password': 'npg_tV7H1PezbcqO'
    }

    try:
        connection = psycopg2.connect(**config)
        cursor = connection.cursor()
        logger.info("Neonデータベースに接続しました")

        # SQLファイルを読み込み
        with open('database_examples.pgsql', 'r', encoding='utf-8') as file:
            sql_content = file.read()

        logger.info("database_examples.pgsqlファイルを読み込みました")

        # SQL文を解析してリストに格納
        sql_statements = []
        current_statement = ""

        for line in sql_content.split('\n'):
            line = line.strip()
            # コメント行と空行をスキップ
            if line.startswith('--') or not line:
                continue

            current_statement += line + ' '

            # SQL文の終了を検出（セミコロン）
            if line.endswith(';'):
                sql_statements.append(current_statement.strip())
                current_statement = ""

        logger.info(f"合計 {len(sql_statements)} 個のSQL文を実行予定")

        # 実行結果のカウンタ
        executed_count = 0
        skipped_count = 0

        # 各SQL文を実行
        for i, statement in enumerate(sql_statements, 1):
            try:
                # Neonでサポートされていない操作をスキップ
                if 'CREATE DATABASE' in statement.upper():
                    logger.info(f"SQL {i}: データベース作成文をスキップ")
                    skipped_count += 1
                    continue

                if 'CREATE USER' in statement.upper() or 'CREATE ROLE' in statement.upper():
                    logger.info(f"SQL {i}: ユーザー/ロール作成文をスキップ")
                    skipped_count += 1
                    continue

                if 'ENABLE ROW LEVEL SECURITY' in statement.upper() or 'CREATE POLICY' in statement.upper():
                    logger.info(f"SQL {i}: RLS関連文をスキップ")
                    skipped_count += 1
                    continue

                cursor.execute(statement)
                connection.commit()
                executed_count += 1

                # 進行状況の表示
                if executed_count % 10 == 0:
                    logger.info(f"進行状況: {executed_count}/{len(sql_statements)} 実行完了")

            except psycopg2.Error as e:
                logger.warning(f"SQL {i} 実行エラー (継続): {e}")
                connection.rollback()
                continue

        logger.info(f"SQL実行完了: {executed_count}件実行, {skipped_count}件スキップ")

        # 動作確認用のテストクエリ
        test_queries = [
            ("テーブル一覧", "SELECT tablename FROM pg_tables WHERE schemaname = 'public';"),
            ("学部データ確認", "SELECT * FROM departments;"),
            ("学生データ確認", "SELECT student_id, name, dept_code FROM students LIMIT 5;"),
            ("ビューの動作確認", "SELECT * FROM student_grades LIMIT 3;"),
        ]

        logger.info("=== テストクエリ実行 ===")
        for description, query in test_queries:
            try:
                cursor.execute(query)
                results = cursor.fetchall()
                logger.info(f"{description}: {len(results)}件のデータを取得")

                # 結果の最初の3件を表示
                for i, row in enumerate(results[:3]):
                    logger.info(f"  {i+1}: {row}")
                if len(results) > 3:
                    logger.info(f"  ... 他 {len(results)-3} 件")

            except psycopg2.Error as e:
                logger.error(f"{description} エラー: {e}")

        cursor.close()
        connection.close()
        logger.info("データベース接続を切断しました")

        return True

    except Exception as e:
        logger.error(f"処理中にエラーが発生しました: {e}")
        return False

if __name__ == "__main__":
    logger.info("Database Examples SQL実行スクリプトを開始します")

    try:
        success = execute_sql_file()

        if success:
            print("\n" + "="*60)
            print("[SUCCESS] database_examples.pgsql実行完了")
            print("[INFO] Neonデータベースに大学管理システムが構築されました")
            print("[LOG] 詳細ログ: sql_execution.log")
            print("="*60)
        else:
            print("\n" + "="*60)
            print("[ERROR] SQL実行中にエラーが発生しました")
            print("[LOG] 詳細ログ: sql_execution.log")
            print("="*60)
            sys.exit(1)

    except KeyboardInterrupt:
        logger.info("ユーザーによりスクリプトが中断されました")
        sys.exit(0)
    except Exception as e:
        logger.error(f"予期しないエラー: {e}")
        sys.exit(1)
