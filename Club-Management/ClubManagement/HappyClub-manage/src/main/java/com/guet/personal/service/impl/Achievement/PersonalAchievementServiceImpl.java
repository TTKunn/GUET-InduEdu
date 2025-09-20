package com.guet.personal.service.impl.Achievement;

import java.util.List;

import com.guet.personal.domain.Dto.Audit.PersonalAchievementAuditDto;
import com.guet.personal.domain.Dto.PersonalAchievementDto;
import com.guet.personal.domain.Vo.PersonalAchievementVo;
import com.guet.personal.mapper.AchievementMemberMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.guet.personal.mapper.PersonalAchievementMapper;
import com.guet.personal.domain.PersonalAchievement;
import com.guet.personal.service.IPersonalAchievementService;
import org.springframework.transaction.annotation.Transactional;

import javax.annotation.Resource;

/**
 * 成果管理Service业务层处理
 * 
 * @author kevin
 * @date 2025-05-01
 */
@Service
public class PersonalAchievementServiceImpl implements IPersonalAchievementService
{
    @Resource
    private PersonalAchievementMapper personalAchievementMapper;

    @Autowired
    private AchievementMemberMapper achievementMemberMapper;

    /**
     * 查询成果管理
     * 
     * @param achievementId 成果管理主键
     * @return 成果管理
     */
    @Override
    public PersonalAchievement selectPachievementByAchievementId(Long achievementId)
    {
        return personalAchievementMapper.selectPachievementByAchievementId(achievementId);
    }

    /**
     * 查询成果管理列表
     * 
     * @param pachievement 成果管理
     * @return 成果管理
     */
    @Override
    public List<PersonalAchievementVo> selectPachievementList(PersonalAchievementDto pachievement)
    {
        // 自动分组处理（MyBatis的嵌套结果映射会自动处理分组）
        return personalAchievementMapper.selectPachievementList(pachievement);
    }

    /**
     * 新增成果管理
     * 
     * @param personalAchievement 成果管理
     * @return 结果
     */
    @Override
    @Transactional
    public int insertPachievement(PersonalAchievement personalAchievement)
    {
        // 新增成果管理
        personalAchievementMapper.insertPachievement(personalAchievement);
        Long generatedId = personalAchievement.getAchievementId();
        Long achievementId = personalAchievement.getAchievementId();
        // System.out.println("generatedId: " + generatedId);
        // 创建一个AuditDto对象
        PersonalAchievementAuditDto pachievementAuditDto = new PersonalAchievementAuditDto();

        pachievementAuditDto.setAchievementId(generatedId);
        pachievementAuditDto.setApplicantId(personalAchievement.getPublisherId());
        pachievementAuditDto.setType("achievement");
        pachievementAuditDto.setStatus("pending");

        // 插入关联表
        if(personalAchievement.getParticipantIds() != null
                && !personalAchievement.getParticipantIds().isEmpty()){
            achievementMemberMapper.batchInsertAchievementMember(
                    achievementId,
                    personalAchievement.getParticipantIds()
            );
        }
        // 插入审核信息
        personalAchievementMapper.insertPachievementAudit(pachievementAuditDto);

        return 1;
    }

    /**
     * 修改成果管理
     * 
     * @param personalAchievement 成果管理
     * @return 结果
     */
    @Override
    public int updatePachievement(PersonalAchievement personalAchievement)
    {
        return personalAchievementMapper.updatePachievement(personalAchievement);
    }

    /**
     * 批量删除成果管理
     * 
     * @param achievementIds 需要删除的成果管理主键
     * @return 结果
     */
    @Override
    public int deletePachievementByAchievementIds(Long[] achievementIds)
    {
        return personalAchievementMapper.deletePachievementByAchievementIds(achievementIds);
    }

    /**
     * 删除成果管理信息
     * 
     * @param achievementId 成果管理主键
     * @return 结果
     */
    @Override
    public int deletePachievementByAchievementId(Long achievementId)
    {
        return personalAchievementMapper.deletePachievementByAchievementId(achievementId);
    }
}
