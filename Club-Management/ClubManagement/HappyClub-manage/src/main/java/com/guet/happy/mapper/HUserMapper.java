package com.guet.happy.mapper;

import com.guet.happy.domain.HClub;
import com.guet.happy.domain.HUser;
import org.apache.ibatis.annotations.Mapper;

import java.util.List;

@Mapper
public interface HUserMapper {
    HUser selectUserById(Integer userId);
    /**
     * 更新用户个人信息
     * @param user 用户信息对象
     * @return 影响的行数
     */
    int updateUserInfo(HUser user);
    /**
     * 根据用户ID查询其已加入的社团列表
     */
    List<HClub> getJoinedClubs(Integer userId);
}
