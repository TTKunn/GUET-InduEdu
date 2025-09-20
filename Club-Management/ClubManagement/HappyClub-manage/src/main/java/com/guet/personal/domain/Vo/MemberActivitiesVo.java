package com.guet.personal.domain.Vo;

import lombok.Data;

@Data
public class MemberActivitiesVo {
    private String name;
    private String description;
    private String startTime;
    private String location;
    private String publishTime;
    private Long activityId;
    private String participation;
    private String endTime;
}
