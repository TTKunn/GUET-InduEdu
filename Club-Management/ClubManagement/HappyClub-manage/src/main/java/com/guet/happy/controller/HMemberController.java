package com.guet.happy.controller;

import com.guet.common.core.domain.AjaxResult;
import com.guet.happy.domain.HMember;
import com.guet.happy.domain.MemberRequest;
import com.guet.happy.service.HMemberService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("happy/members")
public class HMemberController {

    @Autowired
    private HMemberService hMemberService;

    @GetMapping("/user/{userId}")
    public HMember getMemberByUserId(@PathVariable Integer userId) {
        return hMemberService.getMemberByUserId(userId);
    }

    @GetMapping("/club/{clubId}")
    public AjaxResult getMembersByClubId(@PathVariable Integer clubId) {
        return AjaxResult.success(hMemberService.getMembersByClubId(clubId));
    }

    @GetMapping("/check")
    public boolean checkMember(@RequestParam Integer userId, @RequestParam Integer clubId) {
        return hMemberService.isMember(userId, clubId);
    }

    @PostMapping("/join")
    public AjaxResult join(@RequestBody MemberRequest request) {
        return AjaxResult.success(hMemberService.joinClub(request.getUserId(), request.getClubId(), request.getRemark()));
    }

    @PostMapping("/quit")
    public AjaxResult quit(@RequestBody MemberRequest request) {
        return AjaxResult.success(hMemberService.quitClub(request.getUserId(), request.getClubId(), request.getRemark()));
    }

}
