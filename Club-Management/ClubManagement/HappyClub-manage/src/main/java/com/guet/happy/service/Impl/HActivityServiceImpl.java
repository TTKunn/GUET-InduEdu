package com.guet.happy.service.Impl;

import com.guet.happy.domain.HActivity;
import com.guet.happy.mapper.HActivityMapper;
import com.guet.happy.service.HActivityService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class HActivityServiceImpl implements HActivityService {

    @Autowired
    private HActivityMapper hActivityMapper;

    @Override
    public List<HActivity> getPublicActivities() {
        return hActivityMapper.selectPublicActivity();
    }

    @Override
    public HActivity getActivityById(Integer activityId) {
        return hActivityMapper.selectActivityById(activityId);
    }

    @Override
    public int joinActivity(Long activityId, Long userId) {
        // 判断是否已经参加活动
        Boolean hasParticipated = hActivityMapper.selectActivityUser(activityId, userId);
        if (Boolean.TRUE.equals(hasParticipated)) {
            // 用户已参加该活动
            throw new RuntimeException("用户已参加该活动");
        } else {
            // 用户未参加该活动
            return hActivityMapper.participateActivity(activityId, userId);
        }
    }
    @Override
    public List<HActivity> getActivitiesByUserId(Long userId) {
        return hActivityMapper.selectActivitiesByUserId(userId);
    }

    @Override
    public List<HActivity> getInternalActivitiesByClubId(Long clubId) {
        return hActivityMapper.selectInnerActivity(clubId);
    }
    @Override
    public List<HActivity> getInnerActivityList(Long clubId) {
        return hActivityMapper.selectInnerActivityList(clubId);
    }

    @Override
    public List<HActivity> getPublicActivityList(Long clubId) {
        return hActivityMapper.selectPublicActivityList(clubId);
    }
    @Override
    public List<HActivity> getUserParticipatedActivities(Long userId) {
        return hActivityMapper.selectUserParticipatedActivities(userId);
    }
}
