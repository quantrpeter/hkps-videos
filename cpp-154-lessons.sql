-- C++ 154講 lessons for LearnHub course 5066
-- https://www.hkprog.org/learn/?lh_course=5066
--
-- Import in phpMyAdmin (database of hkprog.org), or: mysql DB_NAME < cpp-154-lessons.sql
-- Tables use the wp_ prefix. The plugin already queries wp_frmt_form_entry_meta, so this is the live prefix.
-- Re-running deletes only hkps_lh_lesson rows whose _hkps_lh_course is 5066, then inserts these 154.
-- It does not touch 香農信息論 or any other course.
-- Each video is already shared as “anyone with the link can view”.

SET NAMES utf8mb4;
SET @now := NOW();
SET @gmt := UTC_TIMESTAMP();

SELECT ID, post_type, post_status, post_title
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course';

SET @course_ok := (
  SELECT COUNT(*) FROM wp_posts
  WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND post_title = 'C++ 154講'
);
-- @course_ok must be 1. If it is 0, the rest of this script changes nothing.

START TRANSACTION;

DELETE p, pm
FROM wp_posts AS p
INNER JOIN wp_postmeta AS course
  ON course.post_id = p.ID
 AND course.meta_key = '_hkps_lh_course'
 AND course.meta_value = '5066'
LEFT JOIN wp_postmeta AS pm ON pm.post_id = p.ID
WHERE p.post_type = 'hkps_lh_lesson'
  AND @course_ok = 1;

-- Part 0 起步
INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '0.1 C++ 係乜嘢？', '第1堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-001', '', '', @now, @gmt, '', 0, '', 1, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1hJNVOOZHXclCYycj4BynlMrPrsI8smXj/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '0.2 安裝開發環境', '第2堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-002', '', '', @now, @gmt, '', 0, '', 2, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1uF7DFpyU4auUHpYxNvAYeQGS4zRYG1iG/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '0.3 Hello, World!', '第3堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-003', '', '', @now, @gmt, '', 0, '', 3, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1YE20YjRaIMW5ER-0i_uEV5UwFOM2E6Fu/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '0.4 編譯係點運作', '第4堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-004', '', '', @now, @gmt, '', 0, '', 4, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1fdQOnpqqeT9fog0FUqKgZQHaUql589Hj/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '0.5 睇得明編譯錯誤', '第5堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-005', '', '', @now, @gmt, '', 0, '', 5, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1L8M1Uk9Q-7IF7-WvIRx2tn-StmXNuj7V/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '0.6 註解同寫碼風格', '第6堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-006', '', '', @now, @gmt, '', 0, '', 6, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1-EFhss1nwf67KFLBI51kixjl5qwzMOcq/view' FROM DUAL WHERE @lesson_id <> 0;

-- Part 1 變數、型別同運算
INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '1.1 變數：俾資料一個名', '第7堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-007', '', '', @now, @gmt, '', 0, '', 7, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/13GlOfo0f63gX-d87L1PqfXT-Z0EorlTt/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '1.2 初始化', '第8堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-008', '', '', @now, @gmt, '', 0, '', 8, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1eAKB_FBdnPc-zq_fkMLx4sxNkdEOG-iw/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '1.3 基本型別', '第9堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-009', '', '', @now, @gmt, '', 0, '', 9, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1YzzkFoQKT89Ws_2c_Z1Vff3xTc8dVRHE/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '1.4 用 cin 讀輸入', '第10堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-010', '', '', @now, @gmt, '', 0, '', 10, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1Y8xBTBJ6oUGSJbZCCrKAztWcdzJdhcHY/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '1.5 算術運算', '第11堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-011', '', '', @now, @gmt, '', 0, '', 11, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/15evGWmd9GrcMJZbL_fFNUv3fwqVQGcTO/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '1.6 整數溢位', '第12堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-012', '', '', @now, @gmt, '', 0, '', 12, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1M4MUfCd92T6bjIrxRtzKoQZFAeFTqHaK/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '1.7 浮點數同精度', '第13堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-013', '', '', @now, @gmt, '', 0, '', 13, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1o8z7s2hxKoffBR0_qtl98BDZbodY0zxI/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '1.8 型別轉換', '第14堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-014', '', '', @now, @gmt, '', 0, '', 14, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1P7lr9mdfU5yrDD9lKUnIjktew2us7ZY5/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '1.9 const 同 constexpr', '第15堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-015', '', '', @now, @gmt, '', 0, '', 15, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1LJf19rWaQ3gcVQs3c1l1s_RDBEYq4d-B/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '1.10 auto', '第16堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-016', '', '', @now, @gmt, '', 0, '', 16, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1hxZ1de4kaDnHEOf6EnaVDF0oQ2D-Mk5R/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '1.11 std::string 入門', '第17堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-017', '', '', @now, @gmt, '', 0, '', 17, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1OIHWkCAnDNzEPeQGDUQKVFCno2FVIHlg/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '1.12 小項目：BMI 計算機', '第18堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-018', '', '', @now, @gmt, '', 0, '', 18, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/14AfV-LQcX4ecFvMa_BQ3bIy0LIlZ0CKi/view' FROM DUAL WHERE @lesson_id <> 0;

-- Part 2 流程控制
INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '2.1 if / else', '第19堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-019', '', '', @now, @gmt, '', 0, '', 19, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1YTnjdVUNvINlAMNj6bD5mNYsThnbwzTw/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '2.2 邏輯運算', '第20堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-020', '', '', @now, @gmt, '', 0, '', 20, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/17YJO7O7Ah9RZEpTE2lHaCLzCMISDHOko/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '2.3 else if 同巢狀 if', '第21堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-021', '', '', @now, @gmt, '', 0, '', 21, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1CnC_nnsdxB7oJvVpfUAJTMmlUEh2GAub/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '2.4 switch', '第22堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-022', '', '', @now, @gmt, '', 0, '', 22, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1udpkWce8qxWjuQIMkUJ_slAl1pOgeyT6/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '2.5 條件運算子', '第23堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-023', '', '', @now, @gmt, '', 0, '', 23, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1DjNqHyykw0hsaWujsTbI8T8eehE3zSvK/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '2.6 while 迴圈', '第24堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-024', '', '', @now, @gmt, '', 0, '', 24, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1Jv6sL-g3B7KYmzpFqtrW5vFY6XoLkUsm/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '2.7 for 迴圈', '第25堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-025', '', '', @now, @gmt, '', 0, '', 25, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1mzynk-ausDtP4tf5PxC1xqTop2AEAH_X/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '2.8 do-while、break、continue', '第26堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-026', '', '', @now, @gmt, '', 0, '', 26, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1M6K54rUdkMRkEmUyCLPedo9pIphIxXcX/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '2.9 巢狀迴圈', '第27堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-027', '', '', @now, @gmt, '', 0, '', 27, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1EJlSAVb0cWU7dGKXhPwAgyvh5Pk06a-n/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '2.10 隨機數', '第28堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-028', '', '', @now, @gmt, '', 0, '', 28, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1mTNbV2e2WOC3lrYj_ggYp5WvUdAfLtxa/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '2.11 小項目：估數字', '第29堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-029', '', '', @now, @gmt, '', 0, '', 29, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1jPts6WsiY_0Kuyao4XkpKopX69zpfsVW/view' FROM DUAL WHERE @lesson_id <> 0;

-- Part 3 函數
INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '3.1 點解要用函數', '第30堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-030', '', '', @now, @gmt, '', 0, '', 30, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1eOOnPlONHq35Y8mJ7Y_w61tOJPoxTKRC/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '3.2 參數同回傳值', '第31堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-031', '', '', @now, @gmt, '', 0, '', 31, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/12JGDloG5KK03VE-Pkqodom9Y0WQiE8Eq/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '3.3 宣告同定義', '第32堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-032', '', '', @now, @gmt, '', 0, '', 32, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/14GTUFwQft6Y4rJLI1biXWgLjNT2wzFRP/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '3.4 傳值', '第33堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-033', '', '', @now, @gmt, '', 0, '', 33, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1cXipuyCVtzhQnCIh8J9OF4aEDKu3pVtZ/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '3.5 Reference 入門', '第34堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-034', '', '', @now, @gmt, '', 0, '', 34, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1ZBSjYMeCgWCEJdPA2iLhfETep5xdAOiE/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '3.6 傳參考同 const reference', '第35堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-035', '', '', @now, @gmt, '', 0, '', 35, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1cdBDWh5HYWGBwQMDKVuvi7Ap6dYJQUIs/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '3.7 預設參數同多載', '第36堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-036', '', '', @now, @gmt, '', 0, '', 36, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1tBjuYj_5RL3nZGfi6I7AvXf-bYp65KvT/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '3.8 作用域同生命週期', '第37堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-037', '', '', @now, @gmt, '', 0, '', 37, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1Bvzt8dbMYGuRgZSC0zQAGWZW_XhyR2lb/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '3.9 遞迴', '第38堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-038', '', '', @now, @gmt, '', 0, '', 38, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1xjRKpX2WM3CuvdwnLw0QYsy8T3QpM_OJ/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '3.10 拆開多個檔案', '第39堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-039', '', '', @now, @gmt, '', 0, '', 39, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1vLQm03WBW6AiJ7xHKVsxGfk72BMM_H_T/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '3.11 namespace', '第40堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-040', '', '', @now, @gmt, '', 0, '', 40, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1ZPrsxAuNsoHcC1TNpW7dc3mcqkUgoILq/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '3.12 小項目：計數機', '第41堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-041', '', '', @now, @gmt, '', 0, '', 41, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/18nQ4VUzesjVHIoVgMrGg2DDp2vaWu27v/view' FROM DUAL WHERE @lesson_id <> 0;

-- Part 4 vector 同字串
INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '4.1 vector 入門', '第42堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-042', '', '', @now, @gmt, '', 0, '', 42, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/14bAofx75_tQD-jMW87W8OBgLvcxVyJRT/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '4.2 Range-based for', '第43堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-043', '', '', @now, @gmt, '', 0, '', 43, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1R_C44PTKKP0HXkjnLJqAEEL3zurnR1AZ/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '4.3 vector 常用操作', '第44堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-044', '', '', @now, @gmt, '', 0, '', 44, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1Gr5zPyu0ZviXDHefd2gOUSAaE--6FQwk/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '4.4 二維 vector', '第45堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-045', '', '', @now, @gmt, '', 0, '', 45, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1tqUihQqJPCPUHLnggN5vK35j2Ri66ebl/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '4.5 C 風格陣列', '第46堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-046', '', '', @now, @gmt, '', 0, '', 46, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1wdw-XTDtkL3uHICDbU-JJosaT8p8LRdF/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '4.6 std::array', '第47堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-047', '', '', @now, @gmt, '', 0, '', 47, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1y6Ym2SZGm6ZDZSFRpfoWMI9EiAs7vGSb/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '4.7 字串操作', '第48堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-048', '', '', @now, @gmt, '', 0, '', 48, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1ML9uYb7lMmmTL8iZFGTKqygnPsoXleW0/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '4.8 字元同中文字', '第49堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-049', '', '', @now, @gmt, '', 0, '', 49, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1ryi0PvhXUEz8cDbdHNiUg8413CqcNsUZ/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '4.9 自己寫搜尋同排序', '第50堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-050', '', '', @now, @gmt, '', 0, '', 50, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1WU65drv-XbOg5fHN2ek04ZV1n-6qPOaq/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '4.10 小項目：井字過三關', '第51堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-051', '', '', @now, @gmt, '', 0, '', 51, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1hEge1_G1toqpehzzx4LnTSQtSOiQx0Ex/view' FROM DUAL WHERE @lesson_id <> 0;

-- Part 5 指標同記憶體
INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '5.1 記憶體同地址', '第52堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-052', '', '', @now, @gmt, '', 0, '', 52, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1fVFOJZkjoREa_So_LInSXGUIawZyIstG/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '5.2 指標入門', '第53堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-053', '', '', @now, @gmt, '', 0, '', 53, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/19wMwyrOKyh6uHLRhlfyKTPdZ6Qx4e_fB/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '5.3 指標 vs reference', '第54堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-054', '', '', @now, @gmt, '', 0, '', 54, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1Zic7S3UFhjfQnUV59I4kjy15B4Nyitvb/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '5.4 nullptr 同懸空指標', '第55堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-055', '', '', @now, @gmt, '', 0, '', 55, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1dYcCIfYQnp6PDuM-NdkVFxTK_LY5KnW0/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '5.5 指標同陣列', '第56堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-056', '', '', @now, @gmt, '', 0, '', 56, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1h7elYQ4NvRZ_JJ-XYcggP1_P-4NvYWjs/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '5.6 const 同指標', '第57堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-057', '', '', @now, @gmt, '', 0, '', 57, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1kkmRBdCO85WUWKh-5JpbKJHw8GIeGq5B/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '5.7 new 同 delete', '第58堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-058', '', '', @now, @gmt, '', 0, '', 58, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/18-UUXg3e2B32MxKWPLN-JVdqos6NGVDC/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '5.8 RAII', '第59堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-059', '', '', @now, @gmt, '', 0, '', 59, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1zSVqYPwsLqfRL3-YEJ1tybASqnzWzK8I/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '5.9 unique_ptr', '第60堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-060', '', '', @now, @gmt, '', 0, '', 60, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1mwQni20QSktmVRXzgmdLTXoQH4-2eef4/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '5.10 shared_ptr 同 weak_ptr', '第61堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-061', '', '', @now, @gmt, '', 0, '', 61, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1ZmQJsStAckXnG08_BluMKthEwyHIwGpC/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '5.11 未定義行為', '第62堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-062', '', '', @now, @gmt, '', 0, '', 62, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1wLbtOOwK_Twtdc3FfFgwFRnGcQL53TpE/view' FROM DUAL WHERE @lesson_id <> 0;

-- Part 6 物件導向
INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '6.1 struct', '第63堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-063', '', '', @now, @gmt, '', 0, '', 63, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1WaXhI0h0XGN8MzN-HH2sYvSfZXV2xMgg/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '6.2 class 同成員函數', '第64堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-064', '', '', @now, @gmt, '', 0, '', 64, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/15mhkC_dK6fLQkwrwTbG6YE205vl3t5BT/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '6.3 封裝：public / private', '第65堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-065', '', '', @now, @gmt, '', 0, '', 65, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/13ZWDGlG85Y2NLmEpkew6RtpxE7JY5TBp/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '6.4 Constructor', '第66堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-066', '', '', @now, @gmt, '', 0, '', 66, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1Sf_ZGHEMGwkmYrqa7LoG-sMdfA0h53sB/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '6.5 Destructor', '第67堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-067', '', '', @now, @gmt, '', 0, '', 67, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1PmVsSDd4KYpCQinwrBdjDjD2R1kN_GLW/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '6.6 this 同 const 成員函數', '第68堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-068', '', '', @now, @gmt, '', 0, '', 68, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1xhwrfTBVVHygqVskItw8xCqPz0mIuO5x/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '6.7 static 成員', '第69堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-069', '', '', @now, @gmt, '', 0, '', 69, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1ecTbRwlChLd6kPqe3R_d5eMVQ7xv8DpG/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '6.8 運算子多載', '第70堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-070', '', '', @now, @gmt, '', 0, '', 70, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1CP2x7v7idEHImhVSX-GJQWPtKbBp76F6/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '6.9 複製', '第71堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-071', '', '', @now, @gmt, '', 0, '', 71, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1QkhYitc0CmQqYvDQyR_hdbaHuTfGvwHQ/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '6.10 Move semantics', '第72堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-072', '', '', @now, @gmt, '', 0, '', 72, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1mDVgaKG3SNoecUDyq9HM8l9KkhF3b1Sw/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '6.11 Rule of zero / five', '第73堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-073', '', '', @now, @gmt, '', 0, '', 73, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/18goaLLlXAj4mjHpc1NJkeWe2HipTNcOW/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '6.12 繼承', '第74堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-074', '', '', @now, @gmt, '', 0, '', 74, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1iKzi96mUZgYWhixshjGeoprC5LLGvBTC/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '6.13 virtual 同多型', '第75堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-075', '', '', @now, @gmt, '', 0, '', 75, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1a5dhvmSofwszXhPmrESF_ucN-p1ygbQf/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '6.14 抽象類別', '第76堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-076', '', '', @now, @gmt, '', 0, '', 76, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/12q8CPrUG_r_LBYE-sPLfN5ivZYosDWFg/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '6.15 virtual destructor 同 final', '第77堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-077', '', '', @now, @gmt, '', 0, '', 77, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/175UCG_whhwLUDnukJvFHciFYSDJd1okt/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '6.16 組合 vs 繼承', '第78堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-078', '', '', @now, @gmt, '', 0, '', 78, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1a9AgJIFfU6SisuT3-FcDCDMuGgKE8GfV/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '6.17 enum class', '第79堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-079', '', '', @now, @gmt, '', 0, '', 79, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1aenQoF6hqUEKJlMF4_B5yMoE3zuJJdAG/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '6.18 小項目：圖形面積計算器', '第80堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-080', '', '', @now, @gmt, '', 0, '', 80, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/12S2olKCale2VVksKGIvMu8i3gvntd1tl/view' FROM DUAL WHERE @lesson_id <> 0;

-- Part 7 模板
INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '7.1 函數模板', '第81堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-081', '', '', @now, @gmt, '', 0, '', 81, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1FebxKmHl06grdVS0-DkI_dLolH_8lzvX/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '7.2 類別模板', '第82堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-082', '', '', @now, @gmt, '', 0, '', 82, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1lXo91VjoqRlFKWfJKkpTs3uf2sQQRIS9/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '7.3 推導同 CTAD', '第83堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-083', '', '', @now, @gmt, '', 0, '', 83, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1HgpJ8QKQAJWjcFN6pC4fUAO5daSnBwxD/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '7.4 Concepts', '第84堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-084', '', '', @now, @gmt, '', 0, '', 84, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1jl555M8648X285xHSNWpMx-LxVASk9w9/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '7.5 constexpr 函數同 if constexpr', '第85堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-085', '', '', @now, @gmt, '', 0, '', 85, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1ioKieBfvcMV2iIDc2Kan4P2X97mZfpRS/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '7.6 Variadic templates', '第86堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-086', '', '', @now, @gmt, '', 0, '', 86, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/11f_oitD3qO6IY7gNWypJ4LOHo2yodMhQ/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '7.7 小項目：自己寫 MiniVector', '第87堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-087', '', '', @now, @gmt, '', 0, '', 87, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1d6Hm1YswM6RjvZGTmD3Jst3UTTdlLTVJ/view' FROM DUAL WHERE @lesson_id <> 0;

-- Part 8 STL 標準函式庫
INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '8.1 STL 全景', '第88堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-088', '', '', @now, @gmt, '', 0, '', 88, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1tfV2XlrefmkMAn_r2MaFUULeJeJoSGXR/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '8.2 Iterator', '第89堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-089', '', '', @now, @gmt, '', 0, '', 89, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1F0LDeyTi3umAoV9s87JdlzX7Nvb8O6tV/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '8.3 vector 深入', '第90堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-090', '', '', @now, @gmt, '', 0, '', 90, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1CFzjEni_Q05NXmVbM072vXjWe0uKb7nb/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '8.4 pair、tuple、structured bindings', '第91堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-091', '', '', @now, @gmt, '', 0, '', 91, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1LG7p3mQajzGcpN4VnN5CgPY4N1mn-XaL/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '8.5 map', '第92堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-092', '', '', @now, @gmt, '', 0, '', 92, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1b19L1nNMSD7H5m5oHHLEYAJjdUWgT5LU/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '8.6 unordered_map', '第93堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-093', '', '', @now, @gmt, '', 0, '', 93, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1KjZRdjTUa4eMtCzFeA0ILme7MfJgjZ0I/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '8.7 set 同 multiset', '第94堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-094', '', '', @now, @gmt, '', 0, '', 94, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1pc-axR6unrzi4DwUIfH4ofVY-7Qkskk9/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '8.8 stack 同 queue', '第95堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-095', '', '', @now, @gmt, '', 0, '', 95, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1gNjpm_XTKZQl67tNBFg_IURYvSYB3KCE/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '8.9 priority_queue', '第96堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-096', '', '', @now, @gmt, '', 0, '', 96, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1grwzrDlKhCjRduPt_SqfxOYHsd9xgbGT/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '8.10 deque 同 list', '第97堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-097', '', '', @now, @gmt, '', 0, '', 97, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/15O4yOTmoFPjDPCBuY_SP-qFGUrcCocGz/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '8.11 Lambda', '第98堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-098', '', '', @now, @gmt, '', 0, '', 98, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/10aWmTlsPPS-tPTF1YmU1JgcxhxrFZlLH/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '8.12 sort 同自訂比較', '第99堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-099', '', '', @now, @gmt, '', 0, '', 99, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1cauY7wzZMEkr0ojrZRicQ5eKJiy30ruj/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '8.13 常用演算法', '第100堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-100', '', '', @now, @gmt, '', 0, '', 100, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1gbGDDxhRcOjQTPy1WsWVGS9jMmbiw5g5/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '8.14 二分搜尋', '第101堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-101', '', '', @now, @gmt, '', 0, '', 101, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1zpQJI9WluswIkSu0c_5LD_xU3V9qKL_w/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '8.15 Ranges 同 views', '第102堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-102', '', '', @now, @gmt, '', 0, '', 102, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/18RjNsH22Vde5xsyOkTsyjMCidn-UZR-u/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '8.16 optional', '第103堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-103', '', '', @now, @gmt, '', 0, '', 103, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1wIKDGWrFT544fhl1ktAuHuQXlUC-KnHa/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '8.17 variant 同 visit', '第104堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-104', '', '', @now, @gmt, '', 0, '', 104, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1L8E7pEPaaBwz3w4QIPhGf7NG5kW6RQDK/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '8.18 string_view 同 span', '第105堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-105', '', '', @now, @gmt, '', 0, '', 105, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1c63mi1MmbIX6YUQlcQrMtw0QEDeAhST2/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '8.19 std::format 同 std::print', '第106堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-106', '', '', @now, @gmt, '', 0, '', 106, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1UKrS0cZ1yc4j17wKNsWKefAEcaph7DF3/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '8.20 chrono', '第107堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-107', '', '', @now, @gmt, '', 0, '', 107, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1rrkniGCXMhkGlp9csDDfpPs_jgZMrmAO/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '8.21 小項目：單字頻率統計', '第108堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-108', '', '', @now, @gmt, '', 0, '', 108, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1vf4a975DaMMZgbCKhFlNy4FdMI_lUWH5/view' FROM DUAL WHERE @lesson_id <> 0;

-- Part 9 錯誤處理同檔案
INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '9.1 Exception 入門', '第109堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-109', '', '', @now, @gmt, '', 0, '', 109, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1K_UZZg8GhK-apqdB2H3fvt1VbTTbZN8x/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '9.2 標準同自訂 exception', '第110堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-110', '', '', @now, @gmt, '', 0, '', 110, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1XxuRF5TGvD0dmu0IHXKXGBzTa-wNCjC3/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '9.3 noexcept 同 exception safety', '第111堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-111', '', '', @now, @gmt, '', 0, '', 111, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1SPLAutRLQT49estZq17LjjRwJ4VW9vn_/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '9.4 assert 同 static_assert', '第112堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-112', '', '', @now, @gmt, '', 0, '', 112, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/18CV0Uq-BHVJsqjPeHkNiGMDaKPuxl5jm/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '9.5 std::expected', '第113堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-113', '', '', @now, @gmt, '', 0, '', 113, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1uAyNCzHwxOO6q6GQisPKZfp6gKl8mEgZ/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '9.6 讀寫檔案', '第114堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-114', '', '', @now, @gmt, '', 0, '', 114, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/15kh2LC1kk85qDoxh6scr8NQ6R_lDNanF/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '9.7 stringstream 同解析文字', '第115堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-115', '', '', @now, @gmt, '', 0, '', 115, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1ufApnmx9xwfDqPShJ17srv63w7-9ZrTr/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '9.8 std::filesystem', '第116堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-116', '', '', @now, @gmt, '', 0, '', 116, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/14quspqZMbdV1HIq__q3oUoVS6fVfvAwW/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '9.9 小項目：記帳簿', '第117堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-117', '', '', @now, @gmt, '', 0, '', 117, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1tKecpamo31UfAg1QQK_PVZKgKtsRDd11/view' FROM DUAL WHERE @lesson_id <> 0;

-- Part 10 工具同工程
INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '10.1 編譯三部曲', '第118堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-118', '', '', @now, @gmt, '', 0, '', 118, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1mjzhX4ft187lswkXao8as68LpSlkXaWF/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '10.2 Preprocessor 同 macro', '第119堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-119', '', '', @now, @gmt, '', 0, '', 119, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/18F5iNQZmlPswn-WWzzaSXnR4CSqFQ4M6/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '10.3 CMake 入門', '第120堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-120', '', '', @now, @gmt, '', 0, '', 120, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1wnNVHGLgh6Xl-Anaab3HZZKn05D9_1x6/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '10.4 Debugger', '第121堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-121', '', '', @now, @gmt, '', 0, '', 121, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1FjQ97UJIHO3D9Nxu-QyzenhNc1CaFILk/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '10.5 單元測試', '第122堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-122', '', '', @now, @gmt, '', 0, '', 122, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1PUmSTQNjgDh15W0CAXR26smRQgZhiIEG/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '10.6 用第三方庫', '第123堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-123', '', '', @now, @gmt, '', 0, '', 123, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1N9ALYC0haArm4xBks6IrkkTX5aZ334HP/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '10.7 效能入門', '第124堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-124', '', '', @now, @gmt, '', 0, '', 124, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/108eCeeWzmY3rcbK-PUiVaNR0F8IbxAkH/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '10.8 C++20 modules 簡介', '第125堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-125', '', '', @now, @gmt, '', 0, '', 125, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1mP3yMne-3bGr-ew_v7pg56zUcRM7qmwX/view' FROM DUAL WHERE @lesson_id <> 0;

-- Part 11 並行
INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '11.1 thread 同 jthread', '第126堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-126', '', '', @now, @gmt, '', 0, '', 126, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1238xyw8RHlr2N-InBBwk3HXWi9-0FgRE/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '11.2 Data race 同 mutex', '第127堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-127', '', '', @now, @gmt, '', 0, '', 127, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1bP6OOPBlTedCZZsexqhfIBNegJgqQB3O/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '11.3 atomic', '第128堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-128', '', '', @now, @gmt, '', 0, '', 128, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1i3CAx-wmjTJcFs8H5Uy4mykpQtnDxsuC/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '11.4 Deadlock', '第129堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-129', '', '', @now, @gmt, '', 0, '', 129, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/16mPSgSibpMr51UTO2hVtrC9AafHjPUtP/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '11.5 condition_variable', '第130堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-130', '', '', @now, @gmt, '', 0, '', 130, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1XJFI7rlgUKQLK1Bn0UVirGfnoVNeQNKk/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '11.6 async 同 future', '第131堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-131', '', '', @now, @gmt, '', 0, '', 131, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1ngKPjTo5Zo-7M5yoUcDfQjXZnfzAVnKZ/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '11.7 小項目：平行搵質數', '第132堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-132', '', '', @now, @gmt, '', 0, '', 132, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/13-0LSbbv1uHHZQvf7VXWRu1WMHGdLRT1/view' FROM DUAL WHERE @lesson_id <> 0;

-- Part 12 演算法同競賽
INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '12.1 競賽寫法', '第133堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-133', '', '', @now, @gmt, '', 0, '', 133, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1GHcWrgblHGET6WsMkwLb8mp1Q4mHfldu/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '12.2 時間複雜度', '第134堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-134', '', '', @now, @gmt, '', 0, '', 134, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1_2EGtf9unTRSxreOj6HFwZ3hd5SjdP_A/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '12.3 前綴和', '第135堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-135', '', '', @now, @gmt, '', 0, '', 135, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1OgxPGCgQmbexpwGCY772NzcIAEoa3Mk9/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '12.4 雙指針同滑動視窗', '第136堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-136', '', '', @now, @gmt, '', 0, '', 136, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1KcNrBxuDQe6RD8-uyn9Bw89mYB-Oahr-/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '12.5 二分答案', '第137堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-137', '', '', @now, @gmt, '', 0, '', 137, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1Dwd-G9mgPYdKfxplKBSVSvmIY-U0dQhS/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '12.6 貪心', '第138堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-138', '', '', @now, @gmt, '', 0, '', 138, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1MYjp781FeV3eROVkCSQJVn6_80Mn3dqT/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '12.7 回溯', '第139堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-139', '', '', @now, @gmt, '', 0, '', 139, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1-cGoZi6US4KLvlcMbWAURRF9P2We3rjN/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '12.8 位元運算', '第140堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-140', '', '', @now, @gmt, '', 0, '', 140, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1qqYMiUnmT-mIf9IxSNH5TtVCSfIIjKsJ/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '12.9 圖嘅表示', '第141堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-141', '', '', @now, @gmt, '', 0, '', 141, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1POAn7q3nQpgCcFsJghkMP3WjvaTg17Kf/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '12.10 DFS', '第142堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-142', '', '', @now, @gmt, '', 0, '', 142, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1VFj6R6gZCJhiaL4usXh68gu0wDv8GodK/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '12.11 BFS', '第143堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-143', '', '', @now, @gmt, '', 0, '', 143, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1eY7ItWknt6ZMnDXuRfEpiLbNEn093iu5/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '12.12 Dijkstra', '第144堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-144', '', '', @now, @gmt, '', 0, '', 144, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1MgpTU7-S5vmtMCIK74bt02RdSS6BU7ZE/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '12.13 並查集', '第145堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-145', '', '', @now, @gmt, '', 0, '', 145, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1Ck4ZwhMGbmcEi31X53wAjFK1K6IFHZJx/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '12.14 動態規劃入門', '第146堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-146', '', '', @now, @gmt, '', 0, '', 146, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1rl_gFNzMONI_G2isJXbzg-IGriDw9e3v/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '12.15 經典 DP', '第147堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-147', '', '', @now, @gmt, '', 0, '', 147, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1udsyuPXH8dCZdzGjRuoMRnW_0sWIye76/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '12.16 數論基礎', '第148堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-148', '', '', @now, @gmt, '', 0, '', 148, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1mHprHKejba7iIxV99b7Efnpo_iqqmDWn/view' FROM DUAL WHERE @lesson_id <> 0;

-- Part 13 綜合項目
INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '13.1 貪食蛇（一）：遊戲迴圈', '第149堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-149', '', '', @now, @gmt, '', 0, '', 149, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1yGlSMQcJ8IcXKCfbkVugxeczkpEAGOoT/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '13.2 貪食蛇（二）：鍵盤同碰撞', '第150堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-150', '', '', @now, @gmt, '', 0, '', 150, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1quT3MZ3H8Pc-5q5d1Rvrxnu8oMhWbVIP/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '13.3 貪食蛇（三）：分數同收尾', '第151堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-151', '', '', @now, @gmt, '', 0, '', 151, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1s7maafGX9wQq4m2RXsSwevqyMElz5067/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '13.4 圖書館管理系統（一）：設計', '第152堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-152', '', '', @now, @gmt, '', 0, '', 152, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1YYZy7tCqYwsgune2imWfFiyqKBDLORbH/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '13.5 圖書館管理系統（二）：完成', '第153堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-153', '', '', @now, @gmt, '', 0, '', 153, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1P7BYDJodc-ktHDBEQykavlzmInAYBkTZ/view' FROM DUAL WHERE @lesson_id <> 0;

INSERT INTO wp_posts (
  post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt,
  post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged,
  post_modified, post_modified_gmt, post_content_filtered, post_parent, guid,
  menu_order, post_type, post_mime_type, comment_count
)
SELECT 1, @now, @gmt, '13.6 下一步去邊？', '第154堂', '', 'publish', 'closed', 'closed', '', 'cpp-154-154', '', '', @now, @gmt, '', 0, '', 154, 'hkps_lh_lesson', '', 0
FROM wp_posts
WHERE ID = 5066 AND post_type = 'hkps_lh_course' AND @course_ok = 1
LIMIT 1;
SET @lesson_id := IF(ROW_COUNT() = 1, LAST_INSERT_ID(), 0);
UPDATE wp_posts
SET guid = CONCAT('https://www.hkprog.org/?post_type=hkps_lh_lesson&p=', @lesson_id)
WHERE ID = @lesson_id AND @lesson_id <> 0;
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT @lesson_id, '_hkps_lh_course', '5066' FROM DUAL WHERE @lesson_id <> 0
UNION ALL
SELECT @lesson_id, '_hkps_lh_video', 'https://drive.google.com/file/d/1Xer2WYVJGH2uyoG1egzZkVqLLezY_aKx/view' FROM DUAL WHERE @lesson_id <> 0;

COMMIT;

SELECT p.menu_order, p.post_title, p.post_content, v.meta_value AS video
FROM wp_posts AS p
INNER JOIN wp_postmeta AS course
  ON course.post_id = p.ID AND course.meta_key = '_hkps_lh_course' AND course.meta_value = '5066'
INNER JOIN wp_postmeta AS v
  ON v.post_id = p.ID AND v.meta_key = '_hkps_lh_video'
WHERE p.post_type = 'hkps_lh_lesson' AND p.post_status = 'publish'
ORDER BY p.menu_order
LIMIT 5;

SELECT COUNT(*) AS cpp_lessons
FROM wp_posts AS p
INNER JOIN wp_postmeta AS course
  ON course.post_id = p.ID AND course.meta_key = '_hkps_lh_course' AND course.meta_value = '5066'
WHERE p.post_type = 'hkps_lh_lesson' AND p.post_status = 'publish';
-- cpp_lessons must be 154.
