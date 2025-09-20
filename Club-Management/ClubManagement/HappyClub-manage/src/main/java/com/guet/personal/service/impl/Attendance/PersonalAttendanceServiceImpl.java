package com.guet.personal.service.impl.Attendance;

import java.util.List;

import com.guet.personal.domain.Dto.PersonalAttendanceDto;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.guet.personal.mapper.PersonalAttendanceMapper;
import com.guet.personal.domain.PersonalAttendance;
import com.guet.personal.service.IPersonalAttendanceService;

/**
 * 考勤管理Service业务层处理
 * 
 * @author kevin
 * @date 2025-05-01
 */
@Service
public class PersonalAttendanceServiceImpl implements IPersonalAttendanceService
{
    @Autowired
    private PersonalAttendanceMapper personalAttendanceMapper;

    /**
     * 查询考勤管理
     * 
     * @param attendanceId 考勤管理主键
     * @return 考勤管理
     */
    @Override
    public PersonalAttendance selectPattendanceByAttendanceId(Long attendanceId)
    {
        return personalAttendanceMapper.selectPattendanceByAttendanceId(attendanceId);
    }

    /**
     * 查询考勤管理列表
     * 
     * @param pattendance 考勤管理
     * @return 考勤管理
     */
    @Override
    public List<PersonalAttendance> selectPattendanceList(PersonalAttendanceDto pattendance)
    {
        return personalAttendanceMapper.selectPattendanceList(pattendance);
    }

    /**
     * 新增考勤管理
     * 
     * @param personalAttendance 考勤管理
     * @return 结果
     */
    @Override
    public int insertPattendance(PersonalAttendance personalAttendance)
    {
        return personalAttendanceMapper.insertPattendance(personalAttendance);
    }

    /**
     * 修改考勤管理
     * 
     * @param personalAttendance 考勤管理
     * @return 结果
     */
    @Override
    public int updatePattendance(PersonalAttendance personalAttendance)
    {
        return personalAttendanceMapper.updatePattendance(personalAttendance);
    }

    /**
     * 批量删除考勤管理
     * 
     * @param attendanceIds 需要删除的考勤管理主键
     * @return 结果
     */
    @Override
    public int deletePattendanceByAttendanceIds(Long[] attendanceIds)
    {
        return personalAttendanceMapper.deletePattendanceByAttendanceIds(attendanceIds);
    }

    /**
     * 删除考勤管理信息
     * 
     * @param attendanceId 考勤管理主键
     * @return 结果
     */
    @Override
    public int deletePattendanceByAttendanceId(Long attendanceId)
    {
        return personalAttendanceMapper.deletePattendanceByAttendanceId(attendanceId);
    }
}
