package com.guet.manage.service.impl;

import java.util.List;

import com.guet.manage.domain.MCategory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.guet.manage.mapper.CategoryMapper;
import com.guet.manage.service.ICategoryService;

/**
 * 社团分类管理Service业务层处理
 * 
 * @author kevin
 * @date 2025-04-21
 */
@Service
public class CategoryServiceImpl implements ICategoryService 
{
    @Autowired
    private CategoryMapper categoryMapper;

    /**
     * 查询社团分类管理
     * 
     * @param categoryId 社团分类管理主键
     * @return 社团分类管理
     */
    @Override
    public MCategory selectCategoryByCategoryId(Long categoryId)
    {
        return categoryMapper.selectCategoryByCategoryId(categoryId);
    }

    /**
     * 查询社团分类管理列表
     * 
     * @param MCategory 社团分类管理
     * @return 社团分类管理
     */
    @Override
    public List<MCategory> selectCategoryList(MCategory MCategory)
    {
        return categoryMapper.selectCategoryList(MCategory);
    }

    /**
     * 新增社团分类管理
     * 
     * @param MCategory 社团分类管理
     * @return 结果
     */
    @Override
    public int insertCategory(MCategory MCategory)
    {
        return categoryMapper.insertCategory(MCategory);
    }

    /**
     * 修改社团分类管理
     * 
     * @param MCategory 社团分类管理
     * @return 结果
     */
    @Override
    public int updateCategory(MCategory MCategory)
    {
        return categoryMapper.updateCategory(MCategory);
    }

    /**
     * 批量删除社团分类管理
     * 
     * @param categoryIds 需要删除的社团分类管理主键
     * @return 结果
     */
    @Override
    public int deleteCategoryByCategoryIds(Long[] categoryIds)
    {
        return categoryMapper.deleteCategoryByCategoryIds(categoryIds);
    }

    /**
     * 删除社团分类管理信息
     * 
     * @param categoryId 社团分类管理主键
     * @return 结果
     */
    @Override
    public int deleteCategoryByCategoryId(Long categoryId)
    {
        return categoryMapper.deleteCategoryByCategoryId(categoryId);
    }
}
