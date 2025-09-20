package com.guet.manage.service;

import java.util.List;
import com.guet.manage.domain.Achievement;
import com.guet.manage.domain.dto.AchievementDto;

/**
 * 成果管理Service接口
 * 
 * @author kevin
 * @date 2025-04-30
 */
public interface IAchievementService 
{
    /**
     * 查询成果管理
     * 
     * @param achievementId 成果管理主键
     * @return 成果管理
     */
    public Achievement selectAchievementByAchievementId(Long achievementId);

    /**
     * 查询成果管理列表
     * 
     * @param achievement 成果管理
     * @return 成果管理集合
     */
    public List<Achievement> selectAchievementList(AchievementDto achievement);

    /**
     * 新增成果管理
     * 
     * @param achievement 成果管理
     * @return 结果
     */
    public int insertAchievement(Achievement achievement);

    /**
     * 修改成果管理
     * 
     * @param achievement 成果管理
     * @return 结果
     */
    public int updateAchievement(Achievement achievement);

    /**
     * 批量删除成果管理
     * 
     * @param achievementIds 需要删除的成果管理主键集合
     * @return 结果
     */
    public int deleteAchievementByAchievementIds(Long[] achievementIds);

    /**
     * 删除成果管理信息
     * 
     * @param achievementId 成果管理主键
     * @return 结果
     */
    public int deleteAchievementByAchievementId(Long achievementId);
}
