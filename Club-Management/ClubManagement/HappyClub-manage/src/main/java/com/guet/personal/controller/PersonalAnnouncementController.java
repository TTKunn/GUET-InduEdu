package com.guet.personal.controller;

import java.util.List;
import javax.servlet.http.HttpServletResponse;

import com.guet.personal.domain.Dto.PersonalAnnouncementDto;
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
import com.guet.personal.domain.PersonalAnnouncement;
import com.guet.personal.service.IPersonalAnnouncementService;
import com.guet.common.utils.poi.ExcelUtil;
import com.guet.common.core.page.TableDataInfo;

/**
 * 公告管理Controller
 * 
 * @author kevin
 * @date 2025-05-01
 */
@RestController
@RequestMapping("/personal/announcement")
public class PersonalAnnouncementController extends BaseController
{
    @Autowired
    private IPersonalAnnouncementService pannouncementService;

    /**
     * 查询公告管理列表
     */
    // @PreAuthorize("@ss.hasPermi('personal:announcement:list')")
    @GetMapping("/list")
    public TableDataInfo list(PersonalAnnouncementDto pannouncement)
    {
        startPage();
        List<PersonalAnnouncement> list = pannouncementService.selectPannouncementList(pannouncement);
        return getDataTable(list);
    }

    /**
     * 导出公告管理列表
     */
    // @PreAuthorize("@ss.hasPermi('personal:announcement:export')")
    @Log(title = "公告管理", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, PersonalAnnouncementDto pannouncement)
    {
        List<PersonalAnnouncement> list = pannouncementService.selectPannouncementList(pannouncement);
        ExcelUtil<PersonalAnnouncement> util = new ExcelUtil<PersonalAnnouncement>(PersonalAnnouncement.class);
        util.exportExcel(response, list, "公告管理数据");
    }

    /**
     * 获取公告管理详细信息
     */
    // @PreAuthorize("@ss.hasPermi('personal:announcement:query')")
    @GetMapping(value = "/{announcementId}")
    public AjaxResult getInfo(@PathVariable("announcementId") Long announcementId)
    {
        return success(pannouncementService.selectPannouncementByAnnouncementId(announcementId));
    }

    /**
     * 新增公告管理
     */
    // @PreAuthorize("@ss.hasPermi('personal:announcement:add')")
    @Log(title = "公告管理", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody PersonalAnnouncement personalAnnouncement)
    {
        return toAjax(pannouncementService.insertPannouncement(personalAnnouncement));
    }

    /**
     * 修改公告管理
     */
    // @PreAuthorize("@ss.hasPermi('personal:announcement:edit')")
    @Log(title = "公告管理", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody PersonalAnnouncement personalAnnouncement)
    {
        return toAjax(pannouncementService.updatePannouncement(personalAnnouncement));
    }

    /**
     * 删除公告管理
     */
    // @PreAuthorize("@ss.hasPermi('personal:announcement:remove')")
    @Log(title = "公告管理", businessType = BusinessType.DELETE)
	@DeleteMapping("/{announcementIds}")
    public AjaxResult remove(@PathVariable Long[] announcementIds)
    {
        return toAjax(pannouncementService.deletePannouncementByAnnouncementIds(announcementIds));
    }
}
