import request from '@/utils/request'

// 查询社团管理列表
export function listClub(query) {
  return request({
    url: '/manage/club/list',
    method: 'get',
    params: query
  })
}

// 查询社团管理详细
export function getClub(clubId) {
  return request({
    url: '/manage/club/' + clubId,
    method: 'get'
  })
}

// 新增社团管理
export function addClub(data) {
  return request({
    url: '/manage/club',
    method: 'post',
    data: data
  })
}

// 修改社团管理
export function updateClub(data) {
  return request({
    url: '/manage/club',
    method: 'put',
    data: data
  })
}

// 删除社团管理
export function delClub(clubId) {
  return request({
    url: '/manage/club/' + clubId,
    method: 'delete'
  })
}

// 根据社团id查询社团成员列表
export function listMember(clubId) {
  return request({
    url: '/manage/club/listMember/' + clubId,
    method: 'get',
  })
}

// 获取社团负责人列表
export function listLeaderName() {
  return request({
    url: '/manage/club/clubLeader',
    method: 'get',
  })
}