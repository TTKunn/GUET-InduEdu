import request from '@/utils/request'

// 查询考勤管理列表
export function listAttendance(query) {
  return request({
    url: '/personal/attendance/list',
    method: 'get',
    params: query
  })
}

// 查询考勤管理详细
export function getAttendance(attendanceId) {
  return request({
    url: '/personal/attendance/' + attendanceId,
    method: 'get'
  })
}

// 新增考勤管理
export function addAttendance(data) {
  return request({
    url: '/personal/attendance',
    method: 'post',
    data: data
  })
}

// 修改考勤管理
export function updateAttendance(data) {
  return request({
    url: '/personal/attendance',
    method: 'put',
    data: data
  })
}

// 删除考勤管理
export function delAttendance(attendanceId) {
  return request({
    url: '/personal/attendance/' + attendanceId,
    method: 'delete'
  })
}
