import request from '@/utils/request'

// 查询活动管理列表
export function listActivity(query) {
  return request({
    url: '/personal/activity/list',
    method: 'get',
    params: query
  })
}

// 查询活动管理详细
export function getActivity(activityId) {
  return request({
    url: '/personal/activity/' + activityId,
    method: 'get'
  })
}

// 新增活动管理
export function addActivity(data) {
  return request({
    url: '/personal/activity',
    method: 'post',
    data: data
  })
}

// 修改活动管理
export function updateActivity(data) {
  return request({
    url: '/personal/activity',
    method: 'put',
    data: data
  })
}

// 删除活动管理
export function delActivity(activityId) {
  return request({
    url: '/personal/activity/' + activityId,
    method: 'delete'
  })
}
