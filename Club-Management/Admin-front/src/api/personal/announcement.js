import request from '@/utils/request'

// 查询公告管理列表
export function listAnnouncement(query) {
  return request({
    url: '/personal/announcement/list',
    method: 'get',
    params: query
  })
}

// 查询公告管理详细
export function getAnnouncement(announcementId) {
  return request({
    url: '/personal/announcement/' + announcementId,
    method: 'get'
  })
}

// 新增公告管理
export function addAnnouncement(data) {
  return request({
    url: '/personal/announcement',
    method: 'post',
    data: data
  })
}

// 修改公告管理
export function updateAnnouncement(data) {
  return request({
    url: '/personal/announcement',
    method: 'put',
    data: data
  })
}

// 删除公告管理
export function delAnnouncement(announcementId) {
  return request({
    url: '/personal/announcement/' + announcementId,
    method: 'delete'
  })
}
