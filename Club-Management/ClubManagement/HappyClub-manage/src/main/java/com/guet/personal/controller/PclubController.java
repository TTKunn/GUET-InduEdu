package com.guet.personal.controller;

import com.guet.common.core.controller.BaseController;
import com.guet.personal.service.PclubService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import javax.annotation.Resource;

@RestController
@RequestMapping("/personal/club")
public class PclubController extends BaseController {
//  根据社团负责人id查询社团id
    @Resource
    private PclubService pclubService;
    @GetMapping("/selectClubIdByUserId")
    public Long selectClubIdByUserId(@RequestParam Long userId){
        return pclubService.selectClubIdByUserId(userId);
    }
}
