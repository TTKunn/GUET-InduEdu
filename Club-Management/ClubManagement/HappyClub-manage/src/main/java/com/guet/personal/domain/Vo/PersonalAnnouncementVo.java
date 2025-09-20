package com.guet.personal.domain.Vo;

import com.guet.personal.domain.PersonalAnnouncement;
import lombok.Data;

@Data
public class PersonalAnnouncementVo extends PersonalAnnouncement {
    private String clubName;
    private String userName;
    private String nickName;
}
