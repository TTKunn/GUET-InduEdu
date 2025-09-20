package com.guet.happy.domain;

import com.guet.personal.domain.Vo.AchievementMemberVo;
import lombok.Data;

import java.sql.Timestamp;
import java.util.Date;
import java.util.List;

@Data
public class HAchievement {
    private Integer achievementId;
    private Integer clubId;
    private Integer publisherId;
    private String title;
    private String type;
    private String description;
    private Date achieveDate;
    private String certificateUrl;
    private String status;
    private Timestamp createdAt;
    private Date deletedAt;
    // nickName
    private String nickName;
    private List<AchievementMemberVo> participants;
}
