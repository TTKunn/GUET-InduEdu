package com.guet.personal.service;

import java.util.List;

import com.guet.personal.domain.Dto.MembershipDto;
import com.guet.personal.domain.Membership;
import com.guet.personal.domain.Vo.MemberAchievementsVo;
import com.guet.personal.domain.Vo.MemberActivitiesVo;
import com.guet.personal.domain.Vo.MembershipVo;

/**
 * 社团成员关系Service接口
 * 
 * @author kevin
 * @date 2025-05-05
 */
public interface IMembershipService 
{
    /**
     * 查询社团成员关系
     * 
     * @param membershipId 社团成员关系主键
     * @return 社团成员关系
     */
    public Membership selectMembershipByMembershipId(Long membershipId);

    /**
     * 查询社团成员关系列表
     * 
     * @param membership 社团成员关系
     * @return 社团成员关系集合
     */
    public List<Membership> selectMembershipList(MembershipDto membership);

    /**
     * 新增社团成员关系
     * 
     * @param membership 社团成员关系
     * @return 结果
     */
    public int insertMembership(Membership membership);

    /**
     * 修改社团成员关系
     * 
     * @param membership 社团成员关系
     * @return 结果
     */
    public int updateMembership(Membership membership);

    /**
     * 批量删除社团成员关系
     * 
     * @param membershipIds 需要删除的社团成员关系主键集合
     * @return 结果
     */
    public int deleteMembershipByMembershipIds(Long[] membershipIds);

    /**
     * 删除社团成员关系信息
     * 
     * @param membershipId 社团成员关系主键
     * @return 结果
     */
    public int deleteMembershipByMembershipId(Long membershipId);

    /**
     * 查询社团成员列表
     *
     * @param clubId 社团ID
     * @return 社团成员集合
     */
    public List<MembershipVo> selectMembersByClubId(Long clubId);

    List<MemberAchievementsVo> listAchievementsByMemberId(Long memberId);

    List<MemberActivitiesVo> listActivitiesByMemberId(Long memberId);
}
