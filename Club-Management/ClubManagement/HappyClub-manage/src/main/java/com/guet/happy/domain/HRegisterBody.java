package com.guet.happy.domain;

import lombok.Data;

@Data
public class HRegisterBody {
    private String username;
    private String password;
    private String name;
    private Long deptId;
    private String gender;
}
