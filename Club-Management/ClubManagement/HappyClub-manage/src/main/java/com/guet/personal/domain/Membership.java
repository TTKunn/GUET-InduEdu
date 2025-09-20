package com.guet.personal.domain;

import java.util.Date;
import com.fasterxml.jackson.annotation.JsonFormat;
import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import com.guet.common.annotation.Excel;
import com.guet.common.core.domain.BaseEntity;

/**
 * 社团成员关系对象 tb_membership
 * 
 * @author kevin
 * @date 2025-05-05
 */
public class Membership extends BaseEntity
{
    private static final long serialVersionUID = 1L;

    /** 成员关系ID */
    private Long membershipId;

    /** 用户ID */
    @Excel(name = "用户ID")
    private Long userId;

    /** 社团ID */
    @Excel(name = "社团ID")
    private Long clubId;

    /** 加入时间 */
    @JsonFormat(pattern = "yyyy-MM-dd")
    @Excel(name = "加入时间", width = 30, dateFormat = "yyyy-MM-dd")
    private Date joinTime;

    /** 状态 */
    @Excel(name = "状态")
    private String status;

    /** 退出时间 */
    @JsonFormat(pattern = "yyyy-MM-dd")
    @Excel(name = "退出时间", width = 30, dateFormat = "yyyy-MM-dd")
    private Date exitTime;

    /** 软删除时间 */
    private Date deletedAt;

    /** 累计学习时长（分钟） */
    @Excel(name = "累计学习时长", readConverterExp = "分=钟")
    private String totalStudyDuration;

    public void setMembershipId(Long membershipId) 
    {
        this.membershipId = membershipId;
    }

    public Long getMembershipId() 
    {
        return membershipId;
    }

    public void setUserId(Long userId) 
    {
        this.userId = userId;
    }

    public Long getUserId() 
    {
        return userId;
    }

    public void setClubId(Long clubId) 
    {
        this.clubId = clubId;
    }

    public Long getClubId() 
    {
        return clubId;
    }

    public void setJoinTime(Date joinTime) 
    {
        this.joinTime = joinTime;
    }

    public Date getJoinTime() 
    {
        return joinTime;
    }

    public void setStatus(String status) 
    {
        this.status = status;
    }

    public String getStatus() 
    {
        return status;
    }

    public void setExitTime(Date exitTime) 
    {
        this.exitTime = exitTime;
    }

    public Date getExitTime() 
    {
        return exitTime;
    }

    public void setDeletedAt(Date deletedAt) 
    {
        this.deletedAt = deletedAt;
    }

    public Date getDeletedAt() 
    {
        return deletedAt;
    }

    public void setTotalStudyDuration(String totalStudyDuration) 
    {
        this.totalStudyDuration = totalStudyDuration;
    }

    public String getTotalStudyDuration() 
    {
        return totalStudyDuration;
    }

    @Override
    public String toString() {
        return new ToStringBuilder(this,ToStringStyle.MULTI_LINE_STYLE)
            .append("membershipId", getMembershipId())
            .append("userId", getUserId())
            .append("clubId", getClubId())
            .append("joinTime", getJoinTime())
            .append("status", getStatus())
            .append("exitTime", getExitTime())
            .append("deletedAt", getDeletedAt())
            .append("totalStudyDuration", getTotalStudyDuration())
            .toString();
    }
}
