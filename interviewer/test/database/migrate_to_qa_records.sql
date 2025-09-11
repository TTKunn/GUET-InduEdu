-- 数据库架构迁移脚本：从分离表结构迁移到合并表结构
-- 创建时间：2025-09-06
-- 目的：将interview_questions和interview_answers合并为interview_qa_records

-- ==================== 备份现有数据 ====================

-- 备份interview_questions表
CREATE TABLE IF NOT EXISTS interview_questions_backup AS 
SELECT * FROM interview_questions;

-- 备份interview_answers表  
CREATE TABLE IF NOT EXISTS interview_answers_backup AS 
SELECT * FROM interview_answers;

-- ==================== 创建新的合并表 ====================

CREATE TABLE IF NOT EXISTS interview_qa_records (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '自增主键',
    session_id VARCHAR(100) NOT NULL COMMENT '面试会话ID',
    question_id VARCHAR(100) NOT NULL COMMENT '题目唯一标识',
    
    -- 题目相关字段
    question_text TEXT NOT NULL COMMENT '题目原文',
    question_type VARCHAR(50) DEFAULT 'technical' COMMENT '题目类型',
    question_category VARCHAR(100) COMMENT '题目分类',
    difficulty_level VARCHAR(20) DEFAULT 'medium' COMMENT '题目难度',
    expected_duration INT DEFAULT 10 COMMENT '预期时长（分钟）',
    reference_answer TEXT COMMENT '参考答案',
    scoring_criteria TEXT COMMENT '评分标准',
    sort_order INT DEFAULT 0 COMMENT '题目顺序',
    is_required BOOLEAN DEFAULT TRUE COMMENT '是否必答',
    
    -- 回答相关字段
    candidate_answer TEXT COMMENT '面试者回答',
    interviewer_feedback TEXT COMMENT '面试官反馈',
    answer_quality VARCHAR(20) COMMENT '回答质量',
    technical_accuracy DECIMAL(3,2) COMMENT '技术准确性评分',
    communication_clarity DECIMAL(3,2) COMMENT '表达清晰度评分',
    problem_solving DECIMAL(3,2) COMMENT '问题解决能力评分',
    overall_score DECIMAL(3,2) COMMENT '综合评分',
    answer_duration INT COMMENT '回答时长（分钟）',
    status VARCHAR(20) DEFAULT 'pending' COMMENT '回答状态',
    
    -- 错题标记字段
    is_wrong_question BOOLEAN DEFAULT FALSE COMMENT '是否为错题',
    
    -- 时间字段
    answered_at TIMESTAMP NULL COMMENT '回答时间',
    reviewed_at TIMESTAMP NULL COMMENT '评价时间',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    -- 外键约束
    FOREIGN KEY (session_id) REFERENCES interview_sessions(session_id) ON DELETE CASCADE,
    
    -- 索引
    INDEX idx_qa_session_wrong (session_id, is_wrong_question) COMMENT '错题查询优化',
    INDEX idx_qa_question_type (question_type, difficulty_level) COMMENT '题目类型查询优化',
    INDEX idx_qa_status (status) COMMENT '状态查询优化'
) COMMENT='面试问答记录表（合并题目和回答）';

-- ==================== 数据迁移 ====================

-- 迁移数据：将interview_questions和interview_answers合并
INSERT INTO interview_qa_records (
    session_id, question_id, question_text, question_type, question_category,
    difficulty_level, expected_duration, reference_answer, scoring_criteria,
    sort_order, is_required, candidate_answer, interviewer_feedback,
    answer_quality, technical_accuracy, communication_clarity, problem_solving,
    overall_score, answer_duration, status, is_wrong_question,
    answered_at, reviewed_at, created_at, updated_at
)
SELECT 
    q.session_id, q.question_id, q.question_text, q.question_type, q.question_category,
    q.difficulty_level, q.expected_duration, q.reference_answer, q.scoring_criteria,
    q.sort_order, q.is_required, a.candidate_answer, a.interviewer_feedback,
    a.answer_quality, a.technical_accuracy, a.communication_clarity, a.problem_solving,
    a.overall_score, a.answer_duration, 
    COALESCE(a.status, 'pending') as status,
    CASE WHEN a.overall_score < 6.0 THEN TRUE ELSE FALSE END as is_wrong_question,
    a.answered_at, a.reviewed_at, q.created_at, 
    COALESCE(a.updated_at, q.created_at) as updated_at
FROM interview_questions q
LEFT JOIN interview_answers a ON q.question_id = a.question_id;

-- ==================== 验证迁移结果 ====================

-- 检查迁移的记录数
SELECT 
    'Original Questions' as table_name, COUNT(*) as count FROM interview_questions
UNION ALL
SELECT 
    'Original Answers' as table_name, COUNT(*) as count FROM interview_answers  
UNION ALL
SELECT 
    'Migrated QA Records' as table_name, COUNT(*) as count FROM interview_qa_records;

-- 检查错题标记情况
SELECT 
    'Total Records' as type, COUNT(*) as count FROM interview_qa_records
UNION ALL
SELECT 
    'Wrong Questions' as type, COUNT(*) as count FROM interview_qa_records WHERE is_wrong_question = TRUE
UNION ALL
SELECT 
    'Correct Questions' as type, COUNT(*) as count FROM interview_qa_records WHERE is_wrong_question = FALSE;

-- ==================== 清理旧表（可选，谨慎执行）====================

-- 注意：只有在确认迁移成功后才执行以下语句
-- DROP TABLE IF EXISTS interview_questions;
-- DROP TABLE IF EXISTS interview_answers;

-- ==================== 回滚脚本（紧急情况使用）====================

-- 如果需要回滚，可以使用以下脚本：
-- 
-- -- 恢复interview_questions表
-- CREATE TABLE interview_questions AS 
-- SELECT * FROM interview_questions_backup;
-- 
-- -- 恢复interview_answers表
-- CREATE TABLE interview_answers AS 
-- SELECT * FROM interview_answers_backup;
-- 
-- -- 删除新表
-- DROP TABLE interview_qa_records;
-- 
-- -- 删除备份表
-- DROP TABLE interview_questions_backup;
-- DROP TABLE interview_answers_backup;

-- ==================== 迁移完成 ====================
-- 迁移脚本执行完成
-- 请验证数据完整性后再删除备份表
