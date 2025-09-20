package com.guet.manage.domain.vo;

import com.guet.common.core.domain.BaseEntity;
import lombok.Data;

@Data
public class ClubLeaderVo extends BaseEntity
{
    private String leaderName;
    private Long leaderId;
}
