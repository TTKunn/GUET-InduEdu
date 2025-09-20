package com.guet.happy.domain;
import java.util.Date;

public class HMember {

    private Integer membershipId;
    private Integer userId;
    private Integer clubId;
    private Date joinTime;
    private String status; // Assuming enum is represented as String for simplicity
    private Date exitTime;
    private Date deletedAt;
    private Long totalStudyDuration;
    private Integer activityParticipation;
    private Integer achievementCount;

    // Getters and Setters

    public Integer getMembershipId() {
        return membershipId;
    }

    public void setMembershipId(Integer membershipId) {
        this.membershipId = membershipId;
    }

    public Integer getUserId() {
        return userId;
    }

    public void setUserId(Integer userId) {
        this.userId = userId;
    }

    public Integer getClubId() {
        return clubId;
    }

    public void setClubId(Integer clubId) {
        this.clubId = clubId;
    }

    public Date getJoinTime() {
        return joinTime;
    }

    public void setJoinTime(Date joinTime) {
        this.joinTime = joinTime;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public Date getExitTime() {
        return exitTime;
    }

    public void setExitTime(Date exitTime) {
        this.exitTime = exitTime;
    }

    public Date getDeletedAt() {
        return deletedAt;
    }

    public void setDeletedAt(Date deletedAt) {
        this.deletedAt = deletedAt;
    }

    public Long getTotalStudyDuration() {
        return totalStudyDuration;
    }

    public void setTotalStudyDuration(Long totalStudyDuration) {
        this.totalStudyDuration = totalStudyDuration;
    }

    public Integer getActivityParticipation() {
        return activityParticipation;
    }

    public void setActivityParticipation(Integer activityParticipation) {
        this.activityParticipation = activityParticipation;
    }

    public Integer getAchievementCount() {
        return achievementCount;
    }

    public void setAchievementCount(Integer achievementCount) {
        this.achievementCount = achievementCount;
    }

    // toString method for easy debugging
    @Override
    public String toString() {
        return "HMember{" +
                "membershipId=" + membershipId +
                ", userId=" + userId +
                ", clubId=" + clubId +
                ", joinTime=" + joinTime +
                ", status='" + status + '\'' +
                ", exitTime=" + exitTime +
                ", deletedAt=" + deletedAt +
                ", totalStudyDuration=" + totalStudyDuration +
                ", activityParticipation=" + activityParticipation +
                ", achievementCount=" + achievementCount +
                '}';
    }
}
