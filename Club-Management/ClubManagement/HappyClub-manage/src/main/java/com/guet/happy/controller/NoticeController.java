package com.guet.happy.controller;

import com.guet.common.core.domain.AjaxResult;
import com.guet.happy.domain.Notice;
import com.guet.happy.service.NoticeService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("happy/notices")
public class NoticeController {

    @Autowired
    private NoticeService noticeService;

    /**
     * 查询所有公开公告
     */
    @GetMapping("/public")
    public AjaxResult getPublicNotices() {
        System.out.println(noticeService.getPublicNotices());
        return AjaxResult.success(noticeService.getPublicNotices());
    }

    /**
     * 根据 ID 查询公告详情
     */
    @GetMapping("/{id}")
    public AjaxResult getNoticeById(@PathVariable("id") Integer announcementId) {
        return AjaxResult.success(noticeService.getNoticeById(announcementId));
    }
    /**
     * 获取某个社团的内部公告列表
     */
    @GetMapping("/inner/list/{clubId}")
    public AjaxResult getInnerNoticeList(@PathVariable Long clubId) {
        List<Notice> notices = noticeService.getInnerNoticeList(clubId);
        return AjaxResult.success(notices);
    }
    /**
     * 获取某个社团的内部公告列表
     */
    @GetMapping("/public/list/{clubId}")
    public AjaxResult getPublicNoticeList(@PathVariable Long clubId) {
        List<Notice> notices = noticeService.getPublicNoticeList(clubId);
        return AjaxResult.success(notices);
    }
}
