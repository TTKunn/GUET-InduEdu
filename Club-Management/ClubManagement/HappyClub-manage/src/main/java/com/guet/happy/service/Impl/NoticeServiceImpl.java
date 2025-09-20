package com.guet.happy.service.Impl;

import com.guet.happy.domain.Notice;
import com.guet.happy.mapper.NoticeMapper;
import com.guet.happy.service.NoticeService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
public class NoticeServiceImpl implements NoticeService {

    @Autowired
    private NoticeMapper noticeMapper;

    @Override
    public List<Notice> getPublicNotices() {
        return noticeMapper.selectPublicNotice();
    }

    @Override
    public Notice getNoticeById(Integer announcementId) {
        return noticeMapper.selectNoticeById(announcementId);
    }
    @Override
    public List<Notice> getInnerNoticeList(Long clubId) {
        return noticeMapper.selectInnerNoticeByClubId(clubId);
    }

    @Override
    public List<Notice> getPublicNoticeList(Long clubId) {
        return noticeMapper.selectPublicNoticeByClubId(clubId);
    }
}
