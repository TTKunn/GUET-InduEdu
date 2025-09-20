package com.guet.happy.controller;

import com.guet.common.core.domain.AjaxResult;
import com.guet.happy.domain.HClub;
import com.guet.happy.domain.HUser;
import com.guet.happy.service.HUserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/happy")
public class HUserController {

    @Autowired
    private HUserService userService;

    /**
     * 获取用户详细信息（包含部门）
     * 示例请求：GET /happy/user/detail/1
     */
    @GetMapping("/user/detail/{userId}")
    public AjaxResult getUserDetail(@PathVariable("userId") Integer userId) {
        return AjaxResult.success(userService.getUserById(userId));
    }

    @PostMapping("/user/update")
    public AjaxResult updateUserInfo(@RequestBody HUser user) {
        int result = userService.updateUserInfo(user);
        if (result > 0) {
            return AjaxResult.success("个人信息更新成功");
        } else {
            return AjaxResult.error("个人信息更新失败");
        }
    }
    /**
     * 获取用户已加入的社团列表
     */
    @GetMapping("/clubs/{userId}")
    public AjaxResult getJoinedClubs(@PathVariable Integer userId) {
        List<HClub> clubs = userService.getJoinedClubs(userId);
        return AjaxResult.success(clubs);
    }
}
