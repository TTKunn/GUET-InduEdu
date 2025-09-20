package com.guet.happy.mapper;

import com.guet.happy.domain.HMember;
import org.apache.ibatis.annotations.Param;

import java.util.List;

public interface HMemberMapper {

    /**
     * 根据用户ID查询成员信息
     */
    HMember selectMemberByUserId(Integer userId);

    /**
     * 根据社团ID查询所有成员
     */
    List<HMember> selectMembersByClubId(Integer clubId);

    /**
     * 判断用户是否是该社团的成员
     */
    int checkMember(@Param("userId") Integer userId,@Param("clubId") Integer clubId);

    // exitClub
    int exitClub(@Param("userId") Integer userId, @Param("clubId") Integer clubId);
    // joinClub
    int joinClub(@Param("userId") Integer userId, @Param("clubId") Integer clubId);

    /**
 * 插入入社申请记录
 */
void insertJoinApplication(@Param("userId") Integer userId,
                           @Param("clubId") Integer clubId,
                           @Param("remark") String remark);

/**
 * 插入退社申请记录
 */
void insertQuitApplication(@Param("userId") Integer userId,
                           @Param("clubId") Integer clubId,
                           @Param("remark") String remark);

}
