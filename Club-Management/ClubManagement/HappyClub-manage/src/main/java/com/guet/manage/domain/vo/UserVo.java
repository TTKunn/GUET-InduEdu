package com.guet.manage.domain.vo;

import com.guet.common.core.domain.entity.SysUser;
import lombok.Data;

import java.util.Date;

@Data
public class UserVo extends SysUser {
    // 在社状态：'probation','active','graduated','quit'
    private String status;
    // 加入时间
    private Date joinTime;
    // 退出时间
    private Date exitTime;
}
