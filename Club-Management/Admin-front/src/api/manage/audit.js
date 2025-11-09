import request from '@/utils/request'

/**
 * 获取公告审核列表
 * @param {Object} query 查询参数
 * @param {string} [query.title] 公告标题（模糊查询）
 * @param {string} [query.clubName] 社团名称（精确查询）
 * @param {string} [query.status] 审核状态（pending/published/rejected）
 * @param {string} [query.beginTime] 开始时间（YYYY-MM-DD）
 * @param {string} [query.endTime] 结束时间（YYYY-MM-DD）
 * @returns {Promise} 包含公告审核列表的Promise对象
 */
export function listAuditAnnouncements(query) {
  return request({
    url: '/manage/audit/listAnnouncements',
    method: 'get',
    params: query
  })
}

/**
* 公告审核通过接口
* @param {Object} data 审核数据
* @param {number} data.auditId 审核记录ID（必填）
* @param {number} data.announcementId 公告ID（必填）
* @param {string} [data.remark] 审核备注（5-200字符）
* @param {number} data.processorId 处理人ID（必填）
* @returns {Promise} 包含操作结果的Promise对象
*/
export function approveAuditAnnouncement(data) {
  return request({
    url: '/manage/audit/approveAnnouncement',
    method: 'post',
    data: {
      auditId: data.auditId,
      announcementId: data.announcementId,
      remark: data.remark,
      processorId: data.processorId
    }
  })
}

/**
* 公告审核驳回接口
* @param {Object} data 审核数据
* @param {number} data.auditId 审核记录ID（必填）
* @param {number} data.announcementId 公告ID（必填）
* @param {string} data.remark 驳回原因（必填，5-200字符）
* @param {number} data.processorId 处理人ID（必填）
* @returns {Promise} 包含操作结果的Promise对象
*/
export function rejectAuditAnnouncement(data) {
  return request({
    url: '/manage/audit/rejectAnnouncement',
    method: 'post',
    data: {
      auditId: data.auditId,
      announcementId: data.announcementId,
      remark: data.remark,
      processorId: data.processorId
    }
  })
}

// ================== 活动审核API================== //

/**
* 获取活动审核列表
* @param {Object} query 查询参数
* @param {string} [query.activityName] 活动名称（模糊查询）
* @param {string} [query.clubName] 社团名称（精确查询）
* @param {string} [query.status] 审核状态（pending/approved/rejected/ongoing/completed）
* @param {string} [query.beginTime] 活动开始时间（YYYY-MM-DD）
* @param {string} [query.endTime] 活动结束时间（YYYY-MM-DD）
* @returns {Promise} 包含活动审核列表的Promise对象
*/
export function listAuditActivities(query) {
  return request({
    url: '/manage/audit/listActivities',
    method: 'get',
    params: query
  })
}

/**
* 活动审核通过接口
* @param {Object} data 审核数据
* @param {number} data.auditId 审核记录ID（必填）
* @param {number} data.activityId 活动ID（必填）
* @param {string} [data.remark] 审核备注（5-200字符）
* @param {number} data.processorId 处理人ID（必填）
* @returns {Promise} 包含操作结果的Promise对象
*/
export function approveAuditActivity(data) {
  return request({
    url: '/manage/audit/approveActivity',
    method: 'post',
    data: {
      auditId: data.auditId,
      activityId: data.activityId,
      remark: data.remark,
      processorId: data.processorId
    }
  })
}

/**
* 活动审核驳回接口
* @param {Object} data 审核数据
* @param {number} data.auditId 审核记录ID（必填）
* @param {number} data.activityId 活动ID（必填）
* @param {string} data.remark 驳回原因（必填，5-200字符）
* @param {number} data.processorId 处理人ID（必填）
* @returns {Promise} 包含操作结果的Promise对象
*/
export function rejectAuditActivity(data) {
  return request({
    url: '/manage/audit/rejectActivity',
    method: 'post',
    data: {
      auditId: data.auditId,
      activityId: data.activityId,
      remark: data.remark,
      processorId: data.processorId
    }
  })
}

// ================== 新社团审核API================== //

/**
* 获取新社团注册审核列表
* @param {Object} query 查询参数
* @param {string} [query.clubName] 社团名称（模糊查询）
* @param {string} [query.categoryId] 类别（精确查询）
* @param {string} [query.params] 申请时间范围（YYYY-MM-DD）
* @returns {Promise} 包含活动审核列表的Promise对象
*/
export function listAuditClub(query) {
  return request({
    url: 'manage/audit/listNewClub',
    method: 'get',
    params: query
  })
}
/**
* 新社团注册审核通过接口
* @param {Object} data 审核数据
* @param {number} data.auditId 审核记录ID（必填）
* @param {number} data.clubId 新社团ID（必填）
* @param {string} [data.remark] 审核备注（5-200字符）
* @param {number} data.processorId 处理人ID（必填）
* @returns {Promise} 包含操作结果的Promise对象
*/
export function approveAuditClub(data) {
  return request({
    url: '/manage/audit/approveNewClub',
    method: 'post',
    data: {
      auditId: data.auditId,
      clubId: data.clubId,
      remark: data.remark,
      processorId: data.processorId
    }
  })
}

/**
* 新社团注册审核驳回接口
* @param {Object} data 审核数据
* @param {number} data.auditId 审核记录ID（必填）
* @param {number} data.clubId 活动ID（必填）
* @param {string} data.remark 驳回原因（必填，5-200字符）
* @param {number} data.processorId 处理人ID（必填）
* @returns {Promise} 包含操作结果的Promise对象
*/
export function rejectAuditClub(data) {
  return request({
    url: '/manage/audit/rejectNewClub',
    method: 'post',
    data: {
      auditId: data.auditId,
      clubId: data.clubId,
      remark: data.remark,
      processorId: data.processorId
    }
  })
}

// ================== 成果审核API ================== //

/**
* 获取成果审核列表
* @param {Object} query 查询参数
* @param {string} [query.name] 成果名称（模糊查询）
* @param {string} [query.clubName] 社团名称（精确查询）
* @param {string} [query.leaderName] 负责人名称（精确查询）
* @param {string} [query.beginTime] 开始时间（YYYY-MM-DD）
* @param {string} [query.endTime] 结束时间（YYYY-MM-DD）
* @returns {Promise} 包含成果审核列表的Promise对象
*/
export function listAuditAchievements(query) {
  return request({
    url: '/manage/audit/listAchievements',
    method: 'get',
    params: query
  })
}

/**
* 成果审核通过接口
* @param {Object} data 审核数据
* @param {number} data.auditId 审核记录ID（必填）
* @param {number} data.achievementId 成果ID（必填）
* @param {string} [data.remark] 审核备注（5-200字符）
* @param {number} data.processorId 处理人ID（必填）
* @returns {Promise} 包含操作结果的Promise对象
*/
export function approveAuditAchievement(data) {
  return request({
    url: '/manage/audit/approveAchievement',
    method: 'post',
    data: {
      auditId: data.auditId,
      achievementId: data.achievementId,
      remark: data.remark,
      processorId: data.processorId
    }
  })
}

/**
* 成果审核驳回接口
* @param {Object} data 审核数据
* @param {number} data.auditId 审核记录ID（必填）
* @param {number} data.achievementId 成果ID（必填）
* @param {string} data.remark 驳回原因（必填，5-200字符）
* @param {number} data.processorId 处理人ID（必填）
* @returns {Promise} 包含操作结果的Promise对象
*/
export function rejectAuditAchievement(data) {
  return request({
    url: '/manage/audit/rejectAchievement',
    method: 'post',
    data: {
      auditId: data.auditId,
      achievementId: data.achievementId,
      remark: data.remark,
      processorId: data.processorId
    }
  })
}