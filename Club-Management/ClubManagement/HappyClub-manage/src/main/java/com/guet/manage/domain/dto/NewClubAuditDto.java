package com.guet.manage.domain.dto;

import com.guet.common.core.domain.BaseEntity;
import lombok.Data;

@Data
public class NewClubAuditDto extends BaseEntity {
    private String clubName; // 社团名称
    private Long categoryId; // 社团类别ID
    private Long deptId; // 社团所属学院ID
}
