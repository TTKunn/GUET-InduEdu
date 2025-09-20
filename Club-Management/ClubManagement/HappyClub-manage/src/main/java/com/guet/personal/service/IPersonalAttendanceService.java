package com.guet.personal.service;

import java.util.List;

import com.guet.personal.domain.Dto.PersonalAttendanceDto;
import com.guet.personal.domain.PersonalAttendance;

/**
 * 考勤管理Service接口
 * 
 * @author kevin
 * @date 2025-05-01
 */
public interface IPersonalAttendanceService
{
    /**
     * 查询考勤管理
     * 
     * @param attendanceId 考勤管理主键
     * @return 考勤管理
     */
    public PersonalAttendance selectPattendanceByAttendanceId(Long attendanceId);

    /**
     * 查询考勤管理列表
     * 
     * @param pattendance 考勤管理
     * @return 考勤管理集合
     */
    public List<PersonalAttendance> selectPattendanceList(PersonalAttendanceDto pattendance);

    /**
     * 新增考勤管理
     * 
     * @param personalAttendance 考勤管理
     * @return 结果
     */
    public int insertPattendance(PersonalAttendance personalAttendance);

    /**
     * 修改考勤管理
     * 
     * @param personalAttendance 考勤管理
     * @return 结果
     */
    public int updatePattendance(PersonalAttendance personalAttendance);

    /**
     * 批量删除考勤管理
     * 
     * @param attendanceIds 需要删除的考勤管理主键集合
     * @return 结果
     */
    public int deletePattendanceByAttendanceIds(Long[] attendanceIds);

    /**
     * 删除考勤管理信息
     * 
     * @param attendanceId 考勤管理主键
     * @return 结果
     */
    public int deletePattendanceByAttendanceId(Long attendanceId);
}
