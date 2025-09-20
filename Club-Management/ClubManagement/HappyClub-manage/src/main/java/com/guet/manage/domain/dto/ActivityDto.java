package com.guet.manage.domain.dto;

import com.guet.common.core.domain.BaseEntity;
import lombok.Data;

@Data
public class ActivityDto extends BaseEntity {
    private String name;                // 活动名称
    private String description;         // 活动描述
    private String nickName;            // 组织者昵称（用户名）
    private String clubName;            // 所属社团名称
    private String userName;            // 用户名（可用于模糊搜索组织者）
    private String location;            // 活动地点
    private String status;
}
