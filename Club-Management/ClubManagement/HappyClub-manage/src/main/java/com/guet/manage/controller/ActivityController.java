package com.guet.manage.controller;

import java.util.List;
import javax.servlet.http.HttpServletResponse;

import com.guet.manage.domain.dto.ActivityDto;
import com.guet.manage.domain.vo.ActivityVo;
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
import com.guet.manage.domain.Activity;
import com.guet.manage.service.IActivityService;
import com.guet.common.utils.poi.ExcelUtil;
import com.guet.common.core.page.TableDataInfo;

/**
 * 活动管理Controller
 * 
 * @author kevin
 * @date 2025-04-30
 */
@RestController
@RequestMapping("/manage/activity")
public class ActivityController extends BaseController
{
    @Autowired
    private IActivityService activityService;

    /**
     * 查询活动管理列表
     */
    // @PreAuthorize("@ss.hasPermi('manage:activity:list')")
    @GetMapping("/list")
    public TableDataInfo list(ActivityDto activity)
    {
        startPage();
        List<Activity> list = activityService.selectActivityList(activity);
        return getDataTable(list);
    }

    /**
     * 导出活动管理列表
     */
    // @PreAuthorize("@ss.hasPermi('manage:activity:export')")
    @Log(title = "活动管理", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, ActivityDto activity)
    {
        List<Activity> list = activityService.selectActivityList(activity);
        ExcelUtil<Activity> util = new ExcelUtil<Activity>(Activity.class);
        util.exportExcel(response, list, "活动管理数据");
    }

    /**
     * 获取活动管理详细信息
     */
    // @PreAuthorize("@ss.hasPermi('manage:activity:query')")
    @GetMapping(value = "/{activityId}")
    public AjaxResult getInfo(@PathVariable("activityId") Long activityId)
    {
        return success(activityService.selectActivityByActivityId(activityId));
    }

    /**
     * 新增活动管理
     */
    // @PreAuthorize("@ss.hasPermi('manage:activity:add')")
    @Log(title = "活动管理", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody Activity activity)
    {
        return toAjax(activityService.insertActivity(activity));
    }

    /**
     * 修改活动管理
     */
    // @PreAuthorize("@ss.hasPermi('manage:activity:edit')")
    @Log(title = "活动管理", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody Activity activity)
    {
        return toAjax(activityService.updateActivity(activity));
    }

    /**
     * 删除活动管理
     */
    // @PreAuthorize("@ss.hasPermi('manage:activity:remove')")
    @Log(title = "活动管理", businessType = BusinessType.DELETE)
	@DeleteMapping("/{activityIds}")
    public AjaxResult remove(@PathVariable Long[] activityIds)
    {
        return toAjax(activityService.deleteActivityByActivityIds(activityIds));
    }
}
