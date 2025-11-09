import request from '@/utils/request'

// 查询社团信息列表
export function listPersonalClub(query) {
  return request({
    url: '/personal/PersonalClub/list',
    method: 'get',
    params: query
  })
}

// 查询社团信息详细
export function getPersonalClub(clubId) {
  return request({
    url: '/personal/PersonalClub/' + clubId,
    method: 'get'
  })
}

// 新增社团信息
export function addPersonalClub(data) {
  return request({
    url: '/personal/PersonalClub',
    method: 'post',
    data: data
  })
}

// 修改社团信息
export function updatePersonalClub(data) {
  return request({
    url: '/personal/PersonalClub',
    method: 'put',
    data: data
  })
}

// 删除社团信息
export function delPersonalClub(clubId) {
  return request({
    url: '/personal/PersonalClub/' + clubId,
    method: 'delete'
  })
}
