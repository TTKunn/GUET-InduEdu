package com.guet.manage.service.impl;

import java.util.List;

import com.guet.manage.domain.dto.AttendanceDto;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.guet.manage.mapper.AttendanceMapper;
import com.guet.manage.domain.Attendance;
import com.guet.manage.service.IAttendanceService;

/**
 * 考勤管理Service业务层处理
 * 
 * @author kevin
 * @date 2025-04-30
 */
@Service
public class AttendanceServiceImpl implements IAttendanceService 
{
    @Autowired
    private AttendanceMapper attendanceMapper;

    /**
     * 查询考勤管理
     * 
     * @param attendanceId 考勤管理主键
     * @return 考勤管理
     */
    @Override
    public Attendance selectAttendanceByAttendanceId(Long attendanceId)
    {
        return attendanceMapper.selectAttendanceByAttendanceId(attendanceId);
    }

    /**
     * 查询考勤管理列表
     * 
     * @param attendance 考勤管理
     * @return 考勤管理
     */
    @Override
    public List<Attendance> selectAttendanceList(AttendanceDto attendance)
    {
        return attendanceMapper.selectAttendanceList(attendance);
    }

    /**
     * 新增考勤管理
     * 
     * @param attendance 考勤管理
     * @return 结果
     */
    @Override
    public int insertAttendance(Attendance attendance)
    {
        return attendanceMapper.insertAttendance(attendance);
    }

    /**
     * 修改考勤管理
     * 
     * @param attendance 考勤管理
     * @return 结果
     */
    @Override
    public int updateAttendance(Attendance attendance)
    {
        return attendanceMapper.updateAttendance(attendance);
    }

    /**
     * 批量删除考勤管理
     * 
     * @param attendanceIds 需要删除的考勤管理主键
     * @return 结果
     */
    @Override
    public int deleteAttendanceByAttendanceIds(Long[] attendanceIds)
    {
        return attendanceMapper.deleteAttendanceByAttendanceIds(attendanceIds);
    }

    /**
     * 删除考勤管理信息
     * 
     * @param attendanceId 考勤管理主键
     * @return 结果
     */
    @Override
    public int deleteAttendanceByAttendanceId(Long attendanceId)
    {
        return attendanceMapper.deleteAttendanceByAttendanceId(attendanceId);
    }
}
