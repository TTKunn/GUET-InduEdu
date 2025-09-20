package com.guet.manage.domain.vo;

import com.guet.manage.domain.Announcement;
import lombok.Data;

@Data
public class AnnouncementVo extends Announcement {
    private String userName;
    private String clubName;
    private String nickName;
}
