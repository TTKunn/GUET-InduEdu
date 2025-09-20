package com.guet.happy.service.Impl;

import com.guet.happy.domain.HAttendance;
import com.guet.happy.domain.attendanceStats;
import com.guet.happy.mapper.HAttendanceMapper;
import com.guet.happy.service.HAttendanceService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class HAttendanceServiceImpl implements HAttendanceService {

    @Autowired
    private HAttendanceMapper hAttendanceMapper;

    @Override
    public List<HAttendance> getAttendanceByClubIdAndUserId(Integer clubId, Integer userId) {
        return hAttendanceMapper.selectAttendanceByClubIdAndUserId(clubId, userId);
    }
    // 签到
    @Override
    public int signIn(Long clubId, Long userId) {
        return hAttendanceMapper.insertAttendance(clubId, userId);
    }

    // 获取最新未签退记录
    @Override
    public HAttendance getLatestUncheckedInAttendance(Long userId) {
        return hAttendanceMapper.selectLatestUncheckedInAttendance(userId);
    }

    // 签退
    @Override
    public int signOut(HAttendance attendance) {
        return hAttendanceMapper.updateAttendance(attendance);
    }
    /**
     * 获取本月考勤统计信息
     */
    @Override
    public attendanceStats getAttendanceStatsByMonth(Long userId) {
        return hAttendanceMapper.selectAttendanceStatsByMonth(userId);
    }
}
