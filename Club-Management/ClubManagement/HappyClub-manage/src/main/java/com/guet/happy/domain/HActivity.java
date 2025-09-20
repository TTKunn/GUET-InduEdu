package com.guet.happy.domain;

import lombok.Data;

import java.sql.Timestamp;
import java.util.Date;

@Data
public class HActivity {

    private Integer activityId;      // 活动ID
    private Integer clubId;          // 俱乐部ID
    private String name;             // 活动名称
    private String description;      // 描述
    private Date startTime;          // 开始时间
    private Date endTime;            // 结束时间
    private String location;         // 地点
    private Integer organizerId;     // 组织者ID
    private String visibility;       // 可见性
    private String status;           // 状态
    private Date deletedAt;          // 删除时间
    private Date publishTime;        // 发布时间
    private Boolean isUrgent;        // 是否紧急

    // 额外字段（用于展示）
    private String nickName;         // 组织者的昵称
    private String clubName;         // 俱乐部名称

    // isEnded
    private Integer isEnded;
    private Integer participantCount;
}
