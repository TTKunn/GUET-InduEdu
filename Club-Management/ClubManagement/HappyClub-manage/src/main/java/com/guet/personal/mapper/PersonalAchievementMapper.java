package com.guet.personal.mapper;

import java.util.List;

import com.guet.personal.domain.Dto.Audit.PersonalAchievementAuditDto;
import com.guet.personal.domain.Dto.PersonalAchievementDto;
import com.guet.personal.domain.PersonalAchievement;
import com.guet.personal.domain.Vo.PersonalAchievementVo;

/**
 * 成果管理Mapper接口
 * 
 * @author kevin
 * @date 2025-05-01
 */
public interface PersonalAchievementMapper
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
     * 删除成果管理
     * 
     * @param achievementId 成果管理主键
     * @return 结果
     */
    public int deletePachievementByAchievementId(Long achievementId);

    /**
     * 批量删除成果管理
     * 
     * @param achievementIds 需要删除的数据主键集合
     * @return 结果
     */
    public int deletePachievementByAchievementIds(Long[] achievementIds);

    public int insertPachievementAudit(PersonalAchievementAuditDto pachievementAudit);


}
