package com.guet.personal.controller;

import java.util.List;
import javax.servlet.http.HttpServletResponse;
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
import com.guet.personal.domain.PersonalClub;
import com.guet.personal.service.IPersonalClubService;
import com.guet.common.utils.poi.ExcelUtil;
import com.guet.common.core.page.TableDataInfo;

/**
 * 社团信息Controller
 * 
 * @author kevin
 * @date 2025-05-05
 */
@RestController
@RequestMapping("/personal/PersonalClub")
public class PersonalClubController extends BaseController
{
    @Autowired
    private IPersonalClubService personalClubService;

    /**
     * 查询社团信息列表
     */
    // @PreAuthorize("@ss.hasPermi('personal:PersonalClub:list')")
    @GetMapping("/list")
    public TableDataInfo list(PersonalClub personalClub)
    {
        startPage();
        List<PersonalClub> list = personalClubService.selectPersonalClubList(personalClub);
        return getDataTable(list);
    }

    /**
     * 导出社团信息列表
     */
    // @PreAuthorize("@ss.hasPermi('personal:PersonalClub:export')")
    @Log(title = "社团信息", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, PersonalClub personalClub)
    {
        List<PersonalClub> list = personalClubService.selectPersonalClubList(personalClub);
        ExcelUtil<PersonalClub> util = new ExcelUtil<PersonalClub>(PersonalClub.class);
        util.exportExcel(response, list, "社团信息数据");
    }

    /**
     * 获取社团信息详细信息
     */
    // @PreAuthorize("@ss.hasPermi('personal:PersonalClub:query')")
    @GetMapping(value = "/{clubId}")
    public AjaxResult getInfo(@PathVariable("clubId") Long clubId)
    {
        return success(personalClubService.selectPersonalClubByClubId(clubId));
    }

    /**
     * 新增社团信息
     */
    // @PreAuthorize("@ss.hasPermi('personal:PersonalClub:add')")
    @Log(title = "社团信息", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody PersonalClub personalClub)
    {
        return toAjax(personalClubService.insertPersonalClub(personalClub));
    }

    /**
     * 修改社团信息
     */
    // @PreAuthorize("@ss.hasPermi('personal:PersonalClub:edit')")
    @Log(title = "社团信息", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody PersonalClub personalClub)
    {
        return toAjax(personalClubService.updatePersonalClub(personalClub));
    }

    /**
     * 删除社团信息
     */
    // @PreAuthorize("@ss.hasPermi('personal:PersonalClub:remove')")
    @Log(title = "社团信息", businessType = BusinessType.DELETE)
	@DeleteMapping("/{clubIds}")
    public AjaxResult remove(@PathVariable Long[] clubIds)
    {
        return toAjax(personalClubService.deletePersonalClubByClubIds(clubIds));
    }
}
