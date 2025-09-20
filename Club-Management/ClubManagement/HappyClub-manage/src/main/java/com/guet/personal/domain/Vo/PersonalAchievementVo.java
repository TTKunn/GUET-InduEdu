package com.guet.personal.domain.Vo;

import com.guet.personal.domain.PersonalAchievement;
import lombok.Data;

import java.util.List;

@Data
public class PersonalAchievementVo extends PersonalAchievement {
    private String clubName;
    private String userName;
    private String nickName;
    private List<AchievementMemberVo> participants;
}
