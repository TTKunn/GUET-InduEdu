package com.guet.manage.controller;

import java.util.List;
import javax.servlet.http.HttpServletResponse;

import com.guet.manage.domain.vo.ClubLeaderVo;
import com.guet.manage.domain.vo.ClubVo;
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
import com.guet.manage.domain.vo.Club;
import com.guet.manage.service.IClubService;
import com.guet.common.utils.poi.ExcelUtil;
import com.guet.common.core.page.TableDataInfo;

/**
 * 社团管理Controller
 * 
 * @author kevin
 * @date 2025-04-21
 */
@RestController
@RequestMapping("/manage/club")
public class ClubController extends BaseController
{
    @Autowired
    private IClubService clubService;

    /**
     * 查询社团管理列表
     */
    // @PreAuthorize("@ss.hasPermi('manage:club:list')")
    @GetMapping("/list")
    public TableDataInfo list(Club club)
    {
        startPage();
        List<ClubVo> volist = clubService.selectClubVoList(club);
        return getDataTable(volist);
    }

    /**
     * 导出社团管理列表
     */
    // @PreAuthorize("@ss.hasPermi('manage:club:export')")
    @Log(title = "社团管理", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, Club club)
    {
        List<Club> list = clubService.selectClubList(club);
        ExcelUtil<Club> util = new ExcelUtil<Club>(Club.class);
        util.exportExcel(response, list, "社团管理数据");
    }

    /**
     * 获取社团管理详细信息
     */
    // @PreAuthorize("@ss.hasPermi('manage:club:query')")
    @GetMapping(value = "/{clubId}")
    public AjaxResult getInfo(@PathVariable("clubId") Long clubId)
    {
        return success(clubService.selectClubByClubId(clubId));
    }

    /**
     * 新增社团管理
     */
    // @PreAuthorize("@ss.hasPermi('manage:club:add')")
    @Log(title = "社团管理", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody Club club)
    {
        return toAjax(clubService.insertClub(club));
    }

    /**
     * 修改社团管理
     */
    // @PreAuthorize("@ss.hasPermi('manage:club:edit')")
    @Log(title = "社团管理", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody Club club)
    {
        return toAjax(clubService.updateClub(club));
    }

    /**
     * 删除社团管理
     */
    // @PreAuthorize("@ss.hasPermi('manage:club:remove')")
    @Log(title = "社团管理", businessType = BusinessType.DELETE)
	@DeleteMapping("/{clubIds}")
    public AjaxResult remove(@PathVariable Long[] clubIds)
    {
        return toAjax(clubService.deleteClubByClubIds(clubIds));
    }

    /**
     * 通过社团ID查询用户
     */
    // @PreAuthorize("@ss.hasPermi('manage:club:userList')")
    @GetMapping("/listMember/{clubId}")
    @Log(title = "社团管理", businessType = BusinessType.OTHER)
    public AjaxResult selectUserVoListByClubId(@PathVariable Long clubId)
    {
        return success(clubService.selectUserVoListByClubId(clubId));
    }

    /**
     * 查询所有社团负责人名称
     */
    // @PreAuthorize("@ss.hasPermi('manage:club:clubLeader')")
    @GetMapping("/clubLeader")
    @Log(title = "社团管理", businessType = BusinessType.OTHER)
    public TableDataInfo selectAllClubLeader(){
        startPage();
        List<ClubLeaderVo> list = clubService.selectAllClubLeader();
        return getDataTable(list);
    }
}
