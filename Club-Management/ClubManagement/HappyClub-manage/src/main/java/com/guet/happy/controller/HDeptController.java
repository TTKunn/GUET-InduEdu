package com.guet.happy.controller;

import com.guet.common.core.domain.AjaxResult;
import com.guet.happy.domain.HDept;
import com.guet.happy.service.HDeptService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;


@RestController
@RequestMapping("happy/dept")
public class HDeptController {

    @Autowired
    private HDeptService deptService;

    @GetMapping("/list")
    public AjaxResult getDeptList() {
        return AjaxResult.success(deptService.getDeptList());
    }
}
