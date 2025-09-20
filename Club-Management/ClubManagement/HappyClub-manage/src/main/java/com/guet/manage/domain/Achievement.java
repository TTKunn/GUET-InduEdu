package com.guet.manage.domain;

import java.util.Date;
import com.fasterxml.jackson.annotation.JsonFormat;
import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import com.guet.common.annotation.Excel;
import com.guet.common.core.domain.BaseEntity;

/**
 * 成果管理对象 tb_achievement
 * 
 * @author kevin
 * @date 2025-04-30
 */
public class Achievement extends BaseEntity
{
    private static final long serialVersionUID = 1L;

    /** 成果ID */
    private Long achievementId;

    /** 社团ID */
    @Excel(name = "社团ID")
    private Long clubId;

    /** 发布人ID */
    @Excel(name = "发布人ID")
    private Long publisherId;

    /** 成果标题 */
    @Excel(name = "成果标题")
    private String title;

    /** 成果类型 */
    @Excel(name = "成果类型")
    private String type;

    /** 详细描述 */
    @Excel(name = "详细描述")
    private String description;

    /** 获得日期 */
    @JsonFormat(pattern = "yyyy-MM-dd")
    @Excel(name = "获得日期", width = 30, dateFormat = "yyyy-MM-dd")
    private Date achieveDate;

    /** 证书地址 */
    @Excel(name = "证书地址")
    private String certificateUrl;

    /** 成果审批状态 */
    @Excel(name = "成果审批状态")
    private String status;

    /** 创建时间 */
    private Date createdAt;

    /** 软删除时间 */
    private Date deletedAt;

    public void setAchievementId(Long achievementId) 
    {
        this.achievementId = achievementId;
    }

    public Long getAchievementId() 
    {
        return achievementId;
    }

    public void setClubId(Long clubId) 
    {
        this.clubId = clubId;
    }

    public Long getClubId() 
    {
        return clubId;
    }

    public void setPublisherId(Long publisherId) 
    {
        this.publisherId = publisherId;
    }

    public Long getPublisherId() 
    {
        return publisherId;
    }

    public void setTitle(String title) 
    {
        this.title = title;
    }

    public String getTitle() 
    {
        return title;
    }

    public void setType(String type) 
    {
        this.type = type;
    }

    public String getType() 
    {
        return type;
    }

    public void setDescription(String description) 
    {
        this.description = description;
    }

    public String getDescription() 
    {
        return description;
    }

    public void setAchieveDate(Date achieveDate) 
    {
        this.achieveDate = achieveDate;
    }

    public Date getAchieveDate() 
    {
        return achieveDate;
    }

    public void setCertificateUrl(String certificateUrl) 
    {
        this.certificateUrl = certificateUrl;
    }

    public String getCertificateUrl() 
    {
        return certificateUrl;
    }

    public void setStatus(String status) 
    {
        this.status = status;
    }

    public String getStatus() 
    {
        return status;
    }

    public void setCreatedAt(Date createdAt) 
    {
        this.createdAt = createdAt;
    }

    public Date getCreatedAt() 
    {
        return createdAt;
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
            .append("achievementId", getAchievementId())
            .append("clubId", getClubId())
            .append("publisherId", getPublisherId())
            .append("title", getTitle())
            .append("type", getType())
            .append("description", getDescription())
            .append("achieveDate", getAchieveDate())
            .append("certificateUrl", getCertificateUrl())
            .append("status", getStatus())
            .append("createdAt", getCreatedAt())
            .append("deletedAt", getDeletedAt())
            .toString();
    }
}
