<template>
  <div class="app-container">
    <!-- 搜索表单 -->
    <el-form :model="queryParams" ref="queryForm" :inline="true" v-show="showSearch" label-width="100px"
      class="left-align-form">
      <el-form-item label="成果名称" prop="name">
        <el-input v-model="queryParams.achievementTitle" placeholder="请输入成果名称" clearable />
      </el-form-item>
      <el-form-item label="所属社团" prop="clubName">
        <el-input v-model="queryParams.clubName" placeholder="请输入社团名称" clearable />
      </el-form-item>
      <el-form-item label="负责人" prop="leaderName">
        <el-select v-model="queryParams.leaderId" placeholder="请选择负责人" clearable>
          <el-option v-for="leader in leaderList" :key="leader.leaderId" :label="leader.leaderName"
            :value="leader.leaderId" />
        </el-select>
      </el-form-item>
      <el-form-item label="成果类型" prop="type" style="width: 295px;">
        <el-select v-model="queryParams.type" placeholder="请选择成果类型" clearable>
          <el-option v-for="type in typeOptions" :key="type.dictValue" :label="type.dictLabel" :value="type.dictValue" />
        </el-select>
      </el-form-item>

      <el-form-item label="获得时间">
        <el-date-picker v-model="dateRange" type="daterange" value-format="YYYY-MM-DD" range-separator="-"
          start-placeholder="开始日期" end-placeholder="结束日期" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
        <el-button icon="Refresh" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <!-- 操作按钮 -->
    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button type="danger" plain icon="Delete" @click="handleDelete">删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button type="warning" icon="Download" @click="handleExport">导出</el-button>
      </el-col>
    </el-row>

    <!-- 数据表格 -->
    <el-table v-loading="loading" :data="tableData" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="序号" type="index" width="50" align="center" />
      <el-table-column label="成果名称" prop="title" align="center" show-overflow-tooltip />
      <!-- <el-table-column label="成果简介" prop="description" align="center" show-overflow-tooltip /> -->
      <el-table-column label="成果类型" prop="type" align="center">
        <template #default="scope">
          {{ typeOptions.find(option => option.dictValue === scope.row.type)?.dictLabel || '--' }}
        </template>
      </el-table-column>
      <el-table-column label="所属社团" prop="clubName" align="center" show-overflow-tooltip/>
      <!-- <el-table-column label="负责人" prop="leaderName" align="center" /> -->
      <el-table-column label="获得时间" prop="achieveDate" width="180" align="center">
        <template #default="scope">
          <span>{{ parseTime(scope.row.achieveDate, '{y}-{m}-{d} {h}:{i}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="创建时间" prop="createdAt" align="center" show-overflow-tooltip width="180"/>
      <el-table-column label="证书地址" align="center" prop="certificateUrl" width="100">
        <template #default="scope">
          <image-preview :src="scope.row.certificateUrl" :width="50" :height="50"/>
        </template>
      </el-table-column>
      <el-table-column label="申报备注" prop="userRemark" align="center" show-overflow-tooltip />
      <el-table-column label="状态" align="center">
        <template #default="scope">
          <el-tag :type="getStatusTagType(scope.row.status)">
            {{ STATUS_MAP[scope.row.status] || '--' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" width="180">
        <template #default="scope">
          <!-- 新增详情按钮 -->
          <el-button link type="info" @click="handleDetail(scope.row)">
            详情
          </el-button>
          <!-- 原有审核按钮 -->
          <el-button link type="primary" @click="handleAudit(scope.row)"
            v-if="['pending', 'rejected'].includes(scope.row.status)">
            {{ scope.row.status === 'rejected' ? '重新通过' : '通过' }}
          </el-button>
          <el-button link type="danger" @click="handleReject(scope.row)" v-if="scope.row.status === 'pending'">
            驳回
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <pagination v-show="total > 0" :total="total" v-model:page="queryParams.pageNum" v-model:limit="queryParams.pageSize"
      @pagination="getList" />

    <!-- 审核对话框 -->
    <el-dialog v-model="auditDialog.visible" :title="auditDialog.isApprove ? '审核通过' : '审核驳回'" width="30%">
      <el-form :model="auditForm" :rules="auditRules" ref="auditFormRef">
        <el-form-item label="备注" prop="remark">
          <el-input v-model="auditForm.remark" type="textarea" placeholder="请输入审核备注"
            :autosize="{ minRows: 4, maxRows: 6 }" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="auditDialog.visible = false">取消</el-button>
        <el-button type="primary" @click="submitAudit">确定</el-button>
      </template>
    </el-dialog>

    <!-- 新增详情对话框 -->
    <el-dialog v-model="detailDialog.visible" title="成果详情" width="40%">
      <el-descriptions :column="1" border>
        <el-descriptions-item label="成果名称">{{ detailDialog.currentDetail?.title || '--' }}</el-descriptions-item>
        <el-descriptions-item label="成果类型">
          {{ typeOptions.find(option => option.dictValue === detailDialog.currentDetail?.type)?.dictLabel || '--' }}
        </el-descriptions-item>
        <el-descriptions-item label="所属社团">{{ detailDialog.currentDetail?.clubName || '--' }}</el-descriptions-item>
        <el-descriptions-item label="负责人">{{ detailDialog.currentDetail?.leaderName || '--' }}</el-descriptions-item>
        <el-descriptions-item label="获得时间">
          {{ parseTime(detailDialog.currentDetail?.achieveDate) || '--' }}
        </el-descriptions-item>
        <el-descriptions-item label="创建时间">
          {{ parseTime(detailDialog.currentDetail?.createdAt) || '--' }}
        </el-descriptions-item>
        <el-descriptions-item label="证书链接">
          <el-link v-if="detailDialog.currentDetail?.certificateUrl" :href="detailDialog.currentDetail.certificateUrl"
            target="_blank" type="primary">
            查看证书
          </el-link>
          <span v-else>--</span>
        </el-descriptions-item>
        <el-descriptions-item label="成果简介" :span="2">
          {{ detailDialog.currentDetail?.description || '--' }}
        </el-descriptions-item>
        <el-descriptions-item label="申报备注">
          {{ detailDialog.currentDetail?.userRemark || '--' }}
        </el-descriptions-item>
        <el-descriptions-item label="审核状态">
          {{ STATUS_MAP[detailDialog.currentDetail?.status] || '--' }}
        </el-descriptions-item>
      </el-descriptions>

      <template #footer>
        <el-button @click="detailDialog.visible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>
  
<script setup>
import { ref, reactive, onMounted, getCurrentInstance } from 'vue'
import { listAuditAchievements, approveAuditAchievement, rejectAuditAchievement } from '@/api/manage/audit'
import { loadAllParams } from "@/api/page.js"
import { listLeaderName } from '@/api/manage/club'
import { getInfo } from '@/api/login'

const { proxy } = getCurrentInstance()

// 状态常量
const STATUS_MAP = {
  pending: '待审核',
  approved: '已通过',
  rejected: '已驳回'
}

// 成果类型选项
const typeOptions = ref([
  { dictValue: 'competition', dictLabel: '竞赛' },
  { dictValue: 'project', dictLabel: '项目' },
  { dictValue: 'other', dictLabel: '其他' }
])

// 响应式状态
const loading = ref(false)
const showSearch = ref(true)
const tableData = ref([])
const total = ref(0)
const dateRange = ref([])
const selectedIds = ref([])
const leaderList = ref([])
const auditFormRef = ref(null)

// 查询参数
const queryParams = reactive({
  pageNum: 1,
  pageSize: 10,
  achievementTitle: null,
  clubName: null,
  leaderId: null,
  type: null,
  params: {
    beginCreatedAt: null,
    endCreatedAt: null
  }
})

// 审核对话框状态
const auditDialog = reactive({
  visible: false,
  isApprove: true
})

// 详情对话框状态
const detailDialog = reactive({
  visible: false,
  currentDetail: null
})

// 审核表单
const auditForm = reactive({
  auditId: null,
  achievementId: null,
  remark: '',
  processorId: null
})

// 验证规则
const auditRules = {
  remark: [
    { required: true, message: '备注不能为空', trigger: 'blur' },
    { min: 5, max: 200, message: '长度在5到200个字符', trigger: 'blur' }
  ]
}

// 生命周期钩子
onMounted(() => {
  getList()
  fetchLeaderList()
})

// 方法
async function getList() {
  try {
    loading.value = true
    if (dateRange.value?.length === 2) {
      queryParams.params.beginCreatedAt = dateRange.value[0]
      queryParams.params.endCreatedAt = dateRange.value[1]
    }
    const response = await listAuditAchievements(queryParams)
    tableData.value = response.rows
    total.value = response.total
  } catch (error) {
    console.error('获取成果列表失败:', error)
    proxy.$modal.msgError('数据加载失败')
  } finally {
    loading.value = false
  }
}

function handleQuery() {
  queryParams.pageNum = 1
  getList()
}

function resetQuery() {
  proxy.resetForm('queryForm')
  dateRange.value = []
  // Reset all query parameters to initial state
  queryParams.pageNum = 1
  queryParams.pageSize = 10
  queryParams.achievementTitle = null
  queryParams.clubName = null
  queryParams.leaderId = null
  queryParams.type = null
  queryParams.params.beginCreatedAt = null
  queryParams.params.endCreatedAt = null
  getList()
}

function handleSelectionChange(selection) {
  selectedIds.value = selection.map(item => item.achievementId)
}

function handleDelete() {
  if (!selectedIds.value.length) {
    proxy.$modal.msgWarning('请选择要删除的记录')
    return
  }
  proxy.$modal.msgInfo('删除功能待实现')
}

function handleExport() {
  proxy.$modal.msgInfo('导出功能待实现')
}

// 新增详情处理方法
function handleDetail(row) {
  detailDialog.currentDetail = { ...row }
  detailDialog.visible = true
}

function handleAudit(row) {
  auditDialog.isApprove = true
  openAuditDialog(row)
}

function handleReject(row) {
  auditDialog.isApprove = false
  openAuditDialog(row)
}

function openAuditDialog(row) {
  auditForm.auditId = row.auditId
  auditForm.achievementId = row.achievementId
  auditForm.remark = ''
  auditDialog.visible = true
}

async function submitAudit() {
  try {
    await auditFormRef.value.validate()
    const userId = await getCurrentUserId()

    const params = {
      auditId: auditForm.auditId,
      achievementId: auditForm.achievementId,
      remark: auditForm.remark,
      processorId: userId
    }

    if (auditDialog.isApprove) {
      await approveAuditAchievement(params)
    } else {
      if (!params.remark.trim()) {
        proxy.$modal.msgError("驳回操作必须填写备注")
        return
      }
      await rejectAuditAchievement(params)
    }

    proxy.$modal.msgSuccess('操作成功')
    auditDialog.visible = false
    getList()
  } catch (error) {
    console.error('审核操作失败:', error)
    proxy.$modal.msgError(error.response?.data?.msg || '操作失败')
  }
}

async function fetchLeaderList() {
  try {
    const response = await listLeaderName(loadAllParams)
    leaderList.value = response.rows
  } catch (error) {
    console.error('加载负责人列表失败:', error)
    proxy.$modal.msgError('负责人列表加载失败')
  }
}

async function getCurrentUserId() {
  try {
    const res = await getInfo()
    return res.user.userId
  } catch (error) {
    console.error('获取用户信息失败:', error)
    throw new Error('用户信息获取失败')
  }
}

/**
* Get tag type based on status
*/
function getStatusTagType(status) {
  switch (status) {
    case 'pending':
      return 'warning'
    case 'published':
      return 'success'
    case 'rejected':
      return 'danger'
    case 'ongoing':
      return 'primary'
    case 'completed':
      return 'info'
    default:
      return ''
  }
}
</script>
  
<style scoped>
.app-container {
  padding: 20px;
}

.mb8 {
  margin-bottom: 8px;
}

/* 新增详情对话框样式 */
:deep(.el-descriptions__body) {
  background-color: #f8f8f9;
}

:deep(.el-descriptions__title) {
  min-width: 100px;
  text-align: right;
}

.left-align-form {
  :deep(.el-form-item) {
    text-align: left;
  }
}
</style>