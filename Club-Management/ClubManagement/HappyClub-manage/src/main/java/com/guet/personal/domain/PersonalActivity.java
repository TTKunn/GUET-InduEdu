package com.guet.personal.domain;

import java.util.Date;
import com.fasterxml.jackson.annotation.JsonFormat;
import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import com.guet.common.annotation.Excel;
import com.guet.common.core.domain.BaseEntity;

/**
 * 活动管理对象 tb_activity
 * 
 * @author kevin
 * @date 2025-05-01
 */
public class PersonalActivity extends BaseEntity
{
    private static final long serialVersionUID = 1L;

    /** 活动ID */
    private Long activityId;

    /** 社团ID */
    private Long clubId;

    /** 活动名称 */
    @Excel(name = "活动名称")
    private String name;

    /** 活动描述 */
    @Excel(name = "活动描述")
    private String description;

    /** 开始时间 */
    /** 开始时间 */
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")  // 添加时分秒
    @Excel(name = "开始时间", width = 30, dateFormat = "yyyy-MM-dd HH:mm:ss")  // 添加时分秒
    private Date startTime;

    /** 结束时间 */
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")  // 添加时分秒
    @Excel(name = "结束时间", width = 30, dateFormat = "yyyy-MM-dd HH:mm:ss")  // 添加时分秒
    private Date endTime;

    /** 活动地点 */
    @Excel(name = "活动地点")
    private String location;

    /** 负责人ID */
    @Excel(name = "负责人ID")
    private Long organizerId;

    /** 可见类型: 公开/内部/自定义社团 */
    @Excel(name = "可见类型: 公开/内部/自定义社团")
    private String visibility;

    /** 活动审批状态 */
    @Excel(name = "活动审批状态")
    private String status;

    /** 软删除时间 */
    private Date deletedAt;

    public void setActivityId(Long activityId) 
    {
        this.activityId = activityId;
    }

    public Long getActivityId() 
    {
        return activityId;
    }

    public void setClubId(Long clubId) 
    {
        this.clubId = clubId;
    }

    public Long getClubId() 
    {
        return clubId;
    }

    public void setName(String name) 
    {
        this.name = name;
    }

    public String getName() 
    {
        return name;
    }

    public void setDescription(String description) 
    {
        this.description = description;
    }

    public String getDescription() 
    {
        return description;
    }

    public void setStartTime(Date startTime) 
    {
        this.startTime = startTime;
    }

    public Date getStartTime() 
    {
        return startTime;
    }

    public void setEndTime(Date endTime) 
    {
        this.endTime = endTime;
    }

    public Date getEndTime() 
    {
        return endTime;
    }

    public void setLocation(String location) 
    {
        this.location = location;
    }

    public String getLocation() 
    {
        return location;
    }

    public void setOrganizerId(Long organizerId) 
    {
        this.organizerId = organizerId;
    }

    public Long getOrganizerId() 
    {
        return organizerId;
    }

    public void setVisibility(String visibility) 
    {
        this.visibility = visibility;
    }

    public String getVisibility() 
    {
        return visibility;
    }

    public void setStatus(String status) 
    {
        this.status = status;
    }

    public String getStatus() 
    {
        return status;
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
            .append("activityId", getActivityId())
            .append("clubId", getClubId())
            .append("name", getName())
            .append("description", getDescription())
            .append("startTime", getStartTime())
            .append("endTime", getEndTime())
            .append("location", getLocation())
            .append("organizerId", getOrganizerId())
            .append("visibility", getVisibility())
            .append("status", getStatus())
            .append("deletedAt", getDeletedAt())
            .toString();
    }
}
