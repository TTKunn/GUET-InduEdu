package com.guet.happy.service.Impl;

import com.guet.happy.domain.HClub;
import com.guet.happy.domain.HUser;
import com.guet.happy.mapper.HUserMapper;
import com.guet.happy.service.HUserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class HUserServiceImpl implements HUserService {

    @Autowired
    private HUserMapper userMapper;

    @Override
    public HUser getUserById(Integer userId) {
        return userMapper.selectUserById(userId);
    }

    @Override
    public int updateUserInfo(HUser user) {
        return userMapper.updateUserInfo(user);
    }
    @Override
    public List<HClub> getJoinedClubs(Integer userId) {
        return userMapper.getJoinedClubs(userId);
    }
}
