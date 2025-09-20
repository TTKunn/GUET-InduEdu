package com.guet.happy.service;

import com.guet.happy.domain.HAttendance;
import com.guet.happy.domain.attendanceStats;

import java.util.List;

public interface HAttendanceService {
    List<HAttendance> getAttendanceByClubIdAndUserId(Integer clubId, Integer userId);
    // 签到
    public int signIn(Long clubId, Long userId);

    // 获取最新未签退记录
    public HAttendance getLatestUncheckedInAttendance(Long userId);

    // 签退
    public int signOut(HAttendance attendance);
    /**
     * 获取本月考勤统计信息
     */
    public attendanceStats getAttendanceStatsByMonth(Long userId);
}
