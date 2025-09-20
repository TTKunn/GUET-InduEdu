package com.guet.manage.service.impl;

import java.util.List;

import com.guet.manage.domain.dto.AnnouncementDto;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.guet.manage.mapper.AnnouncementMapper;
import com.guet.manage.domain.Announcement;
import com.guet.manage.service.IAnnouncementService;

/**
 * 公告管理Service业务层处理
 * 
 * @author kevin
 * @date 2025-04-30
 */
@Service
public class AnnouncementServiceImpl implements IAnnouncementService 
{
    @Autowired
    private AnnouncementMapper announcementMapper;

    /**
     * 查询公告管理
     * 
     * @param announcementId 公告管理主键
     * @return 公告管理
     */
    @Override
    public Announcement selectAnnouncementByAnnouncementId(Long announcementId)
    {
        return announcementMapper.selectAnnouncementByAnnouncementId(announcementId);
    }

    /**
     * 查询公告管理列表
     * 
     * @param announcement 公告管理
     * @return 公告管理
     */
    @Override
    public List<Announcement> selectAnnouncementList(AnnouncementDto announcement)
    {
        return announcementMapper.selectAnnouncementList(announcement);
    }

    /**
     * 新增公告管理
     * 
     * @param announcement 公告管理
     * @return 结果
     */
    @Override
    public int insertAnnouncement(Announcement announcement)
    {
        return announcementMapper.insertAnnouncement(announcement);
    }

    /**
     * 修改公告管理
     * 
     * @param announcement 公告管理
     * @return 结果
     */
    @Override
    public int updateAnnouncement(Announcement announcement)
    {
        return announcementMapper.updateAnnouncement(announcement);
    }

    /**
     * 批量删除公告管理
     * 
     * @param announcementIds 需要删除的公告管理主键
     * @return 结果
     */
    @Override
    public int deleteAnnouncementByAnnouncementIds(Long[] announcementIds)
    {
        return announcementMapper.deleteAnnouncementByAnnouncementIds(announcementIds);
    }

    /**
     * 删除公告管理信息
     * 
     * @param announcementId 公告管理主键
     * @return 结果
     */
    @Override
    public int deleteAnnouncementByAnnouncementId(Long announcementId)
    {
        return announcementMapper.deleteAnnouncementByAnnouncementId(announcementId);
    }
}
