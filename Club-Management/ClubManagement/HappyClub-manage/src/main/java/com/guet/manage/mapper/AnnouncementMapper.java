package com.guet.manage.mapper;

import java.util.List;
import com.guet.manage.domain.Announcement;
import com.guet.manage.domain.dto.AnnouncementDto;

/**
 * 公告管理Mapper接口
 * 
 * @author kevin
 * @date 2025-04-30
 */
public interface AnnouncementMapper 
{
    /**
     * 查询公告管理
     * 
     * @param announcementId 公告管理主键
     * @return 公告管理
     */
    public Announcement selectAnnouncementByAnnouncementId(Long announcementId);

    /**
     * 查询公告管理列表
     * 
     * @param announcement 公告管理
     * @return 公告管理集合
     */
    public List<Announcement> selectAnnouncementList(AnnouncementDto announcement);

    /**
     * 新增公告管理
     * 
     * @param announcement 公告管理
     * @return 结果
     */
    public int insertAnnouncement(Announcement announcement);

    /**
     * 修改公告管理
     * 
     * @param announcement 公告管理
     * @return 结果
     */
    public int updateAnnouncement(Announcement announcement);

    /**
     * 删除公告管理
     * 
     * @param announcementId 公告管理主键
     * @return 结果
     */
    public int deleteAnnouncementByAnnouncementId(Long announcementId);

    /**
     * 批量删除公告管理
     * 
     * @param announcementIds 需要删除的数据主键集合
     * @return 结果
     */
    public int deleteAnnouncementByAnnouncementIds(Long[] announcementIds);
}
