package com.guet.happy.service;

import com.guet.happy.domain.HMember;
import java.util.List;

public interface HMemberService {

    HMember getMemberByUserId(Integer userId);

    List<HMember> getMembersByClubId(Integer clubId);

    boolean isMember(Integer userId, Integer clubId);

    // exitClub
    boolean quitClub(Integer userId, Integer clubId,String remark);

    // joinClub
    boolean joinClub(Integer userId, Integer clubId,String remark);

}
