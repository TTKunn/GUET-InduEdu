package com.guet.personal.mapper;

import com.guet.personal.domain.AchievementMember;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;

@Mapper
public interface AchievementMemberMapper {
    int insertAchievementMember(AchievementMember achievementMember);
    // 批量插入成果与成员的绑定关系
    // int batchInsertAchievementMember(List<AchievementMember> achievementMembers);

    /**
     * 批量插入成果参与成员
     * @param achievementId 成果ID
     * @param memberIds 成员ID列表
     * @return 插入条数
     */
    int batchInsertAchievementMember(
            @Param("achievementId") Long achievementId,
            @Param("memberIds") List<Long> memberIds
    );
}