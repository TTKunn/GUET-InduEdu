package com.guet.manage.service.impl;

import java.util.List;

import com.guet.manage.domain.dto.AchievementDto;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.guet.manage.mapper.AchievementMapper;
import com.guet.manage.domain.Achievement;
import com.guet.manage.service.IAchievementService;

/**
 * 成果管理Service业务层处理
 * 
 * @author kevin
 * @date 2025-04-30
 */
@Service
public class AchievementServiceImpl implements IAchievementService 
{
    @Autowired
    private AchievementMapper achievementMapper;

    /**
     * 查询成果管理
     * 
     * @param achievementId 成果管理主键
     * @return 成果管理
     */
    @Override
    public Achievement selectAchievementByAchievementId(Long achievementId)
    {
        return achievementMapper.selectAchievementByAchievementId(achievementId);
    }

    /**
     * 查询成果管理列表
     * 
     * @param achievement 成果管理
     * @return 成果管理
     */
    @Override
    public List<Achievement> selectAchievementList(AchievementDto achievement)
    {
        return achievementMapper.selectAchievementList(achievement);
    }

    /**
     * 新增成果管理
     * 
     * @param achievement 成果管理
     * @return 结果
     */
    @Override
    public int insertAchievement(Achievement achievement)
    {
        return achievementMapper.insertAchievement(achievement);
    }

    /**
     * 修改成果管理
     * 
     * @param achievement 成果管理
     * @return 结果
     */
    @Override
    public int updateAchievement(Achievement achievement)
    {
        return achievementMapper.updateAchievement(achievement);
    }

    /**
     * 批量删除成果管理
     * 
     * @param achievementIds 需要删除的成果管理主键
     * @return 结果
     */
    @Override
    public int deleteAchievementByAchievementIds(Long[] achievementIds)
    {
        return achievementMapper.deleteAchievementByAchievementIds(achievementIds);
    }

    /**
     * 删除成果管理信息
     * 
     * @param achievementId 成果管理主键
     * @return 结果
     */
    @Override
    public int deleteAchievementByAchievementId(Long achievementId)
    {
        return achievementMapper.deleteAchievementByAchievementId(achievementId);
    }
}
