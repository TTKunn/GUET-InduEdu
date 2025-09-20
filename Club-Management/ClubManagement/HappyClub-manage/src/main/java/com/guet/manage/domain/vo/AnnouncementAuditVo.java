package com.guet.manage.domain.vo;

import com.guet.common.core.domain.BaseEntity;
import lombok.Data;

/**
 * 公告审核信息值对象类
 * 用于封装公告审核相关的数据，包括公告基本信息和审核状态
 */
@Data
public class AnnouncementAuditVo extends BaseEntity {
    /**
     * 公告ID，唯一标识一条公告
     */
    private Long announcementId;

    /**
     * 公告标题
     */
    private String title;

    /**
     * 公告内容
     */
    private String content;

    /**
     * 负责人姓名，表示公告的发布者或责任人
     */
    private String leaderName;

    /**
     * 公告创建时间，字符串格式
     */
    private String createAt;

    /**
     * 所属社团名称
     */
    private String clubName;

    /**
     * 审核记录ID，关联到审核表的主键
     */
    private Long auditId;

    /**
     * 公告审核状态
     * 可能的值包括：pending(待审核)、published(已发布)、rejected(已拒绝)等
     */
    private String status;

    /**
     * 用户备注信息，可用于记录额外说明或审核意见
     */
    private String userRemark;
    private String auCreatedAt;
}