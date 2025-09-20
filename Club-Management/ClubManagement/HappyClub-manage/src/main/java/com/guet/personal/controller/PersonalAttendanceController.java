package com.guet.personal.controller;

import java.util.List;
import javax.servlet.http.HttpServletResponse;

import com.guet.personal.domain.Dto.PersonalAttendanceDto;
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
import com.guet.personal.domain.PersonalAttendance;
import com.guet.personal.service.IPersonalAttendanceService;
import com.guet.common.utils.poi.ExcelUtil;
import com.guet.common.core.page.TableDataInfo;

/**
 * 考勤管理Controller
 * 
 * @author kevin
 * @date 2025-05-01
 */
@RestController
@RequestMapping("/personal/attendance")
public class PersonalAttendanceController extends BaseController
{
    @Autowired
    private IPersonalAttendanceService pattendanceService;

    /**
     * 查询考勤管理列表
     */
    // @PreAuthorize("@ss.hasPermi('personal:attendance:list')")
    @GetMapping("/list")
    public TableDataInfo list(PersonalAttendanceDto pattendance)
    {
        startPage();
        List<PersonalAttendance> list = pattendanceService.selectPattendanceList(pattendance);
        return getDataTable(list);
    }

    /**
     * 导出考勤管理列表
     */
    // @PreAuthorize("@ss.hasPermi('personal:attendance:export')")
    @Log(title = "考勤管理", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, PersonalAttendanceDto pattendance)
    {
        List<PersonalAttendance> list = pattendanceService.selectPattendanceList(pattendance);
        ExcelUtil<PersonalAttendance> util = new ExcelUtil<PersonalAttendance>(PersonalAttendance.class);
        util.exportExcel(response, list, "考勤管理数据");
    }

    /**
     * 获取考勤管理详细信息
     */
    // @PreAuthorize("@ss.hasPermi('personal:attendance:query')")
    @GetMapping(value = "/{attendanceId}")
    public AjaxResult getInfo(@PathVariable("attendanceId") Long attendanceId)
    {
        return success(pattendanceService.selectPattendanceByAttendanceId(attendanceId));
    }

    /**
     * 新增考勤管理
     */
    // @PreAuthorize("@ss.hasPermi('personal:attendance:add')")
    @Log(title = "考勤管理", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody PersonalAttendance personalAttendance)
    {
        return toAjax(pattendanceService.insertPattendance(personalAttendance));
    }

    /**
     * 修改考勤管理
     */
    // @PreAuthorize("@ss.hasPermi('personal:attendance:edit')")
    @Log(title = "考勤管理", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody PersonalAttendance personalAttendance)
    {
        return toAjax(pattendanceService.updatePattendance(personalAttendance));
    }

    /**
     * 删除考勤管理
     */
    // @PreAuthorize("@ss.hasPermi('personal:attendance:remove')")
    @Log(title = "考勤管理", businessType = BusinessType.DELETE)
	@DeleteMapping("/{attendanceIds}")
    public AjaxResult remove(@PathVariable Long[] attendanceIds)
    {
        return toAjax(pattendanceService.deletePattendanceByAttendanceIds(attendanceIds));
    }
}
