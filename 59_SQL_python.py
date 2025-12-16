import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
load_dotenv()
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'university_system'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'your_password'),
    'port': os.getenv('DB_PORT', 5432)
}
def get_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.Error as e:
        print(f"接続エラー: {e}")
        return None
def insert_student(student_id, name, grade, dept_code, birth_date=None, admission_year=None, email=None, gpa=None):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cursor:
            query = """
                INSERT INTO students (student_id, name, grade, dept_code, birth_date, admission_year, email, gpa)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (student_id, name, grade, dept_code, birth_date, admission_year, email, gpa))
            conn.commit()
            print(f"学生 {name} を正常に登録しました")
            return True
    except psycopg2.Error as e:
        conn.rollback()
        print(f"挿入エラー: {e}")
        return False
    finally:
        conn.close()
def get_students_by_department(dept_code):
    conn = get_connection()
    if not conn:
        return []
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            query = """
                SELECT s.student_id, s.name, s.grade, d.dept_name
                FROM students s
                INNER JOIN departments d ON s.dept_code = d.dept_code
                WHERE s.dept_code = %s
                ORDER BY s.student_id
            """
            cursor.execute(query, (dept_code,))
            results = cursor.fetchall()
            return [dict(row) for row in results]
    except psycopg2.Error as e:
        print(f"検索エラー: {e}")
        return []
    finally:
        conn.close()

def get_all_students():
    """全ての学生を取得"""
    conn = get_connection()
    if not conn:
        return []
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            query = """
                SELECT s.student_id, s.name, s.grade, d.dept_name, s.gpa
                FROM students s
                INNER JOIN departments d ON s.dept_code = d.dept_code
                ORDER BY s.student_id
            """
            cursor.execute(query)
            results = cursor.fetchall()
            # total_creditsをダミーで追加（表示用）
            for row in results:
                row['total_credits'] = 0
            return [dict(row) for row in results]
    except psycopg2.Error as e:
        print(f"検索エラー: {e}")
        return []
    finally:
        conn.close()

def update_student_grade(student_id, new_grade):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cursor:
            # 更新前の確認
            cursor.execute(
                "SELECT name, grade FROM students WHERE student_id = %s",
                (student_id,)
            )
            old_data = cursor.fetchone()
            if not old_data:
                print("該当する学生が見つかりません")
                return False
            cursor.execute(
                "UPDATE students SET grade = %s WHERE student_id = %s",
                (new_grade, student_id)
            )
            if cursor.rowcount > 0:
                conn.commit()
                print(f"{old_data[0]}の学年を{old_data[1]}年→{new_grade}年に更新")
                return True
            else:
                print("更新対象が見つかりません")
                return False
    except psycopg2.Error as e:
        conn.rollback()
        print(f"更新エラー: {e}")
        return False
    finally:
        conn.close()

def delete_student(student_id):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cursor:
            # 削除前確認
            cursor.execute(
                "SELECT name FROM students WHERE student_id = %s",
                (student_id,)
            )
            student = cursor.fetchone()
            if not student:
                print("該当する学生が見つかりません")
                return False
            cursor.execute(
                "SELECT COUNT(*) FROM enrollments WHERE student_id = %s",
                (student_id,)
            )
            enrollment_count = cursor.fetchone()[0]
            if enrollment_count > 0:
                print(f"履修登録が{enrollment_count}件存在するため削除できません")
                return False
            cursor.execute(
                "DELETE FROM students WHERE student_id = %s",
                (student_id,)
            )
            conn.commit()
            print(f"学生 {student[0]} を削除しました")
            return True
    except psycopg2.Error as e:
        conn.rollback()
        print(f"削除エラー: {e}")
        return False
    finally:
        conn.close()
def register_course(student_id, course_code, academic_year, semester):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cursor:
            conn.autocommit = False
            cursor.execute(
                "SELECT course_name, available_seats FROM courses WHERE course_code = %s",
                (course_code,)
            )
            course_info = cursor.fetchone()
            if not course_info:
                raise Exception("科目が見つかりません")
            if course_info[1] <= 0:
                raise Exception(f"科目 {course_info[0]} は定員に達しています")
            cursor.execute(
                "SELECT 1 FROM enrollments WHERE student_id = %s AND course_code = %s AND academic_year = %s AND semester = %s",
                (student_id, course_code, academic_year, semester)
            )
            if cursor.fetchone():
                raise Exception("既に履修登録済みです")
            cursor.execute(
                "INSERT INTO enrollments (student_id, course_code, academic_year, semester) VALUES (%s, %s, %s, %s)",
                (student_id, course_code, academic_year, semester)
            )
            cursor.execute(
                "UPDATE courses SET available_seats = available_seats - 1 WHERE course_code = %s",
                (course_code,)
            )
            conn.commit()
            print(f"履修登録完了: {course_info[0]}")
            return True
    except Exception as e:
        conn.rollback()
        print(f"履修登録失敗: {e}")
        return False
    finally:
        conn.close()

def display_students(students):
    """学生リストを表示"""
    if not students:
        print("該当する学生が見つかりません")
        return

    print(f"\n{'学生番号':<10} {'氏名':<15} {'学年':<5} {'学部':<20} {'総単位':<10}")
    print("-" * 70)
    for student in students:
        student_id = student.get('student_id', '')
        name = student.get('name', '')
        grade = student.get('grade', '')
        dept_name = student.get('dept_name', '')
        total_credits = student.get('total_credits', 0)
        print(f"{student_id:<10} {name:<15} {grade:<5} {dept_name:<20} {total_credits:<10}")
    print(f"\n合計: {len(students)}名")

def get_all_courses():
    """全ての科目を取得"""
    conn = get_connection()
    if not conn:
        return []
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            query = """
                SELECT c.course_code, c.course_name, c.dept_code,
                       d.dept_name, c.academic_year, c.semester,
                       c.credits, c.available_seats
                FROM courses c
                LEFT JOIN departments d ON c.dept_code = d.dept_code
                ORDER BY c.course_code
            """
            cursor.execute(query)
            results = cursor.fetchall()
            return [dict(row) for row in results]
    except psycopg2.Error as e:
        print(f"検索エラー: {e}")
        return []
    finally:
        conn.close()

def display_courses(courses):
    """科目リストを表示"""
    if not courses:
        print("科目が登録されていません")
        return

    print(f"\n{'科目コード':<12} {'科目名':<30} {'学部':<15} {'年度':<6} {'学期':<6} {'単位':<6} {'定員':<6}")
    print("-" * 95)
    for course in courses:
        course_code = course.get('course_code', '')
        course_name = course.get('course_name', '')
        dept_name = course.get('dept_name', 'N/A')
        academic_year = course.get('academic_year', 0)
        semester = course.get('semester', 0)
        credits = course.get('credits', 0)
        available_seats = course.get('available_seats', 0)
        semester_name = '前期' if semester == 1 else '後期' if semester == 2 else str(semester)
        print(f"{course_code:<12} {course_name:<30} {dept_name:<15} {academic_year:<6} {semester_name:<6} {credits:<6} {available_seats:<6}")
    print(f"\n合計: {len(courses)}科目")

def insert_course(course_code, course_name, dept_code, academic_year, semester, credits, available_seats):
    """科目を登録"""
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cursor:
            query = """
                INSERT INTO courses (course_code, course_name, dept_code, academic_year, semester, credits, available_seats)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (course_code, course_name, dept_code, academic_year, semester, credits, available_seats))
            conn.commit()
            print(f"科目 {course_name} を正常に登録しました")
            return True
    except psycopg2.Error as e:
        conn.rollback()
        print(f"科目登録エラー: {e}")
        return False
    finally:
        conn.close()

def delete_course(course_code):
    """科目を削除"""
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cursor:
            # 削除前確認
            cursor.execute(
                "SELECT course_name FROM courses WHERE course_code = %s",
                (course_code,)
            )
            course = cursor.fetchone()
            if not course:
                print("該当する科目が見つかりません")
                return False

            # 履修登録の確認
            cursor.execute(
                "SELECT COUNT(*) FROM enrollments WHERE course_code = %s",
                (course_code,)
            )
            enrollment_count = cursor.fetchone()[0]
            if enrollment_count > 0:
                print(f"履修登録が{enrollment_count}件存在するため削除できません")
                return False

            cursor.execute(
                "DELETE FROM courses WHERE course_code = %s",
                (course_code,)
            )
            conn.commit()
            print(f"科目 {course[0]} を削除しました")
            return True
    except psycopg2.Error as e:
        conn.rollback()
        print(f"削除エラー: {e}")
        return False
    finally:
        conn.close()

def get_enrollment_stats():
    """履修統計を表示"""
    conn = get_connection()
    if not conn:
        return
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            query = """
                SELECT
                    c.course_name,
                    COUNT(e.student_id) as enrollment_count,
                    c.available_seats,
                    c.credits
                FROM courses c
                LEFT JOIN enrollments e ON c.course_code = e.course_code
                GROUP BY c.course_code, c.course_name, c.available_seats, c.credits
                ORDER BY enrollment_count DESC
            """
            cursor.execute(query)
            results = cursor.fetchall()

            if not results:
                print("履修データが見つかりません")
                return

            print(f"\n{'科目名':<30} {'履修者数':<10} {'空席':<10} {'単位':<5}")
            print("-" * 60)
            for row in results:
                course_name = row['course_name']
                enrollment_count = row['enrollment_count']
                available_seats = row['available_seats']
                credits = row['credits']
                print(f"{course_name:<30} {enrollment_count:<10} {available_seats:<10} {credits:<5}")
    except psycopg2.Error as e:
        print(f"統計取得エラー: {e}")
    finally:
        conn.close()

def main():
    """学生管理システムのメイン処理"""
    while True:
        print("\n=== 学生管理システム ===")
        print("1. 学生一覧表示")
        print("2. 学生登録")
        print("3. 科目一覧表示")
        print("4. 科目登録")
        print("5. 科目削除")
        print("6. 履修登録")
        print("7. 成績統計")
        print("8. 終了")
        choice = input("選択してください (1-8): ").strip()

        if choice == '1':
            dept = input("学部コードを入力 (空白で全て): ").strip()
            dept = dept.ljust(3) if dept else dept
            students = get_students_by_department(dept) if dept else get_all_students()
            display_students(students)
        elif choice == '2':
            student_id = input("学生番号: ").strip()
            name = input("氏名: ").strip()
            grade = int(input("学年: ").strip())
            dept_code = input("学部コード: ").strip().ljust(3)
            birth_date = input("生年月日 (YYYY-MM-DD、空白可): ").strip() or None
            admission_year = input("入学年度 (空白可): ").strip()
            admission_year = int(admission_year) if admission_year else None
            email = input("メールアドレス (空白可): ").strip() or None
            gpa = input("GPA (空白可): ").strip()
            gpa = float(gpa) if gpa else None
            insert_student(student_id, name, grade, dept_code, birth_date, admission_year, email, gpa)
        elif choice == '3':
            courses = get_all_courses()
            display_courses(courses)
        elif choice == '4':
            course_code = input("科目コード: ").strip()
            course_name = input("科目名: ").strip()
            dept_code = input("学部コード: ").strip().ljust(3)
            academic_year = int(input("年度: ").strip())
            semester = int(input("学期 (1=前期, 2=後期): ").strip())
            credits = int(input("単位数: ").strip())
            available_seats = int(input("定員: ").strip())
            insert_course(course_code, course_name, dept_code, academic_year, semester, credits, available_seats)
        elif choice == '5':
            course_code = input("削除する科目コード: ").strip()
            delete_course(course_code)
        elif choice == '6':
            student_id = input("学生番号: ").strip()
            course_code = input("科目コード: ").strip()
            year = int(input("履修年度: ").strip())
            semester = int(input("学期 (1=前期, 2=後期): ").strip())
            register_course(student_id, course_code, year, semester)
        elif choice == '7':
            get_enrollment_stats()
        elif choice == '8':
            print("システムを終了します")
            break
        else:
            print("無効な選択です")
if __name__ == "__main__":
    main()

