package com.guet.manage.domain.vo;

import com.guet.manage.domain.Achievement;
import lombok.Data;

@Data
public class AchievementVo extends Achievement {
    private String clubName;
    private String userName;
    private String nickName;
}
