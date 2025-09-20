package com.guet.happy.controller;

import com.guet.common.core.domain.AjaxResult;
import com.guet.happy.domain.HAchievement;
import com.guet.happy.service.HAchievementService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("happy/achievements")
public class HAchievementController {

    @Autowired
    private HAchievementService hAchievementService;

    @GetMapping("/list/{clubId}")
    public AjaxResult getAchievementsByClubId(@PathVariable Integer clubId) {
        return AjaxResult.success(hAchievementService.getAchievementsByClubId(clubId));
    }
    // GET /achievements/1
    @GetMapping("detail/{achievementId}")
    public AjaxResult getAchievementById(@PathVariable Integer achievementId) {
        return AjaxResult.success(hAchievementService.getAchievementById(achievementId));
    }
}
