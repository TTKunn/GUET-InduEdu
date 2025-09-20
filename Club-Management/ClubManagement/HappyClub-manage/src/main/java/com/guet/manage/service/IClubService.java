package com.guet.manage.service;

import java.util.List;
import com.guet.manage.domain.vo.Club;
import com.guet.manage.domain.vo.ClubLeaderVo;
import com.guet.manage.domain.vo.ClubVo;
import com.guet.manage.domain.vo.UserVo;

/**
 * 社团管理Service接口
 * 
 * @author kevin
 * @date 2025-04-21
 */
public interface IClubService 
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
     * 批量删除社团管理
     * 
     * @param clubIds 需要删除的社团管理主键集合
     * @return 结果
     */
    public int deleteClubByClubIds(Long[] clubIds);

    /**
     * 删除社团管理信息
     * 
     * @param clubId 社团管理主键
     * @return 结果
     */
    public int deleteClubByClubId(Long clubId);

    /**
     * 查询社团管理列表
     * @param club
     * @return clubVo集合
     */
    public List<ClubVo> selectClubVoList(Club club);

    public List<UserVo> selectUserVoListByClubId(Long clubId);
    /**
     * 查询所有社团负责人名称
     */
    public List<ClubLeaderVo> selectAllClubLeader();
}
