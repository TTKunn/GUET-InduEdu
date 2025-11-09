import request from '@/utils/request'

// 查询社团分类管理列表
export function listDept(query) {
    return request({
        url: '/system/dept/list',
        method: 'get',
        params: query    
    })
}