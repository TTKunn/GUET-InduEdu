package com.guet.personal.service.impl.Membership;

import java.util.List;

import com.guet.personal.domain.Dto.MembershipDto;
import com.guet.personal.domain.Vo.MemberAchievementsVo;
import com.guet.personal.domain.Vo.MemberActivitiesVo;
import com.guet.personal.domain.Vo.MembershipVo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.guet.personal.mapper.MembershipMapper;
import com.guet.personal.domain.Membership;
import com.guet.personal.service.IMembershipService;

import javax.annotation.Resource;

/**
 * 社团成员关系Service业务层处理
 * 
 * @author kevin
 * @date 2025-05-05
 */
@Service
public class MembershipServiceImpl implements IMembershipService 
{
    @Resource
    private MembershipMapper membershipMapper;

    /**
     * 查询社团成员关系
     * 
     * @param membershipId 社团成员关系主键
     * @return 社团成员关系
     */
    @Override
    public Membership selectMembershipByMembershipId(Long membershipId)
    {
        return membershipMapper.selectMembershipByMembershipId(membershipId);
    }

    /**
     * 查询社团成员关系列表
     * 
     * @param membership 社团成员关系
     * @return 社团成员关系
     */
    @Override
    public List<Membership> selectMembershipList(MembershipDto membership)
    {
        return membershipMapper.selectMembershipList(membership);
    }

    /**
     * 新增社团成员关系
     * 
     * @param membership 社团成员关系
     * @return 结果
     */
    @Override
    public int insertMembership(Membership membership)
    {
        return membershipMapper.insertMembership(membership);
    }

    /**
     * 修改社团成员关系
     * 
     * @param membership 社团成员关系
     * @return 结果
     */
    @Override
    public int updateMembership(Membership membership)
    {
        return membershipMapper.updateMembership(membership);
    }

    /**
     * 批量删除社团成员关系
     * 
     * @param membershipIds 需要删除的社团成员关系主键
     * @return 结果
     */
    @Override
    public int deleteMembershipByMembershipIds(Long[] membershipIds)
    {
        return membershipMapper.deleteMembershipByMembershipIds(membershipIds);
    }

    /**
     * 删除社团成员关系信息
     * 
     * @param membershipId 社团成员关系主键
     * @return 结果
     */
    @Override
    public int deleteMembershipByMembershipId(Long membershipId)
    {
        return membershipMapper.deleteMembershipByMembershipId(membershipId);
    }

    @Override
    public List<MembershipVo> selectMembersByClubId(Long clubId) {
        return membershipMapper.selectMembersByClubId(clubId);
    }

    @Override
    public List<MemberAchievementsVo> listAchievementsByMemberId(Long memberId) {
        return membershipMapper.listAchievementsByMemberId(memberId);
    }

    @Override
    public List<MemberActivitiesVo> listActivitiesByMemberId(Long memberId) {
        return membershipMapper.listActivitiesByMemberId(memberId);
    }
}
