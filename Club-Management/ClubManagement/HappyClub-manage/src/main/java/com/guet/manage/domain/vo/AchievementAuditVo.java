package com.guet.manage.domain.vo;

import lombok.Data;

@Data
public class AchievementAuditVo {
    private Long achievementId;
    private String title;
    private String description;
    private String leaderName;
    private String achieveDate;
    private String clubName;
    private Long auditId;            // 审核记录ID
    private String status;           // 审核状态（pending/approved/rejected）
    private String userRemark;      // 审核备注
    private String type;              // 成果类型（例如：论文、比赛）
    private String certificateUrl;    // 证书URL
    private String createdAt;         // 创建时间

}
