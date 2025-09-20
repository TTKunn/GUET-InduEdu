package com.guet.happy.service;

import com.guet.happy.domain.Notice;
import java.util.List;

public interface NoticeService {

    /**
     * 查询所有公开公告
     */
    List<Notice> getPublicNotices();

    /**
     * 根据 ID 查询公告
     */
    Notice getNoticeById(Integer announcementId);
    List<Notice> getInnerNoticeList(Long clubId);

    List<Notice> getPublicNoticeList(Long clubId);
}
