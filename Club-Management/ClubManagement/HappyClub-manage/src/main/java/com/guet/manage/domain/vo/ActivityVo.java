package com.guet.manage.domain.vo;

import com.guet.common.annotation.Excel;
import com.guet.manage.domain.Activity;
import lombok.Data;

@Data
public class ActivityVo extends Activity {
    @Excel(name = "社团名称")
    private String clubName;
    @Excel(name = "活动发起人")
    private String userName;
    private String nickName;
}
