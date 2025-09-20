package com.guet.happy.mapper;

import com.guet.happy.domain.HClub;
import com.guet.happy.domain.HCategory;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;

@Mapper
public interface HClubMapper {

    List<HClub> selectClubList(@Param("categoryId") Integer categoryId);

    List<HCategory> selectAllCategories();

    List<String> selectClubCategory();

    HClub selectClubById(Integer clubId);
}
