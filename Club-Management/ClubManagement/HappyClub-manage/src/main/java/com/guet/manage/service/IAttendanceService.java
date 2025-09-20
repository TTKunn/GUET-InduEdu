package com.guet.manage.service;

import java.util.List;
import com.guet.manage.domain.Attendance;
import com.guet.manage.domain.dto.AttendanceDto;

/**
 * 考勤管理Service接口
 * 
 * @author kevin
 * @date 2025-04-30
 */
public interface IAttendanceService 
{
    /**
     * 查询考勤管理
     * 
     * @param attendanceId 考勤管理主键
     * @return 考勤管理
     */
    public Attendance selectAttendanceByAttendanceId(Long attendanceId);

    /**
     * 查询考勤管理列表
     * 
     * @param attendance 考勤管理
     * @return 考勤管理集合
     */
    public List<Attendance> selectAttendanceList(AttendanceDto attendance);

    /**
     * 新增考勤管理
     * 
     * @param attendance 考勤管理
     * @return 结果
     */
    public int insertAttendance(Attendance attendance);

    /**
     * 修改考勤管理
     * 
     * @param attendance 考勤管理
     * @return 结果
     */
    public int updateAttendance(Attendance attendance);

    /**
     * 批量删除考勤管理
     * 
     * @param attendanceIds 需要删除的考勤管理主键集合
     * @return 结果
     */
    public int deleteAttendanceByAttendanceIds(Long[] attendanceIds);

    /**
     * 删除考勤管理信息
     * 
     * @param attendanceId 考勤管理主键
     * @return 结果
     */
    public int deleteAttendanceByAttendanceId(Long attendanceId);
}
