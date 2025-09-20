package com.guet.personal.service;

import java.util.List;

import com.guet.personal.domain.Dto.PersonalActivityDto;
import com.guet.personal.domain.PersonalActivity;

/**
 * 活动管理Service接口
 * 
 * @author kevin
 * @date 2025-05-01
 */
public interface IPersonalActivityService
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
     * 批量删除活动管理
     * 
     * @param activityIds 需要删除的活动管理主键集合
     * @return 结果
     */
    public int deletePactivityByActivityIds(Long[] activityIds);

    /**
     * 删除活动管理信息
     * 
     * @param activityId 活动管理主键
     * @return 结果
     */
    public int deletePactivityByActivityId(Long activityId);
}
