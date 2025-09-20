package com.guet.happy.controller;

import com.guet.common.core.domain.AjaxResult;
import com.guet.happy.domain.HUser;
import com.guet.happy.domain.HRegisterBody;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import javax.annotation.Resource;

@RestController
@RequestMapping("/happy")
public class LoginController {
    @Resource
    private com.guet.happy.service.LoginService loginService;

    @RequestMapping("/login")
    public AjaxResult login(String username, String password) {
        System.out.println("username=" + username + ", password=" + password);
        try {
            HUser user = loginService.login(username, password);
            return AjaxResult.success("登录成功", user); // 返回用户信息或其他 token
        } catch (IllegalArgumentException e) {
            return AjaxResult.error(e.getMessage());
        } catch (Exception e) {
            // 捕获其他未知异常，防止系统报错暴露给前端
            return AjaxResult.error("系统异常，请联系管理员");
        }
    }
    // 注册

    /**
     * 注册接口（支持更多字段）
     */
    @RequestMapping("/register")
    public AjaxResult register(@RequestBody HRegisterBody HRegisterBody) {
        try {
            System.out.println("注册信息: " + HRegisterBody);
            loginService.register(HRegisterBody);
            return AjaxResult.success("注册成功");
        } catch (IllegalArgumentException e) {
            return AjaxResult.error(e.getMessage());
        } catch (Exception e) {
            return AjaxResult.error("系统异常，请联系管理员");
        }
    }

}

