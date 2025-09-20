package com.guet.manage.domain.dto;

import com.guet.common.core.domain.BaseEntity;
import lombok.Data;

@Data
public class AchievementDto extends BaseEntity {
    private String clubName;                // 俱乐部名称，用于模糊查询
    private String userName;                // 用户名，用于模糊查询
    private String nickName;                // 昵称，用于模糊查询（与 userName 类似）
    private String status;
    private String title;
    private String type;
}
