package com.guet.manage.mapper;

import java.util.List;
import com.guet.manage.domain.vo.Club;
import com.guet.manage.domain.vo.ClubLeaderVo;
import com.guet.manage.domain.vo.ClubVo;
import com.guet.manage.domain.vo.UserVo;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

/**
 * 社团管理Mapper接口
 * 
 * @author kevin
 * @date 2025-04-21
 */
public interface ClubMapper 
{
    /**
     * 查询社团管理
     * 
     * @param clubId 社团管理主键
     * @return 社团管理
     */
    public Club selectClubByClubId(Long clubId);

    /**
     * 查询社团管理列表
     * 
     * @param club 社团管理
     * @return 社团管理集合
     */
    public List<Club> selectClubList(Club club);

    /**
     * 新增社团管理
     * 
     * @param club 社团管理
     * @return 结果
     */
    public int insertClub(Club club);

    /**
     * 修改社团管理
     * 
     * @param club 社团管理
     * @return 结果
     */
    public int updateClub(Club club);

    /**
     * 删除社团管理
     * 
     * @param clubId 社团管理主键
     * @return 结果
     */
    public int deleteClubByClubId(Long clubId);

    /**
     * 批量删除社团管理
     * 
     * @param clubIds 需要删除的数据主键集合
     * @return 结果
     */
    public int deleteClubByClubIds(Long[] clubIds);

    public List<ClubVo> selectClubVoList(Club club);
    /**
     * 根据社团ID查询社团人员信息
     *
     * @Param clubId 社团ID
     * @return 社团成员集合
     */
    public List<UserVo> selectUserVoListByClubId(@Param("clubId") Long clubId);

    /**
     * 查询所有社团负责人名称
     *
     */
    public List<ClubLeaderVo> selectAllClubLeader();
    // ClubMapper.java
    @Select("SELECT COUNT(*) FROM tb_club WHERE name = #{name}")
    int countClubByName(String name);
}
