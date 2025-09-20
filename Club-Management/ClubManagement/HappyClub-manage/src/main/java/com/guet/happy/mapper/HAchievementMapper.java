package com.guet.happy.mapper;

import com.guet.happy.domain.HAchievement;
import org.apache.ibatis.annotations.Param;

import java.util.List;

public interface HAchievementMapper {
    // 根据社团ID查询所有成果
    List<HAchievement> selectAchievementByClubId(@Param("clubId") Integer clubId);

    // 根据成果ID查询单个成果
    HAchievement selectAchievementById(@Param("achievementId") Integer achievementId);
}
