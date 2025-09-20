package com.guet.personal.domain.Vo;

import com.guet.personal.domain.Membership;
import lombok.Data;

@Data
public class MembershipVo extends Membership {
    private Long userId;
    private String nickName;
    private String userName;
//     activityParticipation
    private String activityParticipation;
    //achievementCount
    private String achievementCount;
}
