package com.guet.manage.domain.dto;

import com.guet.common.core.domain.BaseEntity;
import lombok.Data;

import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;

@Data
public class AuditDecisionRequest extends BaseEntity {
    @NotNull(message = "审核ID不能为空")
    private Long auditId;

    @NotBlank(message = "备注不能为空")
    @Size(min = 5, max = 200, message = "备注长度需在5-200字符之间")
    private String remark;

    @NotNull(message = "审核人ID不能为空")
    private Long processorId;
}
