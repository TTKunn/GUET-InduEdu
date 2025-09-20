package com.guet.happy.service.Impl;

import com.guet.happy.domain.HUser;
import com.guet.happy.domain.HRegisterBody;
import com.guet.happy.mapper.LoginMapper;
import com.guet.happy.service.LoginService;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;

@Service
public class LoginServiceImpl implements LoginService {
    @Resource
    private LoginMapper loginMapper;

    @Override
    public HUser login(String username, String password) {
        System.out.println(username+password);
        // 1. 非空校验
        if (username == null || username.isEmpty() || password == null || password.isEmpty()) {
            throw new IllegalArgumentException("用户名或密码不能为空");
        }

        // 2. 查询用户信息
        HUser user = loginMapper.login(username, password);
        System.out.println("user = " + user + password);
        // 3. 用户是否存在
        if (user == null) {
            throw new IllegalArgumentException("用户名或密码错误");
        }

        // 4. 移除 BCrypt 校验密码，直接比对明文密码
        if (!password.equals(user.getPassword())) {
            throw new IllegalArgumentException("用户名或密码错误");
        }
        user.setPassword(null);
        // 5. 返回用户信息
        return user;

    }

@Override
public void register(HRegisterBody HRegisterBody) {
    // 检查用户名是否已存在
    HUser existingUser = loginMapper.selectByUsername(HRegisterBody.getUsername());
    if (existingUser != null) {
        throw new IllegalArgumentException("用户名已存在");
    }

    HUser user = new HUser();
    user.setUsername(HRegisterBody.getUsername());
    user.setPassword(HRegisterBody.getPassword()); // 建议加密存储
    user.setNickName(HRegisterBody.getName());
    user.setDeptId(HRegisterBody.getDeptId());
    user.setSex(HRegisterBody.getGender());
    user.setAvatar(""); // 默认头像或可选上传

    loginMapper.insertUser(user); // 插入用户
}

}