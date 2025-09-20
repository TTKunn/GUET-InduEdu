package com.guet.happy.service;

import com.guet.happy.domain.HUser;
import com.guet.happy.domain.HRegisterBody;

public interface LoginService {
    // 登录
    HUser login(String username, String password);

void register(HRegisterBody HRegisterBody);

}
