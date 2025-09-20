package com.guet.manage.mapper;

import com.guet.manage.domain.dto.*;
import com.guet.manage.domain.vo.AchievementAuditVo;
import com.guet.manage.domain.vo.ActivityAuditVo;
import com.guet.manage.domain.vo.AnnouncementAuditVo;
import com.guet.manage.domain.vo.NewClubAuditVo;
import org.apache.ibatis.annotations.Mapper;

import java.util.List;

@Mapper
public interface AuditMapper {
    public List<AnnouncementAuditVo> selectAuditAnnouncements(AnnouncementAuditQueryDto auditAnnouncement);
    // 审核通过
    public int approveAnnouncement(AuditDecisionRequest auditDecisionRequest);
    public int approveAuditAnnouncement(AuditDecisionRequest auditDecisionRequest);
    // 审核拒绝
    public int rejectAnnouncement(AuditDecisionRequest auditDecisionRequest);
    // 更新公告状态
    public int rejectAuditAnnouncement(AuditDecisionRequest auditDecisionRequest);
    // 活动审核

    List<ActivityAuditVo> selectAuditActivities(ActivityAuditQueryDto auditActivityDto);

    int approveActivity(AuditDecisionRequest auditDecisionRequest);

    int approveAuditActivity(AuditDecisionRequest auditDecisionRequest);

    int rejectActivity(AuditDecisionRequest auditDecisionRequest);
    int rejectAuditActivity(AuditDecisionRequest auditDecisionRequest);
    // 新社团审核
    List<NewClubAuditVo> selectAuditNewClub(NewClubAuditDto auditClubDto);
    int approveNewClub(AuditDecisionRequest auditDecisionRequest);
    int approveAuditNewClub(AuditDecisionRequest auditDecisionRequest);
    int rejectNewClub(AuditDecisionRequest auditDecisionRequest);
    int rejectAuditNewClub(AuditDecisionRequest auditDecisionRequest);
    // 社团成就审核
    List<AchievementAuditVo> selectAuditAchievements(AchievementAuditQueryDto queryDto);
    int approveAuditAchievement(AuditDecisionRequest request);
    int approveAchievement(AuditDecisionRequest request);
    int rejectAuditAchievement(AuditDecisionRequest request);
    int rejectAchievement(AuditDecisionRequest request);
}
