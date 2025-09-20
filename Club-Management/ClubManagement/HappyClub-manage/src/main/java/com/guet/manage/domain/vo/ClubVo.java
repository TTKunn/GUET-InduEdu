package com.guet.manage.domain.vo;


import com.guet.common.core.domain.entity.SysDept;
import com.guet.common.core.domain.entity.SysUser;
import com.guet.manage.domain.MCategory;
import lombok.Data;

@Data
public class ClubVo extends Club {
    //社团人数
    private int memberCount;
    //社团分类
    private MCategory MCategory;
    //社团负责人
    private SysUser sysUser;
    //社团学院
    private SysDept sysDept;
    private String clubName;
}
