package com.guet.happy.domain;

import lombok.Data;
import java.util.Date;

@Data
public class HAttendance {
    private Long attendanceId; // bigint 类型对应 Long
    private Integer clubId;    // int 类型对应 Integer
    private Integer userId;    // int 类型对应 Integer
    private Date clockInTime;  // datetime 类型对应 Date
    private Date clockOutTime; // datetime 类型对应 Date
    private Integer studyDuration; // int 类型对应 Integer
    private String status;     // enum 类型假设为 String（具体取决于枚举定义）
    private String notes;      // text 类型对应 String
    private Date createdAt;    // datetime 类型对应 Date
    private Date updatedAt;    // datetime 类型对应 Date
    private Date deletedAt;    // datetime 类型对应 Date
}
