package com.guet.personal.service;

import java.util.List;
import com.guet.personal.domain.PersonalClub;

/**
 * 社团信息Service接口
 * 
 * @author kevin
 * @date 2025-05-05
 */
public interface IPersonalClubService 
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
     * 批量删除社团信息
     * 
     * @param clubIds 需要删除的社团信息主键集合
     * @return 结果
     */
    public int deletePersonalClubByClubIds(Long[] clubIds);

    /**
     * 删除社团信息信息
     * 
     * @param clubId 社团信息主键
     * @return 结果
     */
    public int deletePersonalClubByClubId(Long clubId);
}
