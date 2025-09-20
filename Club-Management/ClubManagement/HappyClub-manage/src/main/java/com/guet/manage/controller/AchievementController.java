package com.guet.manage.controller;

import java.util.List;
import javax.servlet.http.HttpServletResponse;

import com.guet.manage.domain.dto.AchievementDto;
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
import com.guet.manage.domain.Achievement;
import com.guet.manage.service.IAchievementService;
import com.guet.common.utils.poi.ExcelUtil;
import com.guet.common.core.page.TableDataInfo;

/**
 * 成果管理Controller
 * 
 * @author kevin
 * @date 2025-04-30
 */
@RestController
@RequestMapping("/manage/achievement")
public class AchievementController extends BaseController
{
    @Autowired
    private IAchievementService achievementService;

    /**
     * 查询成果管理列表
     */
    // @PreAuthorize("@ss.hasPermi('manage:achievement:list')")
    @GetMapping("/list")
    public TableDataInfo list(AchievementDto achievement)
    {
        startPage();
        List<Achievement> list = achievementService.selectAchievementList(achievement);
        return getDataTable(list);
    }

    /**
     * 导出成果管理列表
     */
    // @PreAuthorize("@ss.hasPermi('manage:achievement:export')")
    @Log(title = "成果管理", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, AchievementDto achievement)
    {
        List<Achievement> list = achievementService.selectAchievementList(achievement);
        ExcelUtil<Achievement> util = new ExcelUtil<Achievement>(Achievement.class);
        util.exportExcel(response, list, "成果管理数据");
    }

    /**
     * 获取成果管理详细信息
     */
    // @PreAuthorize("@ss.hasPermi('manage:achievement:query')")
    @GetMapping(value = "/{achievementId}")
    public AjaxResult getInfo(@PathVariable("achievementId") Long achievementId)
    {
        return success(achievementService.selectAchievementByAchievementId(achievementId));
    }

    /**
     * 新增成果管理
     */
    // @PreAuthorize("@ss.hasPermi('manage:achievement:add')")
    @Log(title = "成果管理", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody Achievement achievement)
    {
        return toAjax(achievementService.insertAchievement(achievement));
    }

    /**
     * 修改成果管理
     */
    // @PreAuthorize("@ss.hasPermi('manage:achievement:edit')")
    @Log(title = "成果管理", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody Achievement achievement)
    {
        return toAjax(achievementService.updateAchievement(achievement));
    }

    /**
     * 删除成果管理
     */
    // @PreAuthorize("@ss.hasPermi('manage:achievement:remove')")
    @Log(title = "成果管理", businessType = BusinessType.DELETE)
	@DeleteMapping("/{achievementIds}")
    public AjaxResult remove(@PathVariable Long[] achievementIds)
    {
        return toAjax(achievementService.deleteAchievementByAchievementIds(achievementIds));
    }
}
