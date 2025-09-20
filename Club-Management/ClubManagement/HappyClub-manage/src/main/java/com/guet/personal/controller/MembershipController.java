package com.guet.personal.controller;

import java.util.List;
import javax.servlet.http.HttpServletResponse;

import com.guet.personal.domain.Dto.MembershipDto;
import com.guet.personal.domain.Vo.MembershipVo;
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
import com.guet.personal.domain.Membership;
import com.guet.personal.service.IMembershipService;
import com.guet.common.utils.poi.ExcelUtil;
import com.guet.common.core.page.TableDataInfo;

/**
 * 社团成员关系Controller
 * 
 * @author kevin
 * @date 2025-05-05
 */
@RestController
@RequestMapping("/personal/membership")
public class MembershipController extends BaseController
{
    @Autowired
    private IMembershipService membershipService;

    /**
     * 查询社团成员关系列表
     */
    // @PreAuthorize("@ss.hasPermi('personal:membership:list')")
    @GetMapping("/list")
    public TableDataInfo list(MembershipDto membership)
    {
        startPage();
        List<Membership> list = membershipService.selectMembershipList(membership);
        return getDataTable(list);
    }

    /**
     * 导出社团成员关系列表
     */
    // @PreAuthorize("@ss.hasPermi('personal:membership:export')")
    @Log(title = "社团成员关系", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, MembershipDto membership)
    {
        List<Membership> list = membershipService.selectMembershipList(membership);
        ExcelUtil<Membership> util = new ExcelUtil<Membership>(Membership.class);
        util.exportExcel(response, list, "社团成员关系数据");
    }

    /**
     * 获取社团成员关系详细信息
     */
    // @PreAuthorize("@ss.hasPermi('personal:membership:query')")
    @GetMapping(value = "/{membershipId}")
    public AjaxResult getInfo(@PathVariable("membershipId") Long membershipId)
    {
        System.out.println("membershipId:"+membershipId);
        return success(membershipService.selectMembershipByMembershipId(membershipId));
    }

    /**
     * 新增社团成员关系
     */
    // @PreAuthorize("@ss.hasPermi('personal:membership:add')")
    @Log(title = "社团成员关系", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody Membership membership)
    {
        return toAjax(membershipService.insertMembership(membership));
    }

    /**
     * 修改社团成员关系
     */
    // @PreAuthorize("@ss.hasPermi('personal:membership:edit')")
    @Log(title = "社团成员关系", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody Membership membership)
    {
        return toAjax(membershipService.updateMembership(membership));
    }

    /**
     * 删除社团成员关系
     */
    // @PreAuthorize("@ss.hasPermi('personal:membership:remove')")
    @Log(title = "社团成员关系", businessType = BusinessType.DELETE)
	@DeleteMapping("/{membershipIds}")
    public AjaxResult remove(@PathVariable Long[] membershipIds)
    {
        return toAjax(membershipService.deleteMembershipByMembershipIds(membershipIds));
    }

    /**
     * 查询社团成员列表
     */
    @GetMapping("/members/{clubId}")
    public AjaxResult getMembersByClubId(@PathVariable("clubId") Long clubId) {
        List<MembershipVo> members = membershipService.selectMembersByClubId(clubId);
        return AjaxResult.success(members);
    }
//     根据用户id查看其成果listAchievementsByMemberId
    //*
    // // 查看成员拥有的的果
    // export function listAchievementsByMemberId(memberId) {
    //   return request({
    //     url: `/personal/membership/achievements/${memberId}`,
    //     method: 'get'
    //   })
    // }
    // */
    @GetMapping("/achievements/{memberId}")
    public AjaxResult listAchievementsByMemberId(@PathVariable("memberId") Long memberId) {
        return AjaxResult.success(membershipService.listAchievementsByMemberId(memberId));
    }
    // **
    // //查看成员的参加的活动
    // export function listActivitiesByMemberId(memberId) {
    //   return request({
    //     url: `/personal/membership/activities/${memberId}`,
    //     method: 'get'
    //   })
    // }
    // /
    @GetMapping("/activities/{memberId}")
    public AjaxResult listActivitiesByMemberId(@PathVariable("memberId") Long memberId) {
        return AjaxResult.success(membershipService.listActivitiesByMemberId(memberId));
    }
}
