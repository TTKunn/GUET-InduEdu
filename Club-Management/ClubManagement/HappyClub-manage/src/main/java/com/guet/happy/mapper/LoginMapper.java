package com.guet.happy.mapper;

import com.guet.happy.domain.HUser;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

@Mapper
public interface LoginMapper {
    // login
    HUser login(@Param("username") String userName, @Param("password") String password);

    HUser selectUserByUsername(String username);

    void insertUser(HUser user);

    HUser selectByUsername(String username);
}
