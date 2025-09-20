package com.guet.personal.service;

import java.util.List;

import com.guet.personal.domain.Dto.PersonalAchievementDto;
import com.guet.personal.domain.PersonalAchievement;
import com.guet.personal.domain.Vo.PersonalAchievementVo;

/**
 * 成果管理Service接口
 * 
 * @author kevin
 * @date 2025-05-01
 */
public interface IPersonalAchievementService
{
    /**
     * 查询成果管理
     * 
     * @param achievementId 成果管理主键
     * @return 成果管理
     */
    public PersonalAchievement selectPachievementByAchievementId(Long achievementId);

    /**
     * 查询成果管理列表
     * 
     * @param pachievement 成果管理
     * @return 成果管理集合
     */
    public List<PersonalAchievementVo> selectPachievementList(PersonalAchievementDto pachievement);

    /**
     * 新增成果管理
     * 
     * @param personalAchievement 成果管理
     * @return 结果
     */
    public int insertPachievement(PersonalAchievement personalAchievement);

    /**
     * 修改成果管理
     * 
     * @param personalAchievement 成果管理
     * @return 结果
     */
    public int updatePachievement(PersonalAchievement personalAchievement);

    /**
     * 批量删除成果管理
     * 
     * @param achievementIds 需要删除的成果管理主键集合
     * @return 结果
     */
    public int deletePachievementByAchievementIds(Long[] achievementIds);

    /**
     * 删除成果管理信息
     * 
     * @param achievementId 成果管理主键
     * @return 结果
     */
    public int deletePachievementByAchievementId(Long achievementId);
}
