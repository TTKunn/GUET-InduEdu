import request from '@/utils/request'
// 根据负责人id查询社团id
export function selectClubIdByUserId(userId) {
    return request({
      url: '/personal/club/selectClubIdByUserId',
      method: 'get',
      params: { userId }
    });
  }
  