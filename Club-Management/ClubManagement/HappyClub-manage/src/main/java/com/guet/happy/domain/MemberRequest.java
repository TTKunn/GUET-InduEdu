package com.guet.happy.domain;

import lombok.Data;

@Data
public class MemberRequest {
    private Integer userId;
    private Integer clubId;
    private String remark;
}