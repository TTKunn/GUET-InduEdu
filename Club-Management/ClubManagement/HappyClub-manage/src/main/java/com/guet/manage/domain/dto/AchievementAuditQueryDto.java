package com.guet.manage.domain.dto;

import com.guet.common.core.domain.BaseEntity;
import lombok.Data;

@Data
public class AchievementAuditQueryDto extends BaseEntity {
    private String achievementTitle;
    private String clubName;
    private Long leaderId;
    private String type;
}
