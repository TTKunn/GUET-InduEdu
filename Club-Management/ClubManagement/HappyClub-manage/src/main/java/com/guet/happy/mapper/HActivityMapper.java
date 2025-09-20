package com.guet.happy.mapper;

import com.guet.happy.domain.HActivity;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;

@Mapper
public interface HActivityMapper {

    /**
     * 查询公开活动列表（包含id和名称）
     */
    List<HActivity> selectPublicActivity();

    /**
     * 根据ID查询活动详情
     */
    HActivity selectActivityById(Integer activityId);

    /**
     * 参加活动
     */
    int participateActivity(@Param("activityId") Long activityId, @Param("userId") Long userId);

Boolean selectActivityUser(@Param("activityId") Long activityId, @Param("userId") Long userId);
    /**
     * 根据用户ID查询其参与的活动列表
     */
    List<HActivity> selectActivitiesByUserId(Long userId);
    /**
     * 根据社团ID查询所有内部活动
     */
    List<HActivity> selectInnerActivity(Long clubId);
    /**
     * 根据社团ID获取该社团的内部活动列表
     */
    List<HActivity> selectInnerActivityList(Long clubId);

    List<HActivity> selectPublicActivityList(Long clubId);
    List<HActivity> selectUserParticipatedActivities(Long userId);
}
