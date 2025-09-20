package com.guet.personal.service.impl.Activity;

import java.util.List;
import java.util.Objects;

import com.guet.personal.domain.Dto.Audit.PersonalActivityAuditDto;
import com.guet.personal.domain.Dto.PersonalActivityDto;
import org.springframework.stereotype.Service;
import com.guet.personal.mapper.PersonalActivityMapper;
import com.guet.personal.domain.PersonalActivity;
import com.guet.personal.service.IPersonalActivityService;
import org.springframework.transaction.annotation.Transactional;

import javax.annotation.Resource;

/**
 * 活动管理Service业务层处理
 * 
 * @author kevin
 * @date 2025-05-01
 */
@Service
public class PersonalActivityServiceImpl implements IPersonalActivityService
{
    @Resource
    private PersonalActivityMapper personalActivityMapper;

    /**
     * 查询活动管理
     * 
     * @param activityId 活动管理主键
     * @return 活动管理
     */
    @Override
    public PersonalActivity selectPactivityByActivityId(Long activityId)
    {
        return personalActivityMapper.selectPactivityByActivityId(activityId);
    }

    /**
     * 查询活动管理列表
     * 
     * @param pactivity 活动管理
     * @return 活动管理
     */
    @Override
    public List<PersonalActivity> selectPactivityList(PersonalActivityDto pactivity)
    {
        return personalActivityMapper.selectPactivityList(pactivity);
    }

    /**
     * 新增活动管理
     * 
     * @param personalActivity 活动管理
     * @return 结果
     */
    @Override
    @Transactional
    public int insertPactivity(PersonalActivity personalActivity)
    {
        // 公开活动 需要加入审核记录
        if (Objects.equals(personalActivity.getVisibility(), "public")){
            // 构建审核记录对象
            PersonalActivityAuditDto pactivityAudit = new PersonalActivityAuditDto();
            // 插入活动记录 获取生成的id
            personalActivityMapper.insertPactivity(personalActivity);
            Long generatedId = personalActivity.getActivityId();
            // 赋值审核记录对象
            pactivityAudit.setActivityId(generatedId);
            pactivityAudit.setApplicantId(personalActivity.getOrganizerId());
            pactivityAudit.setType("activity");
            pactivityAudit.setStatus("pending");
            // 插入审核记录
            return personalActivityMapper.insertPactivityAudit(pactivityAudit);
        }
        // 私有活动 直接插入
        else {
            personalActivityMapper.insertPactivity(personalActivity);
            Long generatedId = personalActivity.getActivityId();
            // 插入活动可见性记录 仅本社团可见
            return personalActivityMapper.insertActivityVisibility(generatedId, personalActivity.getClubId());
        }
    }

    /**
     * 修改活动管理
     * 
     * @param personalActivity 活动管理
     * @return 结果
     */
    @Override
    public int updatePactivity(PersonalActivity personalActivity)
    {
        return personalActivityMapper.updatePactivity(personalActivity);
    }

    /**
     * 批量删除活动管理
     * 
     * @param activityIds 需要删除的活动管理主键
     * @return 结果
     */
    @Override
    public int deletePactivityByActivityIds(Long[] activityIds)
    {
        return personalActivityMapper.deletePactivityByActivityIds(activityIds);
    }

    /**
     * 删除活动管理信息
     * 
     * @param activityId 活动管理主键
     * @return 结果
     */
    @Override
    public int deletePactivityByActivityId(Long activityId)
    {
        return personalActivityMapper.deletePactivityByActivityId(activityId);
    }
}
