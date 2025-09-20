package com.guet.personal.domain;

import java.util.Date;
import com.fasterxml.jackson.annotation.JsonFormat;
import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import com.guet.common.annotation.Excel;
import com.guet.common.core.domain.BaseEntity;

/**
 * 社团信息对象 tb_club
 * 
 * @author kevin
 * @date 2025-05-05
 */
public class PClub extends BaseEntity
{
    private static final long serialVersionUID = 1L;

    /** 社团ID */
    private Long clubId;

    /** 社团名称 */
    @Excel(name = "社团名称")
    private String name;

    /** 社团简介 */
    @Excel(name = "社团简介")
    private String description;

    /** 分类ID */
    @Excel(name = "分类ID")
    private Long categoryId;

    /** 当前负责人ID */
    @Excel(name = "当前负责人ID")
    private Long leaderId;

    /** 所属学院ID */
    @Excel(name = "所属学院ID")
    private Long deptId;

    /** 成立时间 */
    @JsonFormat(pattern = "yyyy-MM-dd")
    @Excel(name = "成立时间", width = 30, dateFormat = "yyyy-MM-dd")
    private Date createdAt;

    /** 状态 */
    @Excel(name = "状态")
    private String status;

    /** LOGO地址 */
    @Excel(name = "LOGO地址")
    private String logoUrl;

    /** 软删除时间 */
    private Date deletedAt;

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

    public void setCategoryId(Long categoryId) 
    {
        this.categoryId = categoryId;
    }

    public Long getCategoryId() 
    {
        return categoryId;
    }

    public void setLeaderId(Long leaderId) 
    {
        this.leaderId = leaderId;
    }

    public Long getLeaderId() 
    {
        return leaderId;
    }

    public void setDeptId(Long deptId) 
    {
        this.deptId = deptId;
    }

    public Long getDeptId() 
    {
        return deptId;
    }

    public void setCreatedAt(Date createdAt) 
    {
        this.createdAt = createdAt;
    }

    public Date getCreatedAt() 
    {
        return createdAt;
    }

    public void setStatus(String status) 
    {
        this.status = status;
    }

    public String getStatus() 
    {
        return status;
    }

    public void setLogoUrl(String logoUrl) 
    {
        this.logoUrl = logoUrl;
    }

    public String getLogoUrl() 
    {
        return logoUrl;
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
            .append("clubId", getClubId())
            .append("name", getName())
            .append("description", getDescription())
            .append("categoryId", getCategoryId())
            .append("leaderId", getLeaderId())
            .append("deptId", getDeptId())
            .append("createdAt", getCreatedAt())
            .append("status", getStatus())
            .append("logoUrl", getLogoUrl())
            .append("deletedAt", getDeletedAt())
            .toString();
    }
}
