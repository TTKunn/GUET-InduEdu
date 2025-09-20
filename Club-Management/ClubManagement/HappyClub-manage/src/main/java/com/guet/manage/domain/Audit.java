package com.guet.manage.domain;

import java.util.Date;
import com.fasterxml.jackson.annotation.JsonFormat;
import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import com.guet.common.annotation.Excel;
import com.guet.common.core.domain.BaseEntity;

/**
 * 通用审核对象 tb_audit
 * 
 * @author kevin
 * @date 2025-04-23
 */
public class Audit extends BaseEntity
{
    private static final long serialVersionUID = 1L;

    /** 审核ID */
    private Long auditId;

    /** 审核类型 */
    @Excel(name = "审核类型")
    private String type;

    /** 申请人ID */
    @Excel(name = "申请人ID")
    private Long applicantId;

    /** 处理人ID */
    @Excel(name = "处理人ID")
    private Long processorId;

    /** 审核状态 */
    @Excel(name = "审核状态")
    private String status;

    /** 关联业务ID */
    @Excel(name = "关联业务ID")
    private Long relatedId;

    /** 申请时间 */
    @JsonFormat(pattern = "yyyy-MM-dd")
    @Excel(name = "申请时间", width = 30, dateFormat = "yyyy-MM-dd")
    private Date createdAt;

    /** 处理时间 */
    @JsonFormat(pattern = "yyyy-MM-dd")
    @Excel(name = "处理时间", width = 30, dateFormat = "yyyy-MM-dd")
    private Date processedAt;

    /** 用户备注 */
    @Excel(name = "用户备注")
    private String userRemark;

    /** 软删除时间 */
    private Date deletedAt;

    public void setAuditId(Long auditId) 
    {
        this.auditId = auditId;
    }

    public Long getAuditId() 
    {
        return auditId;
    }

    public void setType(String type) 
    {
        this.type = type;
    }

    public String getType() 
    {
        return type;
    }

    public void setApplicantId(Long applicantId) 
    {
        this.applicantId = applicantId;
    }

    public Long getApplicantId() 
    {
        return applicantId;
    }

    public void setProcessorId(Long processorId) 
    {
        this.processorId = processorId;
    }

    public Long getProcessorId() 
    {
        return processorId;
    }

    public void setStatus(String status) 
    {
        this.status = status;
    }

    public String getStatus() 
    {
        return status;
    }

    public void setRelatedId(Long relatedId) 
    {
        this.relatedId = relatedId;
    }

    public Long getRelatedId() 
    {
        return relatedId;
    }

    public void setCreatedAt(Date createdAt) 
    {
        this.createdAt = createdAt;
    }

    public Date getCreatedAt() 
    {
        return createdAt;
    }

    public void setProcessedAt(Date processedAt) 
    {
        this.processedAt = processedAt;
    }

    public Date getProcessedAt() 
    {
        return processedAt;
    }

    public void setUserRemark(String userRemark) 
    {
        this.userRemark = userRemark;
    }

    public String getUserRemark() 
    {
        return userRemark;
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
            .append("auditId", getAuditId())
            .append("type", getType())
            .append("applicantId", getApplicantId())
            .append("processorId", getProcessorId())
            .append("status", getStatus())
            .append("relatedId", getRelatedId())
            .append("createdAt", getCreatedAt())
            .append("processedAt", getProcessedAt())
            .append("remark", getRemark())
            .append("userRemark", getUserRemark())
            .append("deletedAt", getDeletedAt())
            .toString();
    }
}
