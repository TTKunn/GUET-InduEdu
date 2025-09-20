package com.guet.happy.mapper;

import com.guet.happy.domain.Notice;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import java.util.List;

@Mapper
public interface NoticeMapper {

    /**
     * 查询公开公告
     */
    List<Notice> selectPublicNotice();

    /**
     * 根据 ID 查询公告
     */
    Notice selectNoticeById(@Param("announcementId") Integer announcementId);
    /**
     * 根据社团ID查询所有内部公告
     */
    List<Notice> selectInnerNoticeByClubId(Long clubId);

    List<Notice> selectPublicNoticeByClubId(Long clubId);
}
