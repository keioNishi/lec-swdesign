-- データベースシステム講義 SQLサンプルコード
-- PostgreSQL用のSQLファイル

-- データベース作成
CREATE DATABASE university_system;

-- 大学管理システム用のテーブル群

-- 1. 学部テーブル
CREATE TABLE departments (
    dept_code CHAR(3) PRIMARY KEY,
    dept_name VARCHAR(50) NOT NULL
);

-- 2. 学生テーブル
CREATE TABLE students (
    student_id CHAR(7) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    grade INTEGER NOT NULL CHECK (grade BETWEEN 1 AND 4),
    dept_code CHAR(3),
    gpa DECIMAL(3,2) CHECK (gpa >= 0.00 AND gpa <= 4.00),
    email VARCHAR(100),
    phone_number VARCHAR(15),
    birth_date DATE NOT NULL,
    admission_year INTEGER NOT NULL,
    total_credits INTEGER DEFAULT 0,
    FOREIGN KEY (dept_code) REFERENCES departments(dept_code)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- 3. 科目テーブル
CREATE TABLE courses (
    course_code CHAR(6) PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    dept_code CHAR(3) NOT NULL,
    academic_year INTEGER NOT NULL,
    semester INTEGER NOT NULL,
    credits INTEGER NOT NULL DEFAULT 3,
    available_seats INTEGER NOT NULL DEFAULT 0 CHECK (available_seats >= 0),
    UNIQUE (course_name, dept_code, academic_year, semester),
    FOREIGN KEY (dept_code) REFERENCES departments(dept_code)
);

-- 4. 履修テーブル
CREATE TABLE enrollments (
    enrollment_id SERIAL PRIMARY KEY,
    student_id CHAR(7),
    course_code CHAR(6),
    academic_year INTEGER NOT NULL,
    semester INTEGER NOT NULL,
    grade CHAR(2),
    enrollment_date DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (course_code) REFERENCES courses(course_code)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    UNIQUE (student_id, course_code, academic_year, semester)
);

-- サンプルデータの挿入

-- 学部データ
INSERT INTO departments (dept_code, dept_name) VALUES
('CS', 'コンピュータ学部'),
('EC', '経済学部'),
('LA', '文学部'),
('EN', '工学部');

-- 学生データ
INSERT INTO students (student_id, name, grade, dept_code, gpa, email, birth_date, admission_year) VALUES
('2024001', '田中太郎', 3, 'CS', 3.5, 'tanaka@university.edu', '2003-04-15', 2022),
('2024002', '佐藤花子', 2, 'EC', 3.8, 'sato@university.edu', '2004-03-22', 2023),
('2024003', '山田次郎', 4, 'CS', 3.2, 'yamada@university.edu', '2002-07-10', 2021),
('2024004', '鈴木美咲', 1, 'LA', 3.6, 'suzuki@university.edu', '2005-01-08', 2024),
('2024005', '高橋一郎', 3, 'EN', 3.4, 'takahashi@university.edu', '2003-11-25', 2022);

-- 科目データ
INSERT INTO courses (course_code, course_name, dept_code, academic_year, semester, credits, available_seats) VALUES
('CS101', 'データベース論', 'CS', 2024, 1, 3, 50),
('CS102', 'アルゴリズム基礎', 'CS', 2024, 1, 3, 40),
('MA201', '数学', 'EC', 2024, 1, 2, 60),
('EXP11', '実験', 'CS', 2024, 2, 4, 20),
('EN301', '設計工学', 'EN', 2024, 1, 3, 30);

-- 履修データ
INSERT INTO enrollments (student_id, course_code, academic_year, semester, grade) VALUES
('2024001', 'CS101', 2024, 1, 'A'),
('2024001', 'EXP11', 2024, 2, 'B'),
('2024002', 'MA201', 2024, 1, 'B'),
('2024003', 'CS101', 2024, 1, 'A'),
('2024005', 'EN301', 2024, 1, 'A');

-- インデックスの作成
CREATE INDEX idx_student_name ON students(name);
CREATE INDEX idx_student_dept ON students(dept_code);
CREATE INDEX idx_course_dept ON courses(dept_code);
CREATE INDEX idx_enrollment_student ON enrollments(student_id);
CREATE INDEX idx_enrollment_course ON enrollments(course_code);

-- ビューの作成

-- 学生成績一覧ビュー
CREATE VIEW student_grades AS
SELECT
    s.student_id,
    s.name AS student_name,
    d.dept_name,
    c.course_name,
    e.grade,
    e.academic_year,
    e.semester
FROM students s
INNER JOIN departments d ON s.dept_code = d.dept_code
INNER JOIN enrollments e ON s.student_id = e.student_id
INNER JOIN courses c ON e.course_code = c.course_code
ORDER BY s.student_id, e.academic_year, e.semester;

-- 学部別統計ビュー
CREATE VIEW department_stats AS
SELECT
    d.dept_name,
    COUNT(s.student_id) AS student_count,
    ROUND(AVG(s.gpa), 2) AS avg_gpa,
    COUNT(e.enrollment_id) AS total_enrollments
FROM departments d
LEFT JOIN students s ON d.dept_code = s.dept_code
LEFT JOIN enrollments e ON s.student_id = e.student_id
GROUP BY d.dept_code, d.dept_name
ORDER BY avg_gpa DESC;

-- セキュリティ関連

-- ユーザーの作成
CREATE USER app_user WITH PASSWORD 'secure_password123';
CREATE USER report_user WITH PASSWORD 'report_pass789';
CREATE ROLE db_admin WITH
    LOGIN
    PASSWORD 'admin_password456'
    CREATEDB
    VALID UNTIL '2025-12-31';

-- 権限の設定
GRANT SELECT ON students TO report_user;
GRANT INSERT, UPDATE ON students TO app_user;
GRANT ALL PRIVILEGES ON students TO db_admin;

GRANT CONNECT ON DATABASE university_system TO app_user;
GRANT USAGE ON SCHEMA public TO app_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO report_user;

-- 行レベルセキュリティの例
ALTER TABLE students ENABLE ROW LEVEL SECURITY;

-- 学部ごとのアクセスポリシー
CREATE POLICY dept_isolation ON students
    FOR ALL TO dept_user
    USING (dept_code = current_setting('app.current_dept'));

-- トランザクションの例

-- 履修登録トランザクション
BEGIN;
-- 履修テーブルに登録
INSERT INTO enrollments (student_id, course_code, academic_year, semester)
VALUES ('2024001', 'CS102', 2024, 2);

-- 定員数を減算
UPDATE courses
SET available_seats = available_seats - 1
WHERE course_code = 'CS102';

-- 学生の履修単位数を増加
UPDATE students
SET total_credits = total_credits + 3
WHERE student_id = '2024001';

COMMIT;

-- クエリの例

-- 基本的なSELECT
SELECT * FROM students WHERE grade = 3;

-- JOIN を使った複合クエリ
SELECT
    s.student_id,
    s.name,
    d.dept_name,
    c.course_name,
    e.grade
FROM students s
INNER JOIN departments d ON s.dept_code = d.dept_code
INNER JOIN enrollments e ON s.student_id = e.student_id
INNER JOIN courses c ON e.course_code = c.course_code
WHERE e.academic_year = 2024
ORDER BY s.student_id, c.course_name;

-- 集約関数を使ったクエリ
SELECT
    d.dept_name,
    COUNT(*) AS student_count,
    AVG(s.gpa) AS avg_gpa
FROM departments d
INNER JOIN students s ON d.dept_code = s.dept_code
GROUP BY d.dept_code, d.dept_name
HAVING COUNT(*) >= 1
ORDER BY avg_gpa DESC;

-- サブクエリを使った例
SELECT student_id, name, gpa
FROM students
WHERE gpa > (SELECT AVG(gpa) FROM students);

-- EXISTS演算子の使用
SELECT s.student_id, s.name
FROM students s
WHERE EXISTS (
    SELECT 1 FROM enrollments e
    WHERE e.student_id = s.student_id
);

-- 成績優秀者の抽出（WITH句使用）
WITH dept_percentiles AS (
    SELECT
        dept_code,
        PERCENTILE_CONT(0.8) WITHIN GROUP (ORDER BY gpa) AS top_20_threshold
    FROM students
    GROUP BY dept_code
)
SELECT
    s.student_id,
    s.name,
    d.dept_name,
    s.gpa,
    '上位20%' AS performance_level
FROM students s
INNER JOIN departments d ON s.dept_code = d.dept_code
INNER JOIN dept_percentiles dp ON s.dept_code = dp.dept_code
WHERE s.gpa >= dp.top_20_threshold
ORDER BY d.dept_name, s.gpa DESC;

-- バックアップとリストア（コメントとして記載）
-- pg_dump -h localhost -U postgres -d university_system > university_backup.sql
-- pg_dump -h localhost -U postgres -d university_system -Fc > university_backup.custom
-- pg_dump -h localhost -U postgres -d university_system -t students > students_backup.sql

-- 暗号化の例
-- INSERT INTO students (student_id, name, ssn_encrypted)
-- VALUES ('2024006', 'テスト太郎',
--   crypt('123-45-6789', gen_salt('bf')));

-- パフォーマンス分析
-- EXPLAIN ANALYZE SELECT * FROM students WHERE name = '田中太郎';

-- その他の便利なクエリ

-- 重複する学部コードを除去して表示
SELECT DISTINCT dept_code FROM students;

-- 条件分岐を使った成績分布
SELECT
    d.dept_name,
    COUNT(*) AS total_students,
    SUM(CASE WHEN s.gpa >= 3.5 THEN 1 ELSE 0 END) AS excellent_students,
    SUM(CASE WHEN s.gpa BETWEEN 3.0 AND 3.49 THEN 1 ELSE 0 END) AS good_students,
    SUM(CASE WHEN s.gpa < 3.0 THEN 1 ELSE 0 END) AS needs_improvement
FROM departments d
INNER JOIN students s ON d.dept_code = s.dept_code
GROUP BY d.dept_code, d.dept_name
ORDER BY total_students DESC;

-- データベース情報の取得
SELECT
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_name = 'students'
ORDER BY ordinal_position;