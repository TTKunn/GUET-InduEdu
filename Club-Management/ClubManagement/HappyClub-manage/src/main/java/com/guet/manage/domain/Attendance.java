package com.guet.manage.domain;

import java.util.Date;
import com.fasterxml.jackson.annotation.JsonFormat;
import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import com.guet.common.annotation.Excel;
import com.guet.common.core.domain.BaseEntity;

/**
 * 考勤管理对象 tb_attendance
 * 
 * @author kevin
 * @date 2025-04-30
 */
public class Attendance extends BaseEntity
{
    private static final long serialVersionUID = 1L;

    /** 考勤ID */
    private Long attendanceId;

    /** 所属社团ID */
    @Excel(name = "所属社团ID")
    private Long clubId;

    /** 成员ID */
    @Excel(name = "成员ID")
    private Long userId;

    /** 签到时间 */
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    @Excel(name = "签到时间", width = 30, dateFormat = "yyyy-MM-dd HH:mm:ss")
    private Date clockInTime;

    /** 签退时间 */
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    @Excel(name = "签退时间", width = 30, dateFormat = "yyyy-MM-dd HH:mm:ss")
    private Date clockOutTime;



    /** 学习时长（分钟） */
    @Excel(name = "学习时长", readConverterExp = "分=钟")
    private Long studyDuration;

    /** 考勤状态 */
    @Excel(name = "考勤状态")
    private String status;

    /** 备注 */
    @Excel(name = "备注")
    private String notes;

    /** 创建时间 */
    private Date createdAt;

    /** 更新时间 */
    private Date updatedAt;

    /** 软删除时间 */
    private Date deletedAt;

    public void setAttendanceId(Long attendanceId) 
    {
        this.attendanceId = attendanceId;
    }

    public Long getAttendanceId() 
    {
        return attendanceId;
    }

    public void setClubId(Long clubId) 
    {
        this.clubId = clubId;
    }

    public Long getClubId() 
    {
        return clubId;
    }

    public void setUserId(Long userId) 
    {
        this.userId = userId;
    }

    public Long getUserId() 
    {
        return userId;
    }

    public void setClockInTime(Date clockInTime) 
    {
        this.clockInTime = clockInTime;
    }

    public Date getClockInTime() 
    {
        return clockInTime;
    }

    public void setClockOutTime(Date clockOutTime) 
    {
        this.clockOutTime = clockOutTime;
    }

    public Date getClockOutTime() 
    {
        return clockOutTime;
    }

    public void setStudyDuration(Long studyDuration) 
    {
        this.studyDuration = studyDuration;
    }

    public Long getStudyDuration() 
    {
        return studyDuration;
    }

    public void setStatus(String status) 
    {
        this.status = status;
    }

    public String getStatus() 
    {
        return status;
    }

    public void setNotes(String notes) 
    {
        this.notes = notes;
    }

    public String getNotes() 
    {
        return notes;
    }

    public void setCreatedAt(Date createdAt) 
    {
        this.createdAt = createdAt;
    }

    public Date getCreatedAt() 
    {
        return createdAt;
    }

    public void setUpdatedAt(Date updatedAt) 
    {
        this.updatedAt = updatedAt;
    }

    public Date getUpdatedAt() 
    {
        return updatedAt;
    }

    public void setDeletedAt(Date deletedAt) 
    {
        this.deletedAt = deletedAt;
    }

    public Date getDeletedAt() 
    {
        return deletedAt;
    }

    @Override
    public String toString() {
        return new ToStringBuilder(this,ToStringStyle.MULTI_LINE_STYLE)
            .append("attendanceId", getAttendanceId())
            .append("clubId", getClubId())
            .append("userId", getUserId())
            .append("clockInTime", getClockInTime())
            .append("clockOutTime", getClockOutTime())
            .append("studyDuration", getStudyDuration())
            .append("status", getStatus())
            .append("notes", getNotes())
            .append("createdAt", getCreatedAt())
            .append("updatedAt", getUpdatedAt())
            .append("deletedAt", getDeletedAt())
            .toString();
    }
}
