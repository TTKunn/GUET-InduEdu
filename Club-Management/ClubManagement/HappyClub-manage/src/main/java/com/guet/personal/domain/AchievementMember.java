// AchievementMember.java
package com.guet.personal.domain;

import lombok.Data;

import java.util.Date;

@Data
public class AchievementMember {
    private Integer achievementMemberId;
    private Integer achievementId;
    private Integer membershipId;
    private String role;
    private String contribution;
    private Date createdAt;
}