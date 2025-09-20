package com.guet.happy.service;

import com.guet.happy.domain.HClub;
import com.guet.happy.domain.HCategory;

import java.util.List;

public interface HClubService {

    /**
     * 查询社团列表，支持按分类ID过滤
     *
     * @param categoryId 分类ID（可为null）
     * @return 社团列表
     */
    List<HClub> getClubList(Integer categoryId);

    /**
     * 获取所有社团分类
     *
     * @return 分类列表
     */
    List<HCategory> getAllCategories();

    /**
     * 获取所有社团分类名称
     *
     * @return 分类名称列表
     */
    List<String> getClubCategoryNames();

    // HClubService.java
    HClub getClubById(Integer clubId);

}
