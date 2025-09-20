package com.guet.happy.service;

import com.guet.happy.domain.HActivity;

import java.util.List;

public interface HActivityService {
    List<HActivity> getPublicActivities();
    HActivity getActivityById(Integer activityId);
    int joinActivity(Long activityId, Long userId);
    List<HActivity> getActivitiesByUserId(Long userId);
    List<HActivity> getInternalActivitiesByClubId(Long clubId);
    List<HActivity> getInnerActivityList(Long clubId);

    List<HActivity> getPublicActivityList(Long clubId);
    public List<HActivity> getUserParticipatedActivities(Long useId);
}
