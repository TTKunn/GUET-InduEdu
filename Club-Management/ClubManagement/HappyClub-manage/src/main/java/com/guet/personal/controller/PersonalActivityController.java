package com.guet.personal.controller;

import java.util.List;
import javax.servlet.http.HttpServletResponse;

import com.guet.personal.domain.Dto.PersonalActivityDto;
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
import com.guet.personal.domain.PersonalActivity;
import com.guet.personal.service.IPersonalActivityService;
import com.guet.common.utils.poi.ExcelUtil;
import com.guet.common.core.page.TableDataInfo;

/**
 * 活动管理Controller
 * 
 * @author kevin
 * @date 2025-05-01
 */
@RestController
@RequestMapping("/personal/activity")
public class PersonalActivityController extends BaseController
{
    @Autowired
    private IPersonalActivityService pactivityService;

    /**
     * 查询活动管理列表
     */
    // @PreAuthorize("@ss.hasPermi('personal:activity:list')")
    @GetMapping("/list")
    public TableDataInfo list(PersonalActivityDto pactivity)
    {
        startPage();
        System.out.println(pactivity);
        List<PersonalActivity> list = pactivityService.selectPactivityList(pactivity);
        return getDataTable(list);
    }

    /**
     * 导出活动管理列表
     */
    // @PreAuthorize("@ss.hasPermi('personal:activity:export')")
    @Log(title = "活动管理", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, PersonalActivityDto pactivity)
    {
        List<PersonalActivity> list = pactivityService.selectPactivityList(pactivity);
        ExcelUtil<PersonalActivity> util = new ExcelUtil<PersonalActivity>(PersonalActivity.class);
        util.exportExcel(response, list, "活动管理数据");
    }

    /**
     * 获取活动管理详细信息
     */
    // @PreAuthorize("@ss.hasPermi('personal:activity:query')")
    @GetMapping(value = "/{activityId}")
    public AjaxResult getInfo(@PathVariable("activityId") Long activityId)
    {
        return success(pactivityService.selectPactivityByActivityId(activityId));
    }

    /**
     * 新增活动管理
     */
    // @PreAuthorize("@ss.hasPermi('personal:activity:add')")
    @Log(title = "活动管理", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody PersonalActivity personalActivity)
    {
        return toAjax(pactivityService.insertPactivity(personalActivity));
    }

    /**
     * 修改活动管理
     */
    // @PreAuthorize("@ss.hasPermi('personal:activity:edit')")
    @Log(title = "活动管理", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody PersonalActivity personalActivity)
    {
        return toAjax(pactivityService.updatePactivity(personalActivity));
    }

    /**
     * 删除活动管理
     */
    // @PreAuthorize("@ss.hasPermi('personal:activity:remove')")
    @Log(title = "活动管理", businessType = BusinessType.DELETE)
	@DeleteMapping("/{activityIds}")
    public AjaxResult remove(@PathVariable Long[] activityIds)
    {
        return toAjax(pactivityService.deletePactivityByActivityIds(activityIds));
    }
}
