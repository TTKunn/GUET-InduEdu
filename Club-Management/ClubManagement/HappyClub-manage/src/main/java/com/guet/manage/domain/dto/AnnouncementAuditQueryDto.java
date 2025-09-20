package com.guet.manage.domain.dto;

import com.guet.common.core.domain.BaseEntity;
import lombok.Data;

@Data
public class AnnouncementAuditQueryDto extends BaseEntity {
    private String title;
    private String content;
    private String leaderName;
    private String clubName;
}
