package com.guet.personal.mapper;

import java.util.List;
import java.util.Map;

import com.guet.personal.domain.PersonalClub;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

/**
 * 社团信息Mapper接口
 * 
 * @author kevin
 * @date 2025-05-05
 */
public interface PersonalClubMapper 
{
    /**
     * 查询社团信息
     * 
     * @param clubId 社团信息主键
     * @return 社团信息
     */
    public PersonalClub selectPersonalClubByClubId(Long clubId);

    /**
     * 查询社团信息列表
     * 
     * @param personalClub 社团信息
     * @return 社团信息集合
     */
    public List<PersonalClub> selectPersonalClubList(PersonalClub personalClub);

    /**
     * 新增社团信息
     * 
     * @param personalClub 社团信息
     * @return 结果
     */
    public int insertPersonalClub(PersonalClub personalClub);

    /**
     * 修改社团信息
     * 
     * @param personalClub 社团信息
     * @return 结果
     */
    public int updatePersonalClub(PersonalClub personalClub);

    /**
     * 删除社团信息
     * 
     * @param clubId 社团信息主键
     * @return 结果
     */
    public int deletePersonalClubByClubId(Long clubId);

    /**
     * 批量删除社团信息
     * 
     * @param clubIds 需要删除的数据主键集合
     * @return 结果
     */
    public int deletePersonalClubByClubIds(Long[] clubIds);

    // 在PersonalClubMapper.java中增加方法
    @Select("SELECT c.club_id, c.name AS club_name, " +
            "COUNT(DISTINCT m.user_id) AS member_count, " +
            "COUNT(DISTINCT a.achievement_id) AS achievement_count " +
            "FROM tb_club c " +
            "LEFT JOIN tb_membership m ON c.club_id = m.club_id AND m.deleted_at IS NULL " +
            "LEFT JOIN tb_achievement a ON c.club_id = a.club_id AND a.deleted_at IS NULL " +
            "WHERE c.club_id = #{clubId} AND c.deleted_at IS NULL " +
            "GROUP BY c.club_id, c.name")
    Map<String, Object> selectClubStatistics(@Param("clubId") Long clubId);
}
