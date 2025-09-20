package com.guet.manage.service.impl;

import java.util.List;

import com.guet.manage.domain.vo.ClubLeaderVo;
import com.guet.manage.domain.vo.ClubVo;
import com.guet.manage.domain.vo.UserVo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.guet.manage.mapper.ClubMapper;
import com.guet.manage.domain.vo.Club;
import com.guet.manage.service.IClubService;

/**
 * 社团管理Service业务层处理
 * 
 * @author kevin
 * @date 2025-04-21
 */
@Service
public class ClubServiceImpl implements IClubService
{
    @Autowired
    private ClubMapper clubMapper;

    /**
     * 查询社团管理
     * 
     * @param clubId 社团管理主键
     * @return 社团管理
     */
    @Override
    public Club selectClubByClubId(Long clubId)
    {
        return clubMapper.selectClubByClubId(clubId);
    }

    /**
     * 查询社团管理列表
     * 
     * @param club 社团管理
     * @return 社团管理
     */
    @Override
    public List<Club> selectClubList(Club club)
    {
        return clubMapper.selectClubList(club);
    }

    /**
     * 新增社团管理
     * 
     * @param club 社团管理
     * @return 结果
     */
    @Override
    public int insertClub(Club club)
    {
        if (clubMapper.countClubByName(club.getName()) > 0) {
            throw new RuntimeException("社团名称已存在：" + club.getName());
        }
        return clubMapper.insertClub(club);
    }

    /**
     * 修改社团管理
     * 
     * @param club 社团管理
     * @return 结果
     */
    @Override
    public int updateClub(Club club)
    {
        return clubMapper.updateClub(club);
    }

    /**
     * 批量删除社团管理
     * 
     * @param clubIds 需要删除的社团管理主键
     * @return 结果
     */
    @Override
    public int deleteClubByClubIds(Long[] clubIds)
    {
        return clubMapper.deleteClubByClubIds(clubIds);
    }

    /**
     * 删除社团管理信息
     * 
     * @param clubId 社团管理主键
     * @return 结果
     */
    @Override
    public int deleteClubByClubId(Long clubId)
    {
        return clubMapper.deleteClubByClubId(clubId);
    }

    /**
     * 查询社团管理列表
     * @param club
     * @return
     */
    @Override
    public List<ClubVo> selectClubVoList(Club club) {
        return clubMapper.selectClubVoList(club);
    }

    @Override
    public List<UserVo> selectUserVoListByClubId(Long clubId) {
        return clubMapper.selectUserVoListByClubId(clubId);
    }

    @Override
    public List<ClubLeaderVo> selectAllClubLeader() {
        return clubMapper.selectAllClubLeader();
    }
}
