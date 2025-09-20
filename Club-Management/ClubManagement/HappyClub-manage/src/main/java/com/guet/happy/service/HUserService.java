package com.guet.happy.service;

import com.guet.happy.domain.HClub;
import com.guet.happy.domain.HUser;
import org.springframework.stereotype.Service;

import java.util.List;

public interface HUserService {
    HUser getUserById(Integer userId);
    /**
     * 更新用户个人信息
     * @param user 用户信息对象
     * @return 影响的行数
     */
    int updateUserInfo(HUser user);
    List<HClub> getJoinedClubs(Integer userId);
}
