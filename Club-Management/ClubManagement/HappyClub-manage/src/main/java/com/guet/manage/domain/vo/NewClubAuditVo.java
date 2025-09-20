package com.guet.manage.domain.vo;

import com.guet.common.core.domain.BaseEntity;
import lombok.Data;

@Data
public class NewClubAuditVo{
    private Long auditId; // 审核记录ID
    private Long clubId; // 社团ID
    private String clubName; // 社团名称
    private String categoryName; // 社团类别名称
    private String deptName; // 社团所属学院名称
    private String applicant; // 申请人姓名
    private String status; // 审核状态
    private String userRemark; // 用户申请理由
    private String createAt;
    private String description; // 社团描述
    private String logoUrl;
}
