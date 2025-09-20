package com.guet.manage.service;

import java.util.List;
import com.guet.manage.domain.MCategory;

/**
 * 社团分类管理Service接口
 * 
 * @author kevin
 * @date 2025-04-21
 */
public interface ICategoryService 
{
    /**
     * 查询社团分类管理
     * 
     * @param categoryId 社团分类管理主键
     * @return 社团分类管理
     */
    public MCategory selectCategoryByCategoryId(Long categoryId);

    /**
     * 查询社团分类管理列表
     * 
     * @param MCategory 社团分类管理
     * @return 社团分类管理集合
     */
    public List<MCategory> selectCategoryList(MCategory MCategory);

    /**
     * 新增社团分类管理
     * 
     * @param MCategory 社团分类管理
     * @return 结果
     */
    public int insertCategory(MCategory MCategory);

    /**
     * 修改社团分类管理
     * 
     * @param MCategory 社团分类管理
     * @return 结果
     */
    public int updateCategory(MCategory MCategory);

    /**
     * 批量删除社团分类管理
     * 
     * @param categoryIds 需要删除的社团分类管理主键集合
     * @return 结果
     */
    public int deleteCategoryByCategoryIds(Long[] categoryIds);

    /**
     * 删除社团分类管理信息
     * 
     * @param categoryId 社团分类管理主键
     * @return 结果
     */
    public int deleteCategoryByCategoryId(Long categoryId);
}
