package com.guet.personal.domain.Dto;

import com.guet.common.core.domain.BaseEntity;

import lombok.Data;

@Data
public class MembershipDto extends BaseEntity {
    private String userName;
    private String nickName;
    private Long clubId;
    private String status;
    private String totalStudyDuration;
}
