package com.guet.happy.service.Impl;

import com.guet.happy.domain.HAchievement;
import com.guet.happy.mapper.HAchievementMapper;
import com.guet.happy.service.HAchievementService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class HAchievementServiceImpl implements HAchievementService {

    @Autowired
    private HAchievementMapper hAchievementMapper;

    @Override
    public List<HAchievement> getAchievementsByClubId(Integer clubId) {
        return hAchievementMapper.selectAchievementByClubId(clubId);
    }

    @Override
    public HAchievement getAchievementById(Integer achievementId) {
        return hAchievementMapper.selectAchievementById(achievementId);
    }
}
