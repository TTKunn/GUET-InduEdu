package com.guet.manage.domain.vo;

import com.guet.common.core.domain.BaseEntity;
import lombok.Data;

/**
 * 活动审核视图对象
 * 继承BaseEntity获取若依框架基础字段（createBy/createTime/updateBy等）
 */
@Data
public class ActivityAuditVo extends BaseEntity {
    // 活动核心信息
    private Long activityId;        // 活动ID
    private String activityName;     // 活动名称
    private String location;         // 活动地点

    // 时间信息
    private String startTime;  // 活动开始时间
    private String endTime;    // 活动结束时间

    // 审核相关字段
    private Long auditId;            // 审核记录ID
    private String status;           // 审核状态（pending/approved/rejected）
    private String userRemark;      // 审核备注

    // 关联信息
    private String clubName;         // 所属社团
    private String leaderName;       // 负责人姓名

    private String activityDescription;

}