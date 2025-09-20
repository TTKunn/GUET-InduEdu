package com.guet.personal.service.impl.Announcement;

import java.util.List;
import java.util.Objects;

import com.guet.personal.domain.Dto.Audit.PersonalAnnouncementAuditDto;
import com.guet.personal.domain.Dto.PersonalAnnouncementDto;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.guet.personal.mapper.PersonalAnnouncementMapper;
import com.guet.personal.domain.PersonalAnnouncement;
import com.guet.personal.service.IPersonalAnnouncementService;

/**
 * 公告管理Service业务层处理
 * 
 * @author kevin
 * @date 2025-05-01
 */
@Service
public class PersonalAnnouncementServiceImpl implements IPersonalAnnouncementService
{
    @Autowired
    private PersonalAnnouncementMapper personalAnnouncementMapper;

    /**
     * 查询公告管理
     * 
     * @param announcementId 公告管理主键
     * @return 公告管理
     */
    @Override
    public PersonalAnnouncement selectPannouncementByAnnouncementId(Long announcementId)
    {
        String type = personalAnnouncementMapper.selectPannouncementTypeByAnnouncementId(announcementId);

        if (Objects.equals(type, "public")){
            return personalAnnouncementMapper.selectPublicPannouncementByAnnouncementId(announcementId);
        }
        else {
            return personalAnnouncementMapper.selectInternalPannouncementByAnnouncementId(announcementId);
        }
    }

    /**
     * 查询公告管理列表
     * 
     * @param pannouncement 公告管理
     * @return 公告管理
     */
    @Override
    public List<PersonalAnnouncement> selectPannouncementList(PersonalAnnouncementDto pannouncement)
    {
        if(Objects.equals(pannouncement.getType(), "public")){
            return personalAnnouncementMapper.selectPublicPannouncementList(pannouncement);
        }
        else{
            return personalAnnouncementMapper.selectInternalPannouncementList(pannouncement);
        }
    }

    /**
     * 新增公告管理
     * 
     * @param personalAnnouncement 公告管理
     * @return 结果
     */
    @Override
    public int insertPannouncement(PersonalAnnouncement personalAnnouncement)
    {
        if (Objects.equals(personalAnnouncement.getType(), "public")){
            // 构建审核记录对象
            PersonalAnnouncementAuditDto pannouncementAudit = new PersonalAnnouncementAuditDto();

            personalAnnouncementMapper.insertPannouncement(personalAnnouncement);
            Long generatedId = personalAnnouncement.getAnnouncementId();
            // 赋值审核记录对象
            pannouncementAudit.setAnnouncementId(generatedId);
            pannouncementAudit.setApplicantId(personalAnnouncement.getPublisherId());
            pannouncementAudit.setType("announcement");
            pannouncementAudit.setStatus("pending");
            // 插入审核记录
            return personalAnnouncementMapper.insertPannouncementAudit(pannouncementAudit);
        }
        else {
            personalAnnouncement.setStatus("published");
            personalAnnouncementMapper.insertPannouncement(personalAnnouncement);
            Long generatedId = personalAnnouncement.getAnnouncementId();
            // 插入活动可见性记录 仅本社团可见
            return personalAnnouncementMapper.insertAnnouncementVisibility(generatedId, personalAnnouncement.getClubId());
        }
    }

    /**
     * 修改公告管理
     * 
     * @param personalAnnouncement 公告管理
     * @return 结果
     */
    @Override
    public int updatePannouncement(PersonalAnnouncement personalAnnouncement)
    {
        return personalAnnouncementMapper.updatePannouncement(personalAnnouncement);
    }

    /**
     * 批量删除公告管理
     * 
     * @param announcementIds 需要删除的公告管理主键
     * @return 结果
     */
    @Override
    public int deletePannouncementByAnnouncementIds(Long[] announcementIds)
    {
        return personalAnnouncementMapper.deletePannouncementByAnnouncementIds(announcementIds);
    }

    /**
     * 删除公告管理信息
     * 
     * @param announcementId 公告管理主键
     * @return 结果
     */
    @Override
    public int deletePannouncementByAnnouncementId(Long announcementId)
    {
        return personalAnnouncementMapper.deletePannouncementByAnnouncementId(announcementId);
    }
}
