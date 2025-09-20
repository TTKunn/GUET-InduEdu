package com.guet.manage.service.impl;

import com.guet.manage.domain.dto.*;
import com.guet.manage.domain.vo.AchievementAuditVo;
import com.guet.manage.domain.vo.ActivityAuditVo;
import com.guet.manage.domain.vo.AnnouncementAuditVo;
import com.guet.manage.domain.vo.NewClubAuditVo;
import com.guet.manage.mapper.AuditMapper;
import com.guet.manage.service.AuditService;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import javax.annotation.Resource;
import java.util.List;

@Service
public class AuditServiceImpl implements AuditService {
    @Resource
    private AuditMapper auditMapper;
    @Override
    public List<AnnouncementAuditVo> selectAuditAnnouncements(AnnouncementAuditQueryDto auditAnnouncement) {
        return auditMapper.selectAuditAnnouncements(auditAnnouncement);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public int approveAnnouncement(AuditDecisionRequest auditDecisionRequest) {
        // 审核通过，更新公告状态
        auditMapper.approveAuditAnnouncement(auditDecisionRequest);
        // 更新审核记录
        return auditMapper.approveAnnouncement(auditDecisionRequest);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public int rejectAnnouncement(AuditDecisionRequest auditDecisionRequest) {
        // 审核拒绝，更新公告状态
        auditMapper.rejectAuditAnnouncement(auditDecisionRequest);
        // 更新审核记录
        return auditMapper.rejectAnnouncement(auditDecisionRequest);
    }

    @Override
    public List<ActivityAuditVo> selectAuditActivities(ActivityAuditQueryDto auditActivityDto) {
        return auditMapper.selectAuditActivities(auditActivityDto);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public int approveActivity(AuditDecisionRequest auditDecisionRequest) {
        auditMapper.approveAuditActivity(auditDecisionRequest);
        return auditMapper.approveActivity(auditDecisionRequest);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public int rejectActivity(AuditDecisionRequest auditDecisionRequest) {
        auditMapper.rejectAuditActivity(auditDecisionRequest);
        return auditMapper.rejectActivity(auditDecisionRequest);
    }
    // 新社团审核
    @Override
    public List<NewClubAuditVo> selectAuditNewClub(NewClubAuditDto auditClubDto) {
        return auditMapper.selectAuditNewClub(auditClubDto);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public int approveNewClub(AuditDecisionRequest auditDecisionRequest) {
        auditMapper.approveAuditNewClub(auditDecisionRequest);
        return auditMapper.approveNewClub(auditDecisionRequest);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public int rejectNewClub(AuditDecisionRequest auditDecisionRequest) {
        auditMapper.rejectAuditNewClub(auditDecisionRequest);
        return auditMapper.rejectNewClub(auditDecisionRequest);
    }

    @Override
    public List<AchievementAuditVo> selectAuditAchievements(AchievementAuditQueryDto queryDto) {
        return auditMapper.selectAuditAchievements(queryDto);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public int approveAchievement(AuditDecisionRequest request) {
        // 审核通过，更新成果状态
        auditMapper.approveAuditAchievement(request);
        // 更新审核记录
        return auditMapper.approveAchievement(request);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public int rejectAchievement(AuditDecisionRequest request) {
        // 审核拒绝，更新成果状态
        auditMapper.rejectAuditAchievement(request);
        // 更新审核记录
        return auditMapper.rejectAchievement(request);
    }
}
