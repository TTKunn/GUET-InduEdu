package com.guet.happy.domain;

import lombok.Data;

import java.util.Date;

/**
 * @author Sissot
 */
@Data
public class Notice {
    private Long announcementId;
    private String title;
    private String content;
    private Integer publisherId;
    private String type;
    private String status;
    private String createdAt;
    private Date deletedAt;
    private Integer clubId;
    private Long userId;
    private String userName;
    private String clubName;
    private String nickName;
}
