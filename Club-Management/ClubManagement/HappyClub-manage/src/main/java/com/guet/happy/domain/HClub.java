package com.guet.happy.domain;

import lombok.Data;

@Data
public class HClub {
    private Integer clubId;
    private String name;
    private String description;
    private Integer categoryId;
    private Integer leaderId;
    private Integer primaryAdvisorId;
    private Long deptId;
    private String createdAt;
    private String status;
    private String logoUrl;
    private String deletedAt;
    private Integer memberCount; // 成员数量
    private Integer activeMemberCount; // 活跃成员数量
    private Integer activityCount; // 活动数量
    private Integer totalMembersEver; // 历史总成员数
    // joinTime
    private String joinTime;
    // 新增关联字段
    private Integer userId;
    private String username;
    private String nickName;
    private String deptName;
    private String categoryName;
}
