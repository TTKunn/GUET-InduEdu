package com.guet.manage.service;

import com.guet.manage.domain.dto.*;
import com.guet.manage.domain.vo.AchievementAuditVo;
import com.guet.manage.domain.vo.ActivityAuditVo;
import com.guet.manage.domain.vo.AnnouncementAuditVo;
import com.guet.manage.domain.vo.NewClubAuditVo;

import java.util.List;

public interface AuditService {
    public List<AnnouncementAuditVo> selectAuditAnnouncements(AnnouncementAuditQueryDto auditAnnouncement);

    int approveAnnouncement(AuditDecisionRequest auditDecisionRequest);

    int rejectAnnouncement(AuditDecisionRequest auditDecisionRequest);

    /**
     * 查询活动审核列表
     * @param auditActivity 查询条件
     * @return 审核列表
     */
    List<ActivityAuditVo> selectAuditActivities(ActivityAuditQueryDto auditActivityDto);

    /**
     * 审核通过活动
     * @param auditDecisionRequest 审核请求参数
     * @return 影响行数
     */
    int approveActivity(AuditDecisionRequest auditDecisionRequest);

    /**
     * 审核拒绝活动
     * @param auditDecisionRequest 审核请求参数
     * @return 影响行数
     */
    int rejectActivity(AuditDecisionRequest auditDecisionRequest);
    List<NewClubAuditVo> selectAuditNewClub(NewClubAuditDto auditClubDto);
    int approveNewClub(AuditDecisionRequest auditDecisionRequest);
    int rejectNewClub(AuditDecisionRequest auditDecisionRequest);

    List<AchievementAuditVo> selectAuditAchievements(AchievementAuditQueryDto queryDto);
    int approveAchievement(AuditDecisionRequest request);
    int rejectAchievement(AuditDecisionRequest request);
}
