import request from '@/utils/request'

// 查询社团成员关系列表
export function listMembership(query) {
  return request({
    url: '/personal/membership/list',
    method: 'get',
    params: query
  })
}

// 查询社团成员关系详细
export function getMembership(membershipId) {
  return request({
    url: '/personal/membership/' + membershipId,
    method: 'get'
  })
}

// 新增社团成员关系
export function addMembership(data) {
  return request({
    url: '/personal/membership',
    method: 'post',
    data: data
  })
}

// 修改社团成员关系
export function updateMembership(data) {
  return request({
    url: '/personal/membership',
    method: 'put',
    data: data
  })
}

// 删除社团成员关系
export function delMembership(membershipId) {
  return request({
    url: '/personal/membership/' + membershipId,
    method: 'delete'
  })
}

// 查询社团成员列表
export function listMembersByClubId(clubId) {
  return request({
    url: `/personal/membership/members/${clubId}`,
    method: 'get'
  })
}

// 查看成员拥有的的果
export function listAchievementsByMemberId(memberId) {
  return request({
    url: `/personal/membership/achievements/${memberId}`,
    method: 'get'
  })
}

//查看成员的参加的活动
export function listActivitiesByMemberId(memberId) {
  return request({
    url: `/personal/membership/activities/${memberId}`,
    method: 'get'
  })
}