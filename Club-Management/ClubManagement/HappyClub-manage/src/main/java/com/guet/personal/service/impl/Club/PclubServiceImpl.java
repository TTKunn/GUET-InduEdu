package com.guet.personal.service.impl.Club;

import com.guet.personal.mapper.PclubMapper;
import com.guet.personal.service.PclubService;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;

@Service
public class PclubServiceImpl implements PclubService {
    @Resource
    private PclubMapper pclubMapper;
    @Override
    public Long selectClubIdByUserId(Long userId) {
        return pclubMapper.selectClubIdByUserId(userId);
    }
}
