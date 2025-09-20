package com.guet.happy.controller;

import com.guet.common.core.domain.AjaxResult;
import com.guet.happy.domain.ActivityRequest;
import com.guet.happy.domain.HActivity;
import com.guet.happy.service.HActivityService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("happy/activities")
public class HActivityController {

    @Autowired
    private HActivityService hActivityService;

    /**
     * 获取公开活动列表
     */
    @GetMapping("/public")
    public AjaxResult getPublicActivities() {
        return AjaxResult.success(hActivityService.getPublicActivities());
    }

    /**
     * 根据ID获取活动详情
     */
    @GetMapping("/{id}")
    public AjaxResult getActivityById(@PathVariable("id") Integer activityId) {
        return AjaxResult.success(hActivityService.getActivityById(activityId));
    }

    /**
     * 用户报名参加活动
     */
    @PostMapping("/join")
    public AjaxResult joinActivity(@RequestBody ActivityRequest request) {
        return AjaxResult.success(hActivityService.joinActivity(request.getActivityId(), request.getUserId()));
    }

    /**
     * 获取用户参与的活动列表
     */
    @GetMapping("/user/{userId}")
    public AjaxResult getActivitiesByUserId(@PathVariable Long userId) {
        List<HActivity> activities = hActivityService.getActivitiesByUserId(userId);
        return AjaxResult.success(activities);
    }

    /**
     * 获取某个社团的内部活动
     */
    @GetMapping("/internal/{clubId}")
    public AjaxResult getInternalActivities(@PathVariable Long clubId) {
        List<HActivity> activities = hActivityService.getInternalActivitiesByClubId(clubId);
        return AjaxResult.success(activities);
    }

    /**
     * 获取某个社团的内部活动列表
     */
    @GetMapping("/internal/list/{clubId}")
    public AjaxResult getInnerActivityList(@PathVariable Long clubId) {
        List<HActivity> activities = hActivityService.getInnerActivityList(clubId);
        return AjaxResult.success(activities);
    }
    @GetMapping("/public/list/{clubId}")
    public AjaxResult getPublicActivityList(@PathVariable Long clubId) {
        return AjaxResult.success(hActivityService.getPublicActivityList(clubId));
    }

    /**
     * 获取用户参与的活动列表
     */
    @GetMapping("/participated")
    public AjaxResult getParticipatedActivities(@RequestParam Long userId) {
        return AjaxResult.success(hActivityService.getUserParticipatedActivities(userId));
    }
}
