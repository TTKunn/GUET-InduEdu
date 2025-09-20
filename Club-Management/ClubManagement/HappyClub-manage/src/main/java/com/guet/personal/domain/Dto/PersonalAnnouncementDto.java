package com.guet.personal.domain.Dto;

import com.guet.common.core.domain.BaseEntity;
import lombok.Data;

@Data
public class PersonalAnnouncementDto extends BaseEntity {
    private String userName;                // 用户名，用于模糊查询
    private String nickName;                // 昵称，用于模糊查询（与 userName 类似）
    private String status;
    private String title;
    private String content;
    private Long clubId;
    private String type;
}
