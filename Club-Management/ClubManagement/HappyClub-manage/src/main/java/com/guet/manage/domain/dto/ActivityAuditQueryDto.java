package com.guet.manage.domain.dto;

import com.guet.common.core.domain.BaseEntity;
import lombok.Data;

@Data
public class ActivityAuditQueryDto extends BaseEntity {
    // 活动核心信息
    private String activityName;     // 活动名称
    private String location;         // 活动地点
    // 关联信息
    private String clubName;         // 所属社团
    private String leaderName;       // 负责人姓名
}
