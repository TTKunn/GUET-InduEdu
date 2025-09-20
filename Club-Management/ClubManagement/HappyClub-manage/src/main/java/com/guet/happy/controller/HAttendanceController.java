package com.guet.happy.controller;

import com.guet.common.core.domain.AjaxResult;
import com.guet.happy.domain.HAttendance;
import com.guet.happy.domain.SignInRequest;
import com.guet.happy.service.HAttendanceService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("happy/attendance")
public class HAttendanceController {

    @Autowired
    private HAttendanceService hAttendanceService;

    @GetMapping("/club/{clubId}/user/{userId}/records")
    public AjaxResult getAttendanceByClubIdAndUserId(@PathVariable Integer clubId, @PathVariable Integer userId) {
        return AjaxResult.success(hAttendanceService.getAttendanceByClubIdAndUserId(clubId, userId));
    }
    @GetMapping("/user/{userId}")
    public AjaxResult selectAttendanceStatsByMonth(@PathVariable("userId") Long userId) {
        return AjaxResult.success(hAttendanceService.getAttendanceStatsByMonth(userId));
    }
    // 签到接口
    @PostMapping("/signin")
    public AjaxResult signIn(@RequestBody SignInRequest request) {
        Long clubId = request.getClubId();
        Long userId = request.getUserId();

        if (clubId == null || userId == null) {
            return AjaxResult.error("缺少必要参数");
        }

        int result = hAttendanceService.signIn(clubId, userId);
        return result > 0 ? AjaxResult.success("签到成功") : AjaxResult.error("签到失败");
    }

    // 获取最新未签退记录
    @GetMapping("/latest")
    public AjaxResult getLatestUncheckedInAttendance(@RequestParam Long userId) {
        HAttendance attendance = hAttendanceService.getLatestUncheckedInAttendance(userId);
        if (attendance != null) {
            return AjaxResult.success(attendance);
        } else {
            return AjaxResult.error("未找到签到记录");
        }
    }

    // 签退接口
    @PostMapping("/signout")
    public AjaxResult signOut(@RequestBody HAttendance attendance) {
        int result = hAttendanceService.signOut(attendance);
        return result > 0 ? AjaxResult.success("签退成功") : AjaxResult.error("签退失败");
    }
}
