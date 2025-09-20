package com.guet.manage.controller;

import java.util.List;
import javax.servlet.http.HttpServletResponse;

import com.guet.manage.domain.dto.AnnouncementDto;
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
import com.guet.manage.domain.Announcement;
import com.guet.manage.service.IAnnouncementService;
import com.guet.common.utils.poi.ExcelUtil;
import com.guet.common.core.page.TableDataInfo;

/**
 * 公告管理Controller
 * 
 * @author kevin
 * @date 2025-04-30
 */
@RestController
@RequestMapping("/manage/announcement")
public class AnnouncementController extends BaseController
{
    @Autowired
    private IAnnouncementService announcementService;

    /**
     * 查询公告管理列表
     */
    // @PreAuthorize("@ss.hasPermi('manage:announcement:list')")
    @GetMapping("/list")
    public TableDataInfo list(AnnouncementDto announcement)
    {
        startPage();
        List<Announcement> list = announcementService.selectAnnouncementList(announcement);
        return getDataTable(list);
    }

    /**
     * 导出公告管理列表
     */
    // @PreAuthorize("@ss.hasPermi('manage:announcement:export')")
    @Log(title = "公告管理", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, AnnouncementDto announcement)
    {
        List<Announcement> list = announcementService.selectAnnouncementList(announcement);
        ExcelUtil<Announcement> util = new ExcelUtil<Announcement>(Announcement.class);
        util.exportExcel(response, list, "公告管理数据");
    }

    /**
     * 获取公告管理详细信息
     */
    // @PreAuthorize("@ss.hasPermi('manage:announcement:query')")
    @GetMapping(value = "/{announcementId}")
    public AjaxResult getInfo(@PathVariable("announcementId") Long announcementId)
    {
        return success(announcementService.selectAnnouncementByAnnouncementId(announcementId));
    }

    /**
     * 新增公告管理
     */
    // @PreAuthorize("@ss.hasPermi('manage:announcement:add')")
    @Log(title = "公告管理", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody Announcement announcement)
    {
        return toAjax(announcementService.insertAnnouncement(announcement));
    }

    /**
     * 修改公告管理
     */
    // @PreAuthorize("@ss.hasPermi('manage:announcement:edit')")
    @Log(title = "公告管理", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody Announcement announcement)
    {
        return toAjax(announcementService.updateAnnouncement(announcement));
    }

    /**
     * 删除公告管理
     */
    // @PreAuthorize("@ss.hasPermi('manage:announcement:remove')")
    @Log(title = "公告管理", businessType = BusinessType.DELETE)
	@DeleteMapping("/{announcementIds}")
    public AjaxResult remove(@PathVariable Long[] announcementIds)
    {
        return toAjax(announcementService.deleteAnnouncementByAnnouncementIds(announcementIds));
    }
}
