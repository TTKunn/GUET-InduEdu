package com.guet.personal.domain.Dto.Audit;

import lombok.Data;

@Data
public class AuditDto {
    private Long applicantId;
    private String type;
    private String status;
    private Long auditId;
}
