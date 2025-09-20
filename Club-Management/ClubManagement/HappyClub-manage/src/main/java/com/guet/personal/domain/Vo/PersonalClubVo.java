package com.guet.personal.domain.Vo;

import com.guet.personal.domain.PersonalClub;
import lombok.Data;

@Data
public class PersonalClubVo extends PersonalClub {
    // user_name
    private String userName;
    // nick_name
    private String nickName;
    //club_name
    private String clubName;
    //club_description
    private String clubDescription;
    //category_name
    private String categoryName;
    //dept_name
    private String deptName;
    // advisorNames
    private String advisorNames;
    //advisorIds
    private String advisorIds;


}
