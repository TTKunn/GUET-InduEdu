package com.guet.happy.mapper;

import com.guet.happy.domain.HAttendance;
import com.guet.happy.domain.attendanceStats;
import org.apache.ibatis.annotations.Param;
import java.util.List;

public interface HAttendanceMapper {
    List<HAttendance> selectAttendanceByClubIdAndUserId(@Param("clubId") Integer clubId, @Param("userId") Integer userId);
    // 签到：插入新的考勤记录
    int insertAttendance(@Param("clubId") Long clubId, @Param("userId") Long userId);

    // 查询用户最新的未签退记录
    HAttendance selectLatestUncheckedInAttendance(@Param("userId") Long userId);

    // 签退：更新考勤记录
    int updateAttendance(HAttendance attendance);
    attendanceStats selectAttendanceStatsByMonth(Long useId);
}
