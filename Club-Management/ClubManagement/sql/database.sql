CREATE TABLE `tb_club` (
                           `club_id`             bigint       NOT NULL AUTO_INCREMENT COMMENT '社团主键ID',
                           `name`                varchar(100) NOT NULL COMMENT '社团名称',
                           `description`         text         COMMENT '社团简介',
                           `category_id`         bigint       NOT NULL COMMENT '分类ID',
                           `leader_id`           bigint       NOT NULL COMMENT '社长ID',
                           `primary_advisor_id`  bigint       COMMENT '主要指导老师ID',
                           `dept_id`             bigint       NOT NULL COMMENT '院系ID',
                           `logo_url`            varchar(255) DEFAULT NULL COMMENT 'Logo URL',
                           `status`              tinyint      DEFAULT 0 COMMENT '状态（0正常 1停用）',
                           `activity_count`      int          DEFAULT 0 COMMENT '社团活动数量',
                           `member_count`        int          DEFAULT 0 COMMENT '当前成员数量',
                           `active_member_count` int          DEFAULT 0 COMMENT '活跃成员数量',
                           `total_members_ever`  int          DEFAULT 0 COMMENT '历史总成员数',
                           `created_at`          datetime     DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                           `updated_at`          datetime     DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
                           `deleted_at`          datetime     DEFAULT NULL COMMENT '软删除时间',
                           PRIMARY KEY (`club_id`),
                           KEY `idx_category` (`category_id`),
                           KEY `idx_leader` (`leader_id`),
                           KEY `idx_advisor` (`primary_advisor_id`),
                           KEY `idx_dept` (`dept_id`),
                           KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='社团主表';

CREATE TABLE `tb_club_advisor` (
                                   `club_id`     bigint   NOT NULL COMMENT '社团ID',
                                   `advisor_id`  bigint   NOT NULL COMMENT '老师ID',
                                   `deleted_at`  datetime DEFAULT NULL COMMENT '软删除时间',
                                   PRIMARY KEY (`club_id`, `advisor_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='社团指导老师关联';

CREATE TABLE `tb_category` (
                               `category_id`   bigint       NOT NULL AUTO_INCREMENT COMMENT '分类主键ID',
                               `name` varchar(100) NOT NULL COMMENT '分类名称',
                               `description`   text COMMENT '分类描述',
                               `status`        tinyint      DEFAULT 0 COMMENT '状态（0正常 1停用）',
                               `created_at`    datetime     DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                               `updated_at`    datetime     DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
                               `deleted_at`    datetime     DEFAULT NULL COMMENT '软删除时间',
                               PRIMARY KEY (`category_id`),
                               KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='社团分类表';

CREATE TABLE `tb_attendance` (
                                 `attendance_id`  bigint       NOT NULL AUTO_INCREMENT COMMENT '主键ID',
                                 `club_id`        bigint       NOT NULL COMMENT '社团ID',
                                 `user_id`        bigint       NOT NULL COMMENT '用户ID',
                                 `clock_in_time`  datetime     DEFAULT NULL COMMENT '签到时间',
                                 `clock_out_time` datetime     DEFAULT NULL COMMENT '签退时间',
                                 `study_duration` int          DEFAULT NULL COMMENT '学习时长(分钟)',
                                 `status`         varchar(20)   COMMENT '状态',
                                 `notes`          varchar(255) DEFAULT NULL COMMENT '备注',
                                 `created_at`     datetime     DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                                 `updated_at`     datetime     DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
                                 `deleted_at`     datetime     DEFAULT NULL COMMENT '软删除时间',
                                 PRIMARY KEY (`attendance_id`),
                                 KEY `idx_attendance_club` (`club_id`),
                                 KEY `idx_attendance_user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='社团考勤表';

CREATE TABLE `tb_announcement` (
                                   `announcement_id` bigint       NOT NULL AUTO_INCREMENT COMMENT '公告主键ID',
                                   `title`           varchar(200) NOT NULL COMMENT '公告标题',
                                   `content`         text         NOT NULL COMMENT '公告内容',
                                   `publisher_id`    bigint       NOT NULL COMMENT '发布人（用户ID）',
                                   `club_id`         bigint       NOT NULL COMMENT '所属社团ID',
                                   `type`            varchar(20)  DEFAULT 'GENERAL' COMMENT '公告类型（GENERAL/PUBLIC/INTERNAL等）',
                                   `status`          varchar(30)     COMMENT '状态',
                                   `created_at`      datetime     DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                                   `deleted_at`      datetime     DEFAULT NULL COMMENT '软删除时间',
                                   PRIMARY KEY (`announcement_id`),
                                   KEY `idx_ann_club` (`club_id`),
                                   KEY `idx_ann_publisher` (`publisher_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='社团公告表';

CREATE TABLE `tb_activity_visibility` (
                                          `activity_id` bigint NOT NULL COMMENT '活动ID',
                                          `club_id`     bigint NOT NULL COMMENT '可见社团ID',
                                          PRIMARY KEY (`activity_id`, `club_id`),          -- 联合主键防重复
                                          KEY `idx_av_club` (`club_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='活动可见性关联表';

CREATE TABLE `tb_activity` (
                               `activity_id`  bigint       NOT NULL AUTO_INCREMENT COMMENT '活动主键ID',
                               `club_id`      bigint       NOT NULL COMMENT '所属社团ID',
                               `name`         varchar(100) NOT NULL COMMENT '活动名称',
                               `description`  text COMMENT '活动描述',
                               `start_time`   datetime     NOT NULL COMMENT '开始时间',
                               `end_time`     datetime     NOT NULL COMMENT '结束时间',
                               `location`     varchar(255) DEFAULT NULL COMMENT '活动地点',
                               `organizer_id` bigint       NOT NULL COMMENT '组织者（用户ID）',
                               `visibility`   varchar(20)  DEFAULT 'INTERNAL' COMMENT '可见范围（PUBLIC/INTERNAL）',
                               `status`       varchar(20)      DEFAULT 0 COMMENT '状态',
                               `is_ended`     tinyint      DEFAULT 0 COMMENT '是否已结束（0未结束 1已结束）',
                               `publish_time` datetime     DEFAULT CURRENT_TIMESTAMP COMMENT '发布时间',
                               `is_urgent`    tinyint      DEFAULT 0 COMMENT '是否紧急（0否 1是）',
                               `created_at`   datetime     DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                               `updated_at`   datetime     DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
                               `deleted_at`   datetime     DEFAULT NULL COMMENT '软删除时间',
                               PRIMARY KEY (`activity_id`),
                               KEY `idx_act_club` (`club_id`),
                               KEY `idx_act_organizer` (`organizer_id`),
                               KEY `idx_act_status` (`status`),
                               KEY `idx_act_ended` (`is_ended`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='社团活动表';

ALTER TABLE tb_activity_visibility
    ADD CONSTRAINT fk_av_activity FOREIGN KEY (activity_id) REFERENCES tb_activity (activity_id),
    ADD CONSTRAINT fk_av_club     FOREIGN KEY (club_id)     REFERENCES tb_club   (club_id);

CREATE TABLE `tb_achievement` (
                                  `achievement_id`   bigint       NOT NULL AUTO_INCREMENT COMMENT '荣誉主键ID',
                                  `club_id`          bigint       NOT NULL COMMENT '所属社团ID',
                                  `publisher_id`     bigint       NOT NULL COMMENT '发布人（用户ID）',
                                  `title`            varchar(150) NOT NULL COMMENT '荣誉标题',
                                  `type`             varchar(30)  DEFAULT 'TEAM' COMMENT '荣誉类型（TEAM/PERSONAL等）',
                                  `description`      text COMMENT '详细描述',
                                  `achieve_date`     date         NOT NULL COMMENT '获得日期',
                                  `certificate_url`  varchar(255) DEFAULT NULL COMMENT '证书/证明图片URL',
                                  `status`           tinyint      DEFAULT 0 COMMENT '审核状态 0待审 1通过 2驳回',
                                  `created_at`       datetime     DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                                  `deleted_at`       datetime     DEFAULT NULL COMMENT '软删除时间',
                                  PRIMARY KEY (`achievement_id`),
                                  KEY `idx_ach_club`     (`club_id`),
                                  KEY `idx_ach_publisher`(`publisher_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='社团荣誉表';

CREATE TABLE `tb_membership` (
                                 `membership_id`        bigint       NOT NULL AUTO_INCREMENT COMMENT '主键ID',
                                 `user_id`              bigint       NOT NULL COMMENT '用户ID',
                                 `club_id`              bigint       NOT NULL COMMENT '社团ID',
                                 `join_time`            datetime     DEFAULT CURRENT_TIMESTAMP COMMENT '入社时间',
                                 `status`               varchar(20)  COMMENT '状态',
                                 `exit_time`            datetime     DEFAULT NULL COMMENT '退社时间',
                                 `total_study_duration` int          DEFAULT 0 COMMENT '累计学习时长（分钟）',
                                 `activity_participation` int        DEFAULT 0 COMMENT '活动参与次数',
                                 `achievement_count`    int          DEFAULT 0 COMMENT '荣誉次数',
                                 `deleted_at`           datetime     DEFAULT NULL COMMENT '软删除时间',
                                 PRIMARY KEY (`membership_id`),
                                 UNIQUE KEY `uk_user_club` (`user_id`, `club_id`),  -- 一人同一社团仅一条记录
                                 KEY `idx_ms_club` (`club_id`),
                                 KEY `idx_ms_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='社员加入记录表';

CREATE TABLE `tb_activity_participation` (
                                             `activity_id`      bigint NOT NULL COMMENT '活动ID',
                                             `user_id`          bigint NOT NULL COMMENT '参与用户ID',
                                             `participation_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '参与时间',
                                             PRIMARY KEY (`activity_id`, `user_id`),          -- 联合主键防重复
                                             KEY `idx_ap_user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='活动参与记录表';

CREATE TABLE `tb_achievement_member` (
                                         `achievement_id` bigint NOT NULL COMMENT '荣誉ID',
                                         `user_id`        bigint NOT NULL COMMENT '成员用户ID',
                                         `role`           varchar(30)  DEFAULT 'MEMBER' COMMENT '担任角色',
                                         `contribution`   text COMMENT '贡献描述',
                                         PRIMARY KEY (`achievement_id`, `user_id`),
                                         KEY `idx_am_user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='荣誉参与成员关联表';


INSERT INTO `tb_category` (`name`, `description`, `status`) VALUES
                                                                ('学术科技', '学术研究、科技创新类社团', 0),
                                                                ('文化艺术', '文学、艺术、表演类社团', 0),
                                                                ('体育健身', '体育运动、健身类社团', 0),
                                                                ('公益实践', '志愿服务、社会实践类社团', 0),
                                                                ('创新创业', '创业实践、创新竞赛类社团', 0);

INSERT INTO `tb_club` (`name`, `description`, `category_id`, `leader_id`, `dept_id`, `logo_url`, `status`, `activity_count`, `member_count`, `active_member_count`) VALUES
                                                                                                                                                                        ('计算机协会', '专注于计算机技术和编程的学术社团', 1, 101, 1, '/images/computer_club.jpg', 0, 5, 50, 35),
                                                                                                                                                                        ('电子创新社', '电子设计与创新实践社团', 1, 101, 2, '/images/electronics_club.jpg', 0, 3, 30, 25),
                                                                                                                                                                        ('音乐社', '音乐表演与创作社团', 2, 101, 3, '/images/music_club.jpg', 0, 8, 45, 40),
                                                                                                                                                                        ('篮球社', '篮球运动与比赛社团', 3, 101, 4, '/images/basketball_club.jpg', 0, 12, 60, 55),
                                                                                                                                                                        ('志愿者协会', '志愿服务与社会实践社团', 4, 101, 5, '/images/volunteer_club.jpg', 0, 10, 80, 70),
                                                                                                                                                                        ('创业俱乐部', '创业项目孵化与实践社团', 5, 101, 6, '/images/startup_club.jpg', 0, 6, 35, 30);

INSERT INTO `tb_club_advisor` (`club_id`, `advisor_id`) VALUES
                                                            (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1);

INSERT INTO `tb_activity` (`club_id`, `name`, `description`, `start_time`, `end_time`, `location`, `organizer_id`, `visibility`, `status`, `is_ended`, `publish_time`, `is_urgent`) VALUES
                                                                                                                                                                                        (1, '编程竞赛培训', '为编程竞赛准备的算法培训', '2025-10-15 14:00:00', '2025-11-15 17:00:00', '计算机学院实验室', 101, 'public', 'published', 0, NOW(), 0),
                                                                                                                                                                                        (1, '人工智能讲座', 'AI技术发展趋势分享', '2025-10-20 15:00:00', '2025-11-20 17:00:00', '学术报告厅', 101, 'public','published', 0, NOW(), 0),
                                                                                                                                                                                        (2, '电子设计大赛', '年度电子设计创新大赛', '2025-11-05 09:00:00', '2025-11-05 18:00:00', '工程训练中心', 101, 'public','published', 0, NOW(), 0),
                                                                                                                                                                                        (3, '校园音乐节', '各社团音乐表演展示', '2025-10-25 18:00:00', '2025-11-25 22:00:00', '学校操场', 101, 'public', 'published', 0, NOW(), 0),
                                                                                                                                                                                        (3, '声乐训练课', '基础声乐技巧培训', '2025-10-18 19:00:00', '2025-11-18 21:00:00', '音乐教室', 101, 'public', 'published', 0, NOW(), 0),
                                                                                                                                                                                        (4, '篮球新生杯', '新生篮球比赛', '2025-10-18 16:00:00', '2025-11-18 18:00:00', '体育馆篮球场', 101, 'public', 'published', 0, NOW(), 0),
                                                                                                                                                                                        (4, '篮球技巧训练', '基础篮球技巧教学', '2025-10-22 17:00:00', '2025-11-22 19:00:00', '室外篮球场', 101, 'public', 'published', 0, NOW(), 0),
                                                                                                                                                                                        (5, '校园清洁日', '校园环境清理志愿服务', '2025-10-28 09:00:00', '2025-11-28 12:00:00', '校园各处', 101, 'public', 'published', 0, NOW(), 0),
                                                                                                                                                                                        (6, '创业项目路演', '创业项目展示与评审', '2025-11-10 14:00:00', '2025-11-10 17:00:00', '创业中心', 101, 'public', 'published', 0, NOW(), 0);

INSERT INTO `tb_activity_visibility` (`activity_id`, `club_id`) VALUES
                                                                    (1, 1), (1, 2),  -- 编程竞赛培训对计算机协会和电子创新社可见
                                                                    (2, 1),          -- AI讲座仅对计算机协会可见
                                                                    (3, 2),          -- 电子设计大赛仅对电子创新社可见
                                                                    (4, 3), (4, 1),  -- 音乐节对音乐社和计算机协会可见
                                                                    (7, 4), (7, 3);  -- 校园清洁日对志愿者协会和音乐社可见

INSERT INTO `tb_membership` (`user_id`, `club_id`, `status`, `total_study_duration`, `activity_participation`, `achievement_count`) VALUES
    (102, 1, 'active', 1200, 15, 3);

INSERT INTO `tb_activity_participation` (`activity_id`, `user_id`) VALUES
                                                                       (1, 1001), (1, 1007), (1, 1008), (1, 1009),
                                                                       (2, 1001), (2, 1007), (2, 1008),
                                                                       (3, 1002), (3, 1010),
                                                                       (4, 1003), (4, 1011), (4, 1001),
                                                                       (6, 1004), (6, 1012);

INSERT INTO `tb_attendance` (`club_id`, `user_id`, `clock_in_time`, `clock_out_time`, `study_duration`, `status`) VALUES
                                                                                                                      (1, 1001, '2024-10-10 14:00:00', '2024-10-10 16:00:00', 120, 0),
                                                                                                                      (1, 1007, '2024-10-10 14:05:00', '2024-10-10 15:45:00', 100, 0),
                                                                                                                      (1, 1008, '2024-10-10 14:10:00', '2024-10-10 15:30:00', 80, 0),
                                                                                                                      (2, 1002, '2024-10-11 15:00:00', '2024-10-11 17:30:00', 150, 0),
                                                                                                                      (2, 1010, '2024-10-11 15:05:00', '2024-10-11 17:00:00', 115, 0),
                                                                                                                      (3, 1003, '2024-10-12 19:00:00', '2024-10-12 21:00:00', 120, 0),
                                                                                                                      (3, 1011, '2024-10-12 19:05:00', '2024-10-12 20:45:00', 100, 0);

INSERT INTO `tb_achievement` (`club_id`, `publisher_id`, `title`, `type`, `description`, `achieve_date`, `status`) VALUES
                                                                                                                       (1, 101, '全国大学生编程竞赛一等奖', 'TEAM', '在全国大学生编程竞赛中获得一等奖', '2024-06-15', 1),
                                                                                                                       (1, 101, '校科技创新大赛金奖', 'TEAM', '在校科技创新大赛中获得金奖', '2024-05-20', 1),
                                                                                                                       (2, 101, '电子设计大赛省级二等奖', 'TEAM', '在省级电子设计大赛中获得二等奖', '2024-07-10', 1),
                                                                                                                       (3, 101, '校园艺术节最佳表演奖', 'TEAM', '在校园艺术节中获得最佳表演奖', '2024-04-25', 1),
                                                                                                                       (4, 101, '校际篮球联赛冠军', 'TEAM', '在校际篮球联赛中获得冠军', '2024-03-18', 1),
                                                                                                                       (5, 101, '优秀志愿服务团队', 'TEAM', '被评为市级优秀志愿服务团队', '2024-08-30', 1),
                                                                                                                       (6, 101, '创业计划大赛银奖', 'TEAM', '在创业计划大赛中获得银奖', '2024-09-12', 1);

INSERT INTO `tb_achievement_member` (`achievement_id`, `user_id`, `role`, `contribution`) VALUES
                                                                                              (1, 101, '队长', '负责核心算法设计和项目统筹'),
                                                                                              (1, 102, '队员', '负责前端界面开发'),
                                                                                              (1, 103, '队员', '负责后端服务开发'),
                                                                                              (3, 104, '队长', '负责电路设计和系统集成'),
                                                                                              (3, 105, '队员', '负责硬件调试和测试'),
                                                                                              (4, 106, '主唱', '负责主要演唱部分'),
                                                                                              (4, 107, '吉他手', '负责吉他伴奏');

INSERT INTO `tb_announcement` (`title`, `content`, `publisher_id`, `club_id`, `type`, `status`) VALUES
                                                                                                    ('编程竞赛培训通知', '本周六下午2点将在计算机学院实验室举行编程竞赛培训，请各位成员准时参加。', 101, 1, 'internal', 'published'),
                                                                                                    ('社团招新公告', '计算机协会开始招新啦！欢迎对编程感兴趣的同学加入我们！', 101, 1, 'public', 'published'),
                                                                                                    ('校园音乐节筹备会', '本周五晚上7点在音乐教室召开校园音乐节筹备会议，请核心成员务必参加。', 101, 3, 'internal', 'published'),
                                                                                                    ('新生杯篮球赛报名', '新生杯篮球赛开始报名，请有意参加的同学在本周五前到篮球社报名。', 101, 4, 'public', 'published'),
                                                                                                    ('校园清洁日活动', '本周日上午9点举行校园清洁日活动，欢迎大家积极参与。', 101, 5, 'public', 'published'),
                                                                                                    ('创业项目征集', '创业俱乐部开始征集优秀创业项目，有意者请联系负责人。', 101, 6, 'public', 'published'),
                                                                                                    ('电子设计培训', '电子创新社将于下周举办电子设计基础培训，欢迎报名。', 101, 2, 'public', 'published');