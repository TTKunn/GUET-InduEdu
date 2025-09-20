package com.guet.manage.controller;

import java.util.List;
import javax.servlet.http.HttpServletResponse;

import com.guet.manage.domain.dto.AttendanceDto;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import com.guet.common.annotation.Log;
import com.guet.common.core.controller.BaseController;
import com.guet.common.core.domain.AjaxResult;
import com.guet.common.enums.BusinessType;
import com.guet.manage.domain.Attendance;
import com.guet.manage.service.IAttendanceService;
import com.guet.common.utils.poi.ExcelUtil;
import com.guet.common.core.page.TableDataInfo;

/**
 * 考勤管理Controller
 * 
 * @author kevin
 * @date 2025-04-30
 */
@RestController
@RequestMapping("/manage/attendance")
public class AttendanceController extends BaseController
{
    @Autowired
    private IAttendanceService attendanceService;

    /**
     * 查询考勤管理列表
     */
    // @PreAuthorize("@ss.hasPermi('manage:attendance:list')")
    @GetMapping("/list")
    public TableDataInfo list(AttendanceDto attendance)
    {
        startPage();
        List<Attendance> list = attendanceService.selectAttendanceList(attendance);
        return getDataTable(list);
    }

    /**
     * 导出考勤管理列表
     */
    // @PreAuthorize("@ss.hasPermi('manage:attendance:export')")
    @Log(title = "考勤管理", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, AttendanceDto attendance)
    {
        List<Attendance> list = attendanceService.selectAttendanceList(attendance);
        ExcelUtil<Attendance> util = new ExcelUtil<Attendance>(Attendance.class);
        util.exportExcel(response, list, "考勤管理数据");
    }

    /**
     * 获取考勤管理详细信息
     */
    // @PreAuthorize("@ss.hasPermi('manage:attendance:query')")
    @GetMapping(value = "/{attendanceId}")
    public AjaxResult getInfo(@PathVariable("attendanceId") Long attendanceId)
    {
        return success(attendanceService.selectAttendanceByAttendanceId(attendanceId));
    }

    /**
     * 新增考勤管理
     */
    // @PreAuthorize("@ss.hasPermi('manage:attendance:add')")
    @Log(title = "考勤管理", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody Attendance attendance)
    {
        return toAjax(attendanceService.insertAttendance(attendance));
    }

    /**
     * 修改考勤管理
     */
    // @PreAuthorize("@ss.hasPermi('manage:attendance:edit')")
    @Log(title = "考勤管理", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody Attendance attendance)
    {
        return toAjax(attendanceService.updateAttendance(attendance));
    }

    /**
     * 删除考勤管理
     */
    // @PreAuthorize("@ss.hasPermi('manage:attendance:remove')")
    @Log(title = "考勤管理", businessType = BusinessType.DELETE)
	@DeleteMapping("/{attendanceIds}")
    public AjaxResult remove(@PathVariable Long[] attendanceIds)
    {
        return toAjax(attendanceService.deleteAttendanceByAttendanceIds(attendanceIds));
    }
}
