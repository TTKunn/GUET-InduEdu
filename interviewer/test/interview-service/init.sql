-- 面试记录服务数据库初始化脚本

-- 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS interview_analysis CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE interview_analysis;

-- 面试会话表
CREATE TABLE IF NOT EXISTS interview_sessions (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '自增主键',
    user_id VARCHAR(100) NOT NULL COMMENT '用户ID，关联candidate_profiles.user_id',
    session_id VARCHAR(100) UNIQUE NOT NULL COMMENT '面试会话唯一标识',
    session_name VARCHAR(200) COMMENT '面试名称',
    session_type VARCHAR(50) DEFAULT 'technical' COMMENT '面试类型：technical/behavioral/hr/comprehensive',
    status VARCHAR(20) DEFAULT 'pending' COMMENT '面试状态：pending/in_progress/completed/cancelled',
    difficulty_level VARCHAR(20) DEFAULT 'medium' COMMENT '面试难度：easy/medium/hard',
    estimated_duration INTEGER DEFAULT 60 COMMENT '预计时长（分钟）',
    actual_duration INTEGER COMMENT '实际时长（分钟）',
    start_time TIMESTAMP NULL COMMENT '开始时间',
    end_time TIMESTAMP NULL COMMENT '结束时间',
    total_questions INTEGER DEFAULT 0 COMMENT '总题目数',
    completed_questions INTEGER DEFAULT 0 COMMENT '已完成题目数',
    average_score DECIMAL(3,2) COMMENT '平均得分',
    interviewer_notes TEXT COMMENT '面试官总体评价',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    INDEX idx_user_id (user_id),
    INDEX idx_session_id (session_id),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
) COMMENT='面试会话表';

-- 面试题目表
CREATE TABLE IF NOT EXISTS interview_questions (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '自增主键',
    session_id VARCHAR(100) NOT NULL COMMENT '面试会话ID',
    question_id VARCHAR(100) NOT NULL COMMENT '题目唯一标识',
    question_text TEXT NOT NULL COMMENT '题目原文',
    question_type VARCHAR(50) DEFAULT 'technical' COMMENT '题目类型：technical/behavioral/logical/project_based',
    question_category VARCHAR(100) COMMENT '题目分类：如算法、数据库、框架等',
    difficulty_level VARCHAR(20) DEFAULT 'medium' COMMENT '题目难度：easy/medium/hard',
    expected_duration INTEGER DEFAULT 10 COMMENT '预期时长（分钟）',
    reference_answer TEXT COMMENT '参考答案',
    scoring_criteria TEXT COMMENT '评分标准',
    sort_order INTEGER DEFAULT 0 COMMENT '题目顺序',
    is_required BOOLEAN DEFAULT TRUE COMMENT '是否必答',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    
    FOREIGN KEY (session_id) REFERENCES interview_sessions(session_id) ON DELETE CASCADE,
    UNIQUE KEY uk_session_question (session_id, question_id),
    INDEX idx_session_id (session_id),
    INDEX idx_question_type (question_type),
    INDEX idx_sort_order (sort_order)
) COMMENT='面试题目表';

-- 面试回答表
CREATE TABLE IF NOT EXISTS interview_answers (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '自增主键',
    question_id VARCHAR(100) NOT NULL COMMENT '题目ID',
    session_id VARCHAR(100) NOT NULL COMMENT '会话ID',
    candidate_answer TEXT COMMENT '面试者回答',
    interviewer_feedback TEXT COMMENT '面试官反馈',
    answer_quality VARCHAR(20) COMMENT '回答质量：excellent/good/average/poor',
    technical_accuracy DECIMAL(3,2) COMMENT '技术准确性评分（0-10）',
    communication_clarity DECIMAL(3,2) COMMENT '表达清晰度评分（0-10）',
    problem_solving DECIMAL(3,2) COMMENT '问题解决能力评分（0-10）',
    overall_score DECIMAL(3,2) COMMENT '综合评分（0-10）',
    answer_duration INTEGER COMMENT '回答时长（分钟）',
    status VARCHAR(20) DEFAULT 'pending' COMMENT '回答状态：pending/answered/reviewed/skipped',
    answered_at TIMESTAMP NULL COMMENT '回答时间',
    reviewed_at TIMESTAMP NULL COMMENT '评价时间',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    FOREIGN KEY (question_id) REFERENCES interview_questions(question_id) ON DELETE CASCADE,
    FOREIGN KEY (session_id) REFERENCES interview_sessions(session_id) ON DELETE CASCADE,
    UNIQUE KEY uk_question_answer (question_id),
    INDEX idx_session_id (session_id),
    INDEX idx_status (status),
    INDEX idx_overall_score (overall_score)
) COMMENT='面试回答表';

-- 插入示例数据（可选）
-- INSERT INTO interview_sessions (user_id, session_id, session_name, session_type, status) 
-- VALUES ('test_user_001', 'session_20250904_001', '测试面试会话', 'technical', 'pending');

-- 显示表结构
SHOW TABLES;
DESCRIBE interview_sessions;
DESCRIBE interview_questions;
DESCRIBE interview_answers;
