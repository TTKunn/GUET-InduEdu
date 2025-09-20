package com.guet.manage.domain.vo;

import com.guet.common.core.domain.entity.SysUser;
import com.guet.manage.domain.Attendance;
import lombok.Data;

@Data
public class AttendanceVo extends Attendance {
    private String clubName;
    private String userName;
    private String nickName;
}
