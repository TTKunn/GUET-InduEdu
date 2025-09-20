package com.guet.happy.service.Impl;

import com.guet.happy.domain.HClub;
import com.guet.happy.domain.HCategory;
import com.guet.happy.mapper.HClubMapper;
import com.guet.happy.service.HClubService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class HClubServiceImpl implements HClubService {

    @Autowired
    private HClubMapper clubMapper;

    /**
     * 查询社团列表，支持按分类ID过滤
     *
     * @param categoryId 分类ID（可为 null）
     * @return 社团列表
     */
    @Override
    public List<HClub> getClubList(Integer categoryId) {
        return clubMapper.selectClubList(categoryId);
    }

    /**
     * 获取所有社团分类
     *
     * @return 分类对象列表
     */
    @Override
    public List<HCategory> getAllCategories() {
        return clubMapper.selectAllCategories();
    }

    /**
     * 获取所有社团分类名称
     *
     * @return 分类名称列表
     */
    @Override
    public List<String> getClubCategoryNames() {
        return clubMapper.selectClubCategory();
    }

    // HClubServiceImpl.java
    @Override
    public HClub getClubById(Integer clubId) {
        return clubMapper.selectClubById(clubId);
    }

}
