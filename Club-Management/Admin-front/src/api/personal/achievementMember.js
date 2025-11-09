import request from '@/utils/request'

export function insertAchievementMember(data) {
    return request({
        url: '/personal/achievementMember',
        method: 'post',
        data: data
    })
}

// 批量插入成果与成员的绑定关系
export function insertAchievementMembers(data) {
    return request({
        url: '/personal/achievementMember/batch',
        method: 'post',
        data: data
    })
}