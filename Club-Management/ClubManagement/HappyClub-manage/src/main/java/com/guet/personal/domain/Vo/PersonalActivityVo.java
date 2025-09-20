package com.guet.personal.domain.Vo;

import com.guet.common.annotation.Excel;
import com.guet.personal.domain.PersonalActivity;
import lombok.Data;

@Data
public class PersonalActivityVo extends PersonalActivity {
    @Excel(name = "社团名称")
    private String clubName;
    @Excel(name = "活动发起人")
    private String userName;
    private String nickName;
}
