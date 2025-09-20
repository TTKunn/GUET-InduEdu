// 修改第1行的包名为 Impl（首字母大写）
package com.guet.happy.service.Impl;

import com.guet.happy.domain.HMember;
import com.guet.happy.mapper.HMemberMapper;
import com.guet.happy.service.HMemberService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
public class HMemberServiceImpl implements HMemberService {

    @Autowired
    private HMemberMapper hMemberMapper;

    @Override
    public HMember getMemberByUserId(Integer userId) {
        return hMemberMapper.selectMemberByUserId(userId);
    }

    @Override
    public List<HMember> getMembersByClubId(Integer clubId) {
        return hMemberMapper.selectMembersByClubId(clubId);
    }

    @Override
    public boolean isMember(Integer userId, Integer clubId) {
        return hMemberMapper.checkMember(userId, clubId) > 0;
    }

    @Override
    @Transactional
    public boolean quitClub(Integer userId, Integer clubId, String remark) {
        // 更新 tb_membership 状态为 quit
        int rows = hMemberMapper.exitClub(userId, clubId);

        // 插入退社申请记录
        hMemberMapper.insertQuitApplication(userId, clubId, remark);

        return rows > 0;
    }

    @Override
    @Transactional
    public boolean joinClub(Integer userId, Integer clubId, String remark) {
        // 先检查是否已经是该社团成员
        if (hMemberMapper.checkMember(userId, clubId) > 0) {
            System.out.println(hMemberMapper.checkMember(userId, clubId));
            throw new RuntimeException("该用户已加入该社团");
        }

        // 插入入社申请
        hMemberMapper.insertJoinApplication(userId, clubId, remark);

        // 插入 membership 记录
        return hMemberMapper.joinClub(userId, clubId) > 0;
    }
}
