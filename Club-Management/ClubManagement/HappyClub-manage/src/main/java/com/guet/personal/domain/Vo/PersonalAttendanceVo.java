package com.guet.personal.domain.Vo;

import com.guet.personal.domain.PersonalAttendance;
import lombok.Data;

@Data
public class PersonalAttendanceVo extends PersonalAttendance {
    private String clubName;
    private String userName;
    private String nickName;
}
