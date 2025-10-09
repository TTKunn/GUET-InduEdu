CREATE TABLE `tb_club` (
   `club_id`      bigint       NOT NULL AUTO_INCREMENT COMMENT '社团主键ID',
   `name`         varchar(100) NOT NULL COMMENT '社团名称',
   `description`  text COMMENT '社团简介',
   `category_id`  bigint       NOT NULL COMMENT '所属分类ID',
   `leader_id`    bigint       NOT NULL COMMENT '社长（用户ID）',
   `dept_id`      bigint       NOT NULL COMMENT '所属院系ID',
   `status`       tinyint      DEFAULT 0 COMMENT '状态（0正常 1停用）',
   `logo_url`     varchar(255) DEFAULT NULL COMMENT '社团Logo URL',
   `created_at`   datetime     DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
   `deleted_at`   datetime     DEFAULT NULL COMMENT '软删除时间',
   PRIMARY KEY (`club_id`),
   KEY `idx_leader` (`leader_id`),
   KEY `idx_category` (`category_id`),
   KEY `idx_dept` (`dept_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='社团主表';

CREATE TABLE `tb_attendance` (
     `attendance_id`  bigint       NOT NULL AUTO_INCREMENT COMMENT '主键ID',
     `club_id`        bigint       NOT NULL COMMENT '社团ID',
     `user_id`        bigint       NOT NULL COMMENT '用户ID',
     `clock_in_time`  datetime     DEFAULT NULL COMMENT '签到时间',
     `clock_out_time` datetime     DEFAULT NULL COMMENT '签退时间',
     `study_duration` int          DEFAULT NULL COMMENT '学习时长(分钟)',
     `status`         tinyint      DEFAULT 0 COMMENT '状态 0正常 1异常',
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
   `status`          tinyint      DEFAULT 0 COMMENT '状态 0待审核 1已通过 2已驳回',
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
   `status`       tinyint      DEFAULT 0 COMMENT '状态 0待审核 1已通过 2已驳回',
   `deleted_at`   datetime     DEFAULT NULL COMMENT '软删除时间',
   PRIMARY KEY (`activity_id`),
   KEY `idx_act_club`     (`club_id`),
   KEY `idx_act_organizer`(`organizer_id`)
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
     `status`               tinyint      DEFAULT 0 COMMENT '状态 0正常 1退出 2被移出',
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