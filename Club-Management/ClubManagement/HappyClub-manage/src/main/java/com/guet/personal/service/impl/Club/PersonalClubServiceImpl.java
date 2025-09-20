package com.guet.personal.service.impl.Club;

import java.util.List;
import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.guet.personal.mapper.PersonalClubMapper;
import com.guet.personal.domain.PersonalClub;
import com.guet.personal.service.IPersonalClubService;

import javax.annotation.Resource;

/**
 * 社团信息Service业务层处理
 * 
 * @author kevin
 * @date 2025-05-05
 */
@Service
public class PersonalClubServiceImpl implements IPersonalClubService 
{
    @Resource
    private PersonalClubMapper personalClubMapper;

    /**
     * 查询社团信息
     * 
     * @param clubId 社团信息主键
     * @return 社团信息
     */
    @Override
    public PersonalClub selectPersonalClubByClubId(Long clubId)
    {
        return personalClubMapper.selectPersonalClubByClubId(clubId);
    }

    /**
     * 查询社团信息列表
     * 
     * @param personalClub 社团信息
     * @return 社团信息
     */
    @Override
    public List<PersonalClub> selectPersonalClubList(PersonalClub personalClub) {
        // 1. 获取原始社团列表
        List<PersonalClub> clubList = personalClubMapper.selectPersonalClubList(personalClub);

        // // 检查是否查询到社团
        // if (clubList != null && !clubList.isEmpty()) {
        //     // 2. 只处理第一个社团（假设只有一个）
        //     PersonalClub club = clubList.get(0);
        //
        //     // 3. 查询该社团的统计信息
        //     Map<String, Object> statistics = personalClubMapper.selectClubStatistics(club.getClubId());
        //
        //     // 4. 设置统计信息
        //     if (statistics != null) {
        //         club.setMemberCount((Long) statistics.get("member_count"));
        //         club.setAchievementCount((Long) statistics.get("achievement_count"));
        //     } else {
        //         club.setMemberCount(0L);
        //         club.setAchievementCount(0L);
        //     }
        // }

        return clubList;
    }

    /**
     * 新增社团信息
     * 
     * @param personalClub 社团信息
     * @return 结果
     */
    @Override
    public int insertPersonalClub(PersonalClub personalClub)
    {
        return personalClubMapper.insertPersonalClub(personalClub);
    }

    /**
     * 修改社团信息
     * 
     * @param personalClub 社团信息
     * @return 结果
     */
    @Override
    public int updatePersonalClub(PersonalClub personalClub)
    {
        return personalClubMapper.updatePersonalClub(personalClub);
    }

    /**
     * 批量删除社团信息
     * 
     * @param clubIds 需要删除的社团信息主键
     * @return 结果
     */
    @Override
    public int deletePersonalClubByClubIds(Long[] clubIds)
    {
        return personalClubMapper.deletePersonalClubByClubIds(clubIds);
    }

    /**
     * 删除社团信息信息
     * 
     * @param clubId 社团信息主键
     * @return 结果
     */
    @Override
    public int deletePersonalClubByClubId(Long clubId)
    {
        return personalClubMapper.deletePersonalClubByClubId(clubId);
    }
}
