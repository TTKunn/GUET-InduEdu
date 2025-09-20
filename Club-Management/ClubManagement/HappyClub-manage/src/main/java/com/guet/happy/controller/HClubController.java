package com.guet.happy.controller;

import com.guet.common.core.domain.AjaxResult;
import com.guet.happy.domain.HClub;
import com.guet.happy.domain.HCategory;
import com.guet.happy.service.HClubService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/happy")
public class HClubController {

    @Autowired
    private HClubService clubService;

    /**
     * 获取社团列表（支持按分类ID过滤）
     * 示例：/happy/club/list?categoryId=1
     */
    @GetMapping("/club/list")
    public AjaxResult getClubList(@RequestParam(required = false) Integer categoryId) {
        return AjaxResult.success(clubService.getClubList(categoryId));
    }

    /**
     * 获取所有社团分类
     * 示例：/happy/category/list
     */
    @GetMapping("/category/list")
    public AjaxResult getAllCategories() {
        return AjaxResult.success(clubService.getAllCategories());
    }

    /**
     * 获取所有社团分类名称
     * 示例：/happy/category/names
     */
    @GetMapping("/category/names")
    public AjaxResult getClubCategoryNames() {
        return AjaxResult.success(clubService.getClubCategoryNames());
    }

    // HClubController.java
    @GetMapping("/club/detail/{clubId}")
    public AjaxResult getClubDetail(@PathVariable Integer clubId) {
        return AjaxResult.success(clubService.getClubById(clubId));
    }

}
