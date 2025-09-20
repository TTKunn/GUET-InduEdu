package com.guet.manage.domain;

import java.util.Date;
import com.fasterxml.jackson.annotation.JsonFormat;
import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import com.guet.common.annotation.Excel;
import com.guet.common.core.domain.BaseEntity;

/**
 * 公告管理对象 tb_announcement
 * 
 * @author kevin
 * @date 2025-04-30
 */
public class Announcement extends BaseEntity
{
    private static final long serialVersionUID = 1L;

    /** 公告ID */
    private Long announcementId;

    /** 公告标题 */
    @Excel(name = "公告标题")
    private String title;

    /** 公告内容 */
    @Excel(name = "公告内容")
    private String content;

    /** 发布人ID */
    @Excel(name = "发布人ID")
    private Long publisherId;

    /** 公告类型 */
    private String type;

    /** 公告状态 */
    @Excel(name = "公告状态")
    private String status;

    /** 发布时间 */
    @JsonFormat(pattern = "yyyy-MM-dd")
    @Excel(name = "发布时间", width = 30, dateFormat = "yyyy-MM-dd")
    private Date createdAt;

    /** 软删除时间 */
    private Date deletedAt;

    public void setAnnouncementId(Long announcementId) 
    {
        this.announcementId = announcementId;
    }

    public Long getAnnouncementId() 
    {
        return announcementId;
    }

    public void setTitle(String title) 
    {
        this.title = title;
    }

    public String getTitle() 
    {
        return title;
    }

    public void setContent(String content) 
    {
        this.content = content;
    }

    public String getContent() 
    {
        return content;
    }

    public void setPublisherId(Long publisherId) 
    {
        this.publisherId = publisherId;
    }

    public Long getPublisherId() 
    {
        return publisherId;
    }

    public void setType(String type) 
    {
        this.type = type;
    }

    public String getType() 
    {
        return type;
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
            .append("announcementId", getAnnouncementId())
            .append("title", getTitle())
            .append("content", getContent())
            .append("publisherId", getPublisherId())
            .append("type", getType())
            .append("status", getStatus())
            .append("createdAt", getCreatedAt())
            .append("deletedAt", getDeletedAt())
            .toString();
    }
}
