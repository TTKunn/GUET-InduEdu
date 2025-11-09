import request from '@/utils/request'

// 查询成果管理列表
export function listAchievement(query) {
  return request({
    url: '/manage/achievement/list',
    method: 'get',
    params: query
  })
}

// 查询成果管理详细
export function getAchievement(achievementId) {
  return request({
    url: '/manage/achievement/' + achievementId,
    method: 'get'
  })
}

// 新增成果管理
export function addAchievement(data) {
  return request({
    url: '/manage/achievement',
    method: 'post',
    data: data
  })
}

// 修改成果管理
export function updateAchievement(data) {
  return request({
    url: '/manage/achievement',
    method: 'put',
    data: data
  })
}

// 删除成果管理
export function delAchievement(achievementId) {
  return request({
    url: '/manage/achievement/' + achievementId,
    method: 'delete'
  })
}
