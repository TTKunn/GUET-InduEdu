package com.guet.personal.service;

import java.util.List;
import com.guet.personal.domain.PClub;

/**
 * 社团信息Service接口
 * 
 * @author kevin
 * @date 2025-05-05
 */
public interface IPClubService 
{
    /**
     * 查询社团信息
     * 
     * @param clubId 社团信息主键
     * @return 社团信息
     */
    public PClub selectPClubByClubId(Long clubId);

    /**
     * 查询社团信息列表
     * 
     * @param pClub 社团信息
     * @return 社团信息集合
     */
    public List<PClub> selectPClubList(PClub pClub);

    /**
     * 新增社团信息
     * 
     * @param pClub 社团信息
     * @return 结果
     */
    public int insertPClub(PClub pClub);

    /**
     * 修改社团信息
     * 
     * @param pClub 社团信息
     * @return 结果
     */
    public int updatePClub(PClub pClub);

    /**
     * 批量删除社团信息
     * 
     * @param clubIds 需要删除的社团信息主键集合
     * @return 结果
     */
    public int deletePClubByClubIds(Long[] clubIds);

    /**
     * 删除社团信息信息
     * 
     * @param clubId 社团信息主键
     * @return 结果
     */
    public int deletePClubByClubId(Long clubId);
}
