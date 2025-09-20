package com.guet.manage.controller;

import com.guet.common.core.controller.BaseController;
import com.guet.common.core.domain.AjaxResult;
import com.guet.common.core.page.TableDataInfo;
import com.guet.manage.domain.dto.*;
import com.guet.manage.domain.vo.AchievementAuditVo;
import com.guet.manage.domain.vo.ActivityAuditVo;
import com.guet.manage.domain.vo.AnnouncementAuditVo;
import com.guet.manage.domain.vo.NewClubAuditVo;
import com.guet.manage.service.AuditService;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;
import javax.annotation.Resource;
import javax.validation.Valid;
import java.util.List;

@RestController
@RequestMapping("/manage/audit")
public class AuditController extends BaseController { // 关键点：继承 BaseController
    @Resource
    private AuditService auditService;

    @GetMapping("/listAnnouncements") // 查询需要审核的公告列表
    // @PreAuthorize("@ss.hasPermi('manage:announcement:query')") // 若依权限控制
    public TableDataInfo selectAuditAnnouncements(AnnouncementAuditQueryDto auditAnnouncement) {
        // 若依的 startPage() 会自动从请求中读取 pageNum 和 pageSize
        startPage();
        List<AnnouncementAuditVo> list = auditService.selectAuditAnnouncements(auditAnnouncement);
        return getDataTable(list); // 使用父类方法封装分页数据
    }

    // 公告审核通过接口
    @PostMapping("/approveAnnouncement")
    // @PreAuthorize("@ss.hasPermi('manage:announcement:approve')") // 若依权限控制
    public AjaxResult approveAuditAnnouncement(@RequestBody AuditDecisionRequest auditDecisionRequest) {
        return toAjax(auditService.approveAnnouncement(auditDecisionRequest));
    }

    // 公告审核拒绝接口
    @PostMapping("/rejectAnnouncement")
    // @PreAuthorize("@ss.hasPermi('manage:announcement:reject')") // 若依权限控制
    public AjaxResult rejectAuditAnnouncement(@RequestBody AuditDecisionRequest auditDecisionRequest) {
        return toAjax(auditService.rejectAnnouncement(auditDecisionRequest));
    }

    /**
     * 分页查询活动审核列表
     // * @param ActivityAuditQueryDto 查询条件（自动绑定参数）
     * @return 分页数据
     */
    @GetMapping("/listActivities")
    // @PreAuthorize("@ss.hasPermi('manage:activity:query')")
    public TableDataInfo selectAuditActivities(@Valid ActivityAuditQueryDto auditActivityDto) {
        // 启用分页（自动读取pageNum/pageSize参数）
        startPage();
        // 执行查询
        List<ActivityAuditVo> list = auditService.selectAuditActivities(auditActivityDto);
        // 封装分页结果
        System.out.println("list = " + list);
        return getDataTable(list);
        // return "ok";
    }

    /**
     * 审核通过活动
     * @param request 审核请求体（JSON自动反序列化）
     */
    @PostMapping("/approveActivity")
    // @PreAuthorize("@ss.hasPermi('manage:activity:approve')")
    public AjaxResult approveAuditActivity(@RequestBody AuditDecisionRequest request) {
        // 参数校验（通过JSR-303注解）
        return toAjax(auditService.approveActivity(request));
    }

    /**
     * 审核拒绝活动
     * @param request 审核请求体（必须包含remark）
     */
    @PostMapping("/rejectActivity")
    // @PreAuthorize("@ss.hasPermi('manage:activity:reject')")
    public AjaxResult rejectAuditActivity(@Valid @RequestBody AuditDecisionRequest request) {
        return toAjax(auditService.rejectActivity(request));
    }

    @GetMapping("/listNewClub") // 查询需要审核的社团注册列表
    // @PreAuthorize("@ss.hasPermi('manage:newClub:query')")
    public TableDataInfo selectAuditNewClub(NewClubAuditDto auditClubDto) {
        // 启用分页（自动读取pageNum/pageSize参数）
        startPage();
        // 执行查询
        List<NewClubAuditVo> list = auditService.selectAuditNewClub(auditClubDto);
        // 封装分页结果
        return getDataTable(list);
    }
    // 公告审核通过接口
    @PostMapping("/approveNewClub")
    // @PreAuthorize("@ss.hasPermi('manage:newClub:approve')")
    public AjaxResult approveAuditNewClub(@RequestBody AuditDecisionRequest auditDecisionRequest) {
        return toAjax(auditService.approveNewClub(auditDecisionRequest));
    }

    // 公告审核拒绝接口
    @PostMapping("/rejectNewClub")
    // @PreAuthorize("@ss.hasPermi('manage:newClub:reject')")
    public AjaxResult rejectAuditNewClub(@RequestBody AuditDecisionRequest auditDecisionRequest) {
        return toAjax(auditService.rejectNewClub(auditDecisionRequest));
    }

    // 新增Achievement审核相关接口 =======================================

    /**
     * 分页查询成果审核列表
     * @param queryDto 查询条件（自动绑定参数）
     */
    @GetMapping("/listAchievements")
    // @PreAuthorize("@ss.hasPermi('manage:achievement:query')")
    public TableDataInfo selectAuditAchievements(@Valid AchievementAuditQueryDto queryDto) {
        startPage();
        List<AchievementAuditVo> list = auditService.selectAuditAchievements(queryDto);
        return getDataTable(list);
    }

    /**
     * 审核通过成果
     * @param request 审核请求体（需包含成果ID和审核人信息）
     */
    @PostMapping("/approveAchievement")
    // @PreAuthorize("@ss.hasPermi('manage:achievement:approve')")
    public AjaxResult approveAchievement(@Valid @RequestBody AuditDecisionRequest request) {
        return toAjax(auditService.approveAchievement(request));
    }

    /**
     * 审核拒绝成果（需填写拒绝理由）
     * @param request 审核请求体（需包含remark字段）
     */
    @PostMapping("/rejectAchievement")
    // @PreAuthorize("@ss.hasPermi('manage:achievement:reject')")
    public AjaxResult rejectAchievement(@Valid @RequestBody AuditDecisionRequest request) {
        return toAjax(auditService.rejectAchievement(request));
    }
}