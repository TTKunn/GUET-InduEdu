package com.guet.personal.service;

import java.util.List;

import com.guet.personal.domain.Dto.PersonalAnnouncementDto;
import com.guet.personal.domain.PersonalAnnouncement;

/**
 * 公告管理Service接口
 * 
 * @author kevin
 * @date 2025-05-01
 */
public interface IPersonalAnnouncementService
{
    /**
     * 查询公告管理
     * 
     * @param announcementId 公告管理主键
     * @return 公告管理
     */
    public PersonalAnnouncement selectPannouncementByAnnouncementId(Long announcementId);

    /**
     * 查询公告管理列表
     * 
     * @param pannouncement 公告管理
     * @return 公告管理集合
     */
    public List<PersonalAnnouncement> selectPannouncementList(PersonalAnnouncementDto pannouncement);

    /**
     * 新增公告管理
     * 
     * @param personalAnnouncement 公告管理
     * @return 结果
     */
    public int insertPannouncement(PersonalAnnouncement personalAnnouncement);

    /**
     * 修改公告管理
     * 
     * @param personalAnnouncement 公告管理
     * @return 结果
     */
    public int updatePannouncement(PersonalAnnouncement personalAnnouncement);

    /**
     * 批量删除公告管理
     * 
     * @param announcementIds 需要删除的公告管理主键集合
     * @return 结果
     */
    public int deletePannouncementByAnnouncementIds(Long[] announcementIds);

    /**
     * 删除公告管理信息
     * 
     * @param announcementId 公告管理主键
     * @return 结果
     */
    public int deletePannouncementByAnnouncementId(Long announcementId);
}
