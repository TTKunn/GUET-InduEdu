package com.guet.personal.mapper;

import java.util.List;

import com.guet.personal.domain.Dto.Audit.PersonalAnnouncementAuditDto;
import com.guet.personal.domain.Dto.PersonalAnnouncementDto;
import com.guet.personal.domain.PersonalAnnouncement;
import org.apache.ibatis.annotations.Param;

/**
 * 公告管理Mapper接口
 * 
 * @author kevin
 * @date 2025-05-01
 */
public interface PersonalAnnouncementMapper
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
    // public List<Pannouncement> selectPannouncementList(PannouncementDto pannouncement);

    /**
     * 新增公告管理
     * 
     * @param personalAnnouncement 公告管理
     * @return 结果
     */
    public int insertPannouncement(PersonalAnnouncement personalAnnouncement);

    // public int insertInternalPersonalAnnouncement(PersonalAnnouncement personalAnnouncement);

    // public int insertPublicPersonalAnnouncement(PersonalAnnouncement personalAnnouncement);

    /**
     * 修改公告管理
     * 
     * @param personalAnnouncement 公告管理
     * @return 结果
     */
    public int updatePannouncement(PersonalAnnouncement personalAnnouncement);

    /**
     * 删除公告管理
     * 
     * @param announcementId 公告管理主键
     * @return 结果
     */
    public int deletePannouncementByAnnouncementId(Long announcementId);

    /**
     * 批量删除公告管理
     * 
     * @param announcementIds 需要删除的数据主键集合
     * @return 结果
     */
    public int deletePannouncementByAnnouncementIds(Long[] announcementIds);
    /**
     * 查询公开公公告管理列表
     *
     * @param pannouncement 公告管理
     * @return 公开公告管理集合
     */
    public List<PersonalAnnouncement> selectPublicPannouncementList(PersonalAnnouncementDto pannouncement);
    /**
     * 查询内部公告管理列表
     *
     * @param pannouncement 公告管理
     * @return 内部公告管理集合
     */
    public List<PersonalAnnouncement> selectInternalPannouncementList(PersonalAnnouncementDto pannouncement);

    public String selectPannouncementTypeByAnnouncementId(Long announcementId);

    public PersonalAnnouncement selectPublicPannouncementByAnnouncementId(Long announcementId);
    public PersonalAnnouncement selectInternalPannouncementByAnnouncementId(Long announcementId);

    int insertPannouncementAudit(PersonalAnnouncementAuditDto pannouncementAudit);

    int insertAnnouncementVisibility(@Param("announcementId") Long generatedId,@Param("clubId") Long clubId);
}
