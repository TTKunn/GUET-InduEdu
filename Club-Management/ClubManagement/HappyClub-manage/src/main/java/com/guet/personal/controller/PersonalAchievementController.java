package com.guet.personal.controller;

import java.util.List;
import javax.servlet.http.HttpServletResponse;

import com.guet.personal.domain.Dto.PersonalAchievementDto;
import com.guet.personal.domain.Vo.PersonalAchievementVo;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.transaction.annotation.Transactional;
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
import com.guet.personal.domain.PersonalAchievement;
import com.guet.personal.service.IPersonalAchievementService;
import com.guet.common.utils.poi.ExcelUtil;
import com.guet.common.core.page.TableDataInfo;

/**
 * 成果管理Controller
 * 
 * @author kevin
 * @date 2025-05-01
 */
@RestController
@RequestMapping("/personal/achievement")
public class PersonalAchievementController extends BaseController
{
    @Autowired
    private IPersonalAchievementService pachievementService;

    /**
     * 查询成果管理列表
     */
    // @PreAuthorize("@ss.hasPermi('personal:achievement:list')")
    @GetMapping("/list")
    public TableDataInfo list(PersonalAchievementDto pachievement)
    {
        startPage();
        List<PersonalAchievementVo> list = pachievementService.selectPachievementList(pachievement);
        return getDataTable(list);
    }

    /**
     * 导出成果管理列表
     */
    // @PreAuthorize("@ss.hasPermi('personal:achievement:export')")
    // @Log(title = "成果管理", businessType = BusinessType.EXPORT)
    // @PostMapping("/export")
    // public void export(HttpServletResponse response, PersonalAchievementDto pachievement)
    // {
    //     List<PersonalAchievementVo> list = pachievementService.selectPachievementList(pachievement);
    //     ExcelUtil<PersonalAchievement> util = new ExcelUtil<PersonalAchievement>(PersonalAchievement.class);
    //     util.exportExcel(response, list, "成果管理数据");
    // }

    /**
     * 获取成果管理详细信息
     */
    // @PreAuthorize("@ss.hasPermi('personal:achievement:query')")
    @GetMapping(value = "/{achievementId}")
    public AjaxResult getInfo(@PathVariable("achievementId") Long achievementId)
    {
        return success(pachievementService.selectPachievementByAchievementId(achievementId));
    }

    /**
     * 新增成果管理
     */
    // @PreAuthorize("@ss.hasPermi('personal:achievement:add')")
    @Log(title = "成果管理", businessType = BusinessType.INSERT)
    @PostMapping
    @Transactional // 添加事务注解
    public AjaxResult add(@RequestBody PersonalAchievement personalAchievement)
    {
        return toAjax(pachievementService.insertPachievement(personalAchievement));
    }

    /**
     * 修改成果管理
     */
    // @PreAuthorize("@ss.hasPermi('personal:achievement:edit')")
    @Log(title = "成果管理", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody PersonalAchievement personalAchievement)
    {
        return toAjax(pachievementService.updatePachievement(personalAchievement));
    }

    /**
     * 删除成果管理
     */
    // @PreAuthorize("@ss.hasPermi('personal:achievement:remove')")
    @Log(title = "成果管理", businessType = BusinessType.DELETE)
	@DeleteMapping("/{achievementIds}")
    public AjaxResult remove(@PathVariable Long[] achievementIds)
    {
        return toAjax(pachievementService.deletePachievementByAchievementIds(achievementIds));
    }
}
