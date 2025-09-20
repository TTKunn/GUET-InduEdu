package com.guet.happy.service.Impl;

import com.guet.happy.domain.HDept;
import com.guet.happy.mapper.HDeptMapper;
import com.guet.happy.service.HDeptService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class HDeptServiceImpl implements HDeptService {

    @Autowired
    private HDeptMapper deptMapper;

    @Override
    public List<HDept> getDeptList() {
        return deptMapper.selectDeptList();
    }
}
