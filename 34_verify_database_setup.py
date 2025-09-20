"""データベース検証スクリプト
Neon上の講義用データベースが想定どおりに準備されているかを確認します。
"""

import logging
import sys
from typing import List, Tuple

import psycopg2
from psycopg2 import DatabaseError

# 画面とログファイルの両方へ情報を出力する設定
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("db_test.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

def verify_database() -> bool:
    """講義用データベースが期待する構造とデータを持っているか検証する。"""
    config = {
        "host": "ep-plain-cell-a1ui80qe-pooler.ap-southeast-1.aws.neon.tech",
        "port": 5432,
        "database": "lecture",
        "user": "neondb_owner",
        "password": "npg_tV7H1PezbcqO",
    }

    try:
        with psycopg2.connect(**config) as connection:
            with connection.cursor() as cursor:
                logger.info("Neonデータベースに接続しました")

                print("\n" + "=" * 60)
                print("1. テーブル構造の確認")
                print("=" * 60)

                schema_query = """
                    SELECT table_name, column_name, data_type, is_nullable, column_default
                    FROM information_schema.columns
                    WHERE table_schema = 'public'
                    ORDER BY table_name, ordinal_position;
                """
                cursor.execute(schema_query)
                current_table = None
                for table_name, column_name, data_type, is_nullable, default in cursor.fetchall():
                    if table_name != current_table:
                        current_table = table_name
                        print(f"\nテーブル: {table_name}")
                        print("-" * 30)
                    default_text = str(default)[:30] if default else ""
                    print(f"  {column_name:15} {data_type:15} {is_nullable:8} {default_text}")

                print("\n" + "=" * 60)
                print("2. サンプルデータの確認")

                sample_queries: List[Tuple[str, str]] = [
                    ("学部一覧", "SELECT dept_code, dept_name FROM departments ORDER BY dept_code LIMIT 5;"),
                    ("学生一覧", "SELECT student_id, name, grade, dept_code, gpa FROM students ORDER BY student_id LIMIT 5;"),
                    ("履修状況", "SELECT student_id, course_code, grade FROM enrollments ORDER BY student_id LIMIT 5;"),
                ]
                for title, query in sample_queries:
                    print(f"\n{title}:")
                    cursor.execute(query)
                    rows = cursor.fetchall()
                    if rows:
                        for row in rows:
                            print(f"  {row}")
                    else:
                        print("  結果なし")

                print("\n" + "=" * 60)
                print("3. 集計クエリの確認")

                summary_queries: List[Tuple[str, str]] = [
                    (
                        "学部別の学生数",
                        """
                        SELECT d.dept_name, COUNT(s.student_id) AS student_count
                        FROM departments d
                        LEFT JOIN students s ON d.dept_code = s.dept_code
                        GROUP BY d.dept_name
                        ORDER BY d.dept_name;
                        """,
                    ),
                    (
                        "履修科目数",
                        """
                        SELECT student_id, COUNT(*) AS course_count
                        FROM enrollments
                        GROUP BY student_id
                        ORDER BY student_id;
                        """,
                    ),
                ]
                all_green = True
                for title, query in summary_queries:
                    print(f"\n{title}:")
                    try:
                        cursor.execute(query)
                        rows = cursor.fetchall()
                        if rows:
                            for row in rows:
                                print(f"  {row}")
                        else:
                            print("  結果なし")
                    except DatabaseError as exc:
                        all_green = False
                        logger.error("%s の実行でエラーが発生しました: %s", title, exc)
                        connection.rollback()

                print("\n" + "=" * 60)
                print("4. インデックスの確認")

                cursor.execute(
                    """
                    SELECT indexname, tablename, indexdef
                    FROM pg_indexes
                    WHERE schemaname = 'public'
                    ORDER BY tablename, indexname;
                    """
                )
                indexes = cursor.fetchall()
                if indexes:
                    for index_name, table_name, index_def in indexes:
                        print(f"  {table_name}.{index_name}")
                        print(f"    {index_def}")
                        print()
                else:
                    print("  インデックスは定義されていません")

                logger.info("検証が完了しました")
                return all_green

    except DatabaseError as exc:
        logger.error("検証中にデータベースエラーが発生しました: %s", exc)
        return False
    except Exception as exc:  # psycopg2以外の例外も補足
        logger.error("予期しないエラーが発生しました: %s", exc)
        return False

def main() -> None:
    """コマンドラインから検証を実行するエントリーポイント。"""
    print("=" * 60)
    print("大学管理システム - データベース検証")
    print("=" * 60)

    success = verify_database()

    print("\n" + "=" * 60)
    if success:
        print("[SUCCESS] データベース検証が完了しました")
    else:
        print("[ERROR] 検証中に問題が発生しました")
        sys.exit(1)
    print("=" * 60)

if __name__ == "__main__":
    main()
