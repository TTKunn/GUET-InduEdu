package com.guet.personal.domain.Vo;

import lombok.Data;

@Data
public class MemberAchievementsVo {
    private Long achievementId;
    private String title;
    private String type;
    private String description;
    private String achieveDate;
    private String certificateUrl;
    private String status;
    private String createdAt;
    private String role;
    private String contribution;
}
