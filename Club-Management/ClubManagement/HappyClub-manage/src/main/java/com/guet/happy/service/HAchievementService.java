package com.guet.happy.service;

import com.guet.happy.domain.HAchievement;
import java.util.List;

public interface HAchievementService {
    List<HAchievement> getAchievementsByClubId(Integer clubId);
    HAchievement getAchievementById(Integer achievementId);
}
