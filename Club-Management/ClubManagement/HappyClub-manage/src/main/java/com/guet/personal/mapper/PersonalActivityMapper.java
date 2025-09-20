package com.guet.personal.mapper;

import java.util.List;

import com.guet.personal.domain.Dto.Audit.PersonalActivityAuditDto;
import com.guet.personal.domain.Dto.PersonalActivityDto;
import com.guet.personal.domain.PersonalActivity;
import org.apache.ibatis.annotations.Param;

/**
 * 活动管理Mapper接口
 * 
 * @author kevin
 * @date 2025-05-01
 */
public interface PersonalActivityMapper
{
    /**
     * 查询活动管理
     * 
     * @param activityId 活动管理主键
     * @return 活动管理
     */
    public PersonalActivity selectPactivityByActivityId(Long activityId);

    /**
     * 查询活动管理列表
     * 
     * @param pactivity 活动管理
     * @return 活动管理集合
     */
    public List<PersonalActivity> selectPactivityList(PersonalActivityDto pactivity);

    /**
     * 新增活动管理
     * 
     * @param personalActivity 活动管理
     * @return 结果
     */
    public int insertPactivity(PersonalActivity personalActivity);

    /**
     * 修改活动管理
     * 
     * @param personalActivity 活动管理
     * @return 结果
     */
    public int updatePactivity(PersonalActivity personalActivity);

    /**
     * 删除活动管理
     * 
     * @param activityId 活动管理主键
     * @return 结果
     */
    public int deletePactivityByActivityId(Long activityId);

    /**
     * 批量删除活动管理
     * 
     * @param activityIds 需要删除的数据主键集合
     * @return 结果
     */
    public int deletePactivityByActivityIds(Long[] activityIds);

    public int insertPactivityAudit(PersonalActivityAuditDto pactivityAudit);

    public int insertActivityVisibility(@Param("activityId") Long activityId,@Param("clubId") Long clubId);
}
