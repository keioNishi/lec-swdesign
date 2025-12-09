"""PostgreSQL接続テストスクリプト
大学のサンプルデータベースに接続して基本的な操作を確認します。
"""

import logging
import sys
from typing import List, Tuple

import psycopg2
from psycopg2 import OperationalError, DatabaseError, extensions

# ログをファイルと標準出力に送る基本設定
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("db_test.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

class PostgreSQLTester:
    """PostgreSQLへの接続とテストを管理するクラス。"""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 5432,
        database: str = "postgres",
        user: str = "postgres",
        password: str = "postgres",
    ) -> None:
        """接続に必要な設定を保持する。"""
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        # run_all_tests内で接続を生成するため、最初は空にしておく
        self.connection: psycopg2.extensions.connection | None = None
        self.cursor: psycopg2.extensions.cursor | None = None

    def connect(self) -> bool:
        """データベースに接続し、成功を真偽値で返す。"""
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password,
            )
            self.cursor = self.connection.cursor()
            logger.info("PostgreSQLに正常に接続しました: %s@%s:%s", self.database, self.host, self.port)
            return True
        except OperationalError as exc:
            logger.error("データベース接続エラー: %s", exc)
            self.connection = None
            self.cursor = None
            return False

    def disconnect(self) -> None:
        """開いているカーソルと接続を安全に閉じる。"""
        if self.cursor is not None:
            self.cursor.close()
            self.cursor = None
        if self.connection is not None:
            self.connection.close()
            self.connection = None
        logger.info("データベース接続を切断しました")

    def test_connection(self) -> bool:
        """基本的な接続操作が行えるか確認する。"""
        if self.cursor is None:
            logger.error("接続が確立されていません")
            return False

        try:
            self.cursor.execute("SELECT version();")
            version = self.cursor.fetchone()[0]
            logger.info("PostgreSQLバージョン: %s", version)

            self.cursor.execute("SELECT NOW();")
            current_time = self.cursor.fetchone()[0]
            logger.info("現在時刻: %s", current_time)

            self.cursor.execute("SELECT current_database(), current_user;")
            database_name, current_user = self.cursor.fetchone()
            logger.info("接続先データベース: %s / 利用ユーザー: %s", database_name, current_user)
            return True
        except DatabaseError as exc:
            logger.error("基本クエリの実行でエラーが発生しました: %s", exc)
            return False

    def create_university_database(self) -> bool:
        """講義用のデータベースを作成する（既存ならそのまま使う）。"""
        if self.connection is None or self.cursor is None:
            logger.error("接続が確立されていません")
            return False

        logger.info("=== 大学管理データベースの存在確認 ===")
        saved_level = self.connection.isolation_level
        try:
            self.connection.commit()
        except DatabaseError:
            self.connection.rollback()

        try:
            self.connection.set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT)
            self.cursor.execute(
                "SELECT 1 FROM pg_database WHERE datname = 'university_system';"
            )
            exists = self.cursor.fetchone()
            if exists:
                logger.info("university_systemデータベースは既に存在します")
                return True

            self.cursor.execute("CREATE DATABASE university_system;")
            logger.info("university_systemデータベースを作成しました")
            return True
        except DatabaseError as exc:
            logger.error("大学用データベースの作成でエラーが発生しました: %s", exc)
            return False
        finally:
            self.connection.set_isolation_level(saved_level)

    def run_sample_sql(self) -> bool:
        """サンプルSQLを実行し、DDLとDMLが成功するか試す。"""
        if self.connection is None or self.cursor is None:
            logger.error("接続が確立されていません")
            return False

        logger.info("=== サンプルSQLの確認 ===")
        sample_checks: List[Tuple[str, str]] = [
            ("公開スキーマのテーブル数", "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';"),
            ("公開スキーマの代表的なテーブル", "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name LIMIT 5;"),
        ]

        for title, query in sample_checks:
            try:
                self.cursor.execute(query)
                rows = self.cursor.fetchall()
                logger.info("[%s] %s", title, rows if len(rows) > 1 else rows[0] if rows else "結果なし")
            except DatabaseError as exc:
                logger.error("[%s] SQLの実行でエラーが発生しました: %s", title, exc)
                return False
        return True

    def test_sample_queries(self) -> bool:
        """想定した問い合わせが動くか確認する。"""
        if self.cursor is None:
            logger.error("接続が確立されていません")
            return False

        logger.info("=== サンプルクエリの確認 ===")
        queries: List[Tuple[str, str]] = [
            ("学部一覧", "SELECT dept_code, dept_name FROM departments ORDER BY dept_code;"),
            ("学生の所属", "SELECT student_id, name, dept_code FROM students ORDER BY student_id;"),
            ("GPA上位の学生", "SELECT name, gpa FROM students WHERE gpa >= 3.5 ORDER BY gpa DESC;"),
            (
                "履修状況",
                """
                SELECT s.name, e.course_code, e.grade
                FROM students s
                JOIN enrollments e ON s.student_id = e.student_id
                ORDER BY s.student_id, e.course_code;
                """,
            ),
        ]

        success = True
        for title, query in queries:
            try:
                self.cursor.execute(query)
                rows = self.cursor.fetchall()
                logger.info("[%s] %d件取得", title, len(rows))
            except DatabaseError as exc:
                logger.error("[%s] クエリ実行でエラーが発生しました: %s", title, exc)
                success = False
        return success

    def run_all_tests(self) -> bool:
        """すべてのテストを順番に実行し、結果をまとめる。"""
        logger.info("=== PostgreSQL接続テストを開始 ===")

        if not self.connect():
            return False

        success = True
        try:
            if not self.test_connection():
                success = False
            if success:
                if not self.create_university_database():
                    logger.warning("大学用データベースの作成に失敗しました。既存のデータを利用して続行します。")
                if success and not self.run_sample_sql():
                    success = False
            if success and not self.test_sample_queries():
                success = False

            if success:
                logger.info("=== 全テスト成功 ===")
            else:
                logger.error("=== テスト失敗 ===")
            return success
        finally:
            self.disconnect()

def main() -> None:
    """コマンドラインからテストを実行するエントリーポイント。"""
    logger.info("PostgreSQL接続テストスクリプトを開始します")

    config = {
        "host": "ep-plain-cell-a1ui80qe-pooler.ap-southeast-1.aws.neon.tech",
        "port": 5432,
        "database": "lecture",
        "user": "neondb_owner",
        "password": "npg_tV7H1PezbcqO",
    }

    tester = PostgreSQLTester(**config)

    try:
        success = tester.run_all_tests()
        print("\n" + "=" * 50)
        if success:
            print("[SUCCESS] PostgreSQL接続テスト完了")
        else:
            print("[ERROR] テスト中に問題が発生しました")
        print("[LOG] 詳細は db_test.log を確認してください")
        print("=" * 50)
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        logger.info("ユーザーによってテストが中断されました")
        tester.disconnect()
        sys.exit(0)
    except Exception as exc:
        logger.error("予期しないエラーが発生しました: %s", exc)
        tester.disconnect()
        sys.exit(1)

if __name__ == "__main__":
    main()
