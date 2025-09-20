package com.guet.personal.domain.Dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.guet.common.core.domain.BaseEntity;
import lombok.Data;

import java.util.Map;
@Data
public class PersonalAttendanceDto extends BaseEntity {
    private String clubName;                // 俱乐部名称，用于模糊查询
    private String userName;                // 用户名，用于模糊查询
    private String nickName;                // 昵称，用于模糊查询（与 userName 类似）
    private String status;
    @JsonInclude(JsonInclude.Include.NON_EMPTY)
    private Map<String, Object> params2;
    private Long clubId;
}
