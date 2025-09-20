package com.guet.happy.domain;

import lombok.Data;

@Data
public class HUser {
    private Integer userId;
    private String username;
    private String nickName;
    private String email;
    private String phonenumber;
    private String sex;
    private String avatar;
    private String password;
    // 新增字段
    private Long deptId;
    private String deptName;
}
