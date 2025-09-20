package com.guet.manage.controller;

import java.util.List;
import javax.servlet.http.HttpServletResponse;

import com.guet.manage.domain.MCategory;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import com.guet.common.annotation.Log;
import com.guet.common.core.controller.BaseController;
import com.guet.common.core.domain.AjaxResult;
import com.guet.common.enums.BusinessType;
import com.guet.manage.service.ICategoryService;
import com.guet.common.utils.poi.ExcelUtil;
import com.guet.common.core.page.TableDataInfo;

/**
 * 社团分类管理Controller
 * 
 * @author kevin
 * @date 2025-04-21
 */
@RestController
@RequestMapping("/manage/category")
public class CategoryController extends BaseController
{
    @Autowired
    private ICategoryService categoryService;

    /**
     * 查询社团分类管理列表
     */
    // @PreAuthorize("@ss.hasPermi('manage:category:list')")
    @GetMapping("/list")
    public TableDataInfo list(MCategory MCategory)
    {
        startPage();
        List<MCategory> list = categoryService.selectCategoryList(MCategory);
        return getDataTable(list);
    }

    /**
     * 导出社团分类管理列表
     */
    // @PreAuthorize("@ss.hasPermi('manage:category:export')")
    @Log(title = "社团分类管理", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, MCategory MCategory)
    {
        List<MCategory> list = categoryService.selectCategoryList(MCategory);
        ExcelUtil<MCategory> util = new ExcelUtil<MCategory>(MCategory.class);
        util.exportExcel(response, list, "社团分类管理数据");
    }

    /**
     * 获取社团分类管理详细信息
     */
    // @PreAuthorize("@ss.hasPermi('manage:category:query')")
    @GetMapping(value = "/{categoryId}")
    public AjaxResult getInfo(@PathVariable("categoryId") Long categoryId)
    {
        return success(categoryService.selectCategoryByCategoryId(categoryId));
    }

    /**
     * 新增社团分类管理
     */
    // @PreAuthorize("@ss.hasPermi('manage:category:add')")
    @Log(title = "社团分类管理", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody MCategory MCategory)
    {
        return toAjax(categoryService.insertCategory(MCategory));
    }

    /**
     * 修改社团分类管理
     */
    // @PreAuthorize("@ss.hasPermi('manage:category:edit')")
    @Log(title = "社团分类管理", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody MCategory MCategory)
    {
        return toAjax(categoryService.updateCategory(MCategory));
    }

    /**
     * 删除社团分类管理
     */
    // @PreAuthorize("@ss.hasPermi('manage:category:remove')")
    @Log(title = "社团分类管理", businessType = BusinessType.DELETE)
	@DeleteMapping("/{categoryIds}")
    public AjaxResult remove(@PathVariable Long[] categoryIds)
    {
        return toAjax(categoryService.deleteCategoryByCategoryIds(categoryIds));
    }
}
