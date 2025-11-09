<template>
  <div class="app-container">
    <!-- Search Form -->
    <el-form :model="queryParams" ref="queryForm" :inline="true" v-show="showSearch" label-width="100px">
      <el-form-item label="公告标题" prop="title">
        <el-input v-model="queryParams.title" placeholder="请输入公告标题" clearable />
      </el-form-item>
      <el-form-item label="公告内容" prop="content">
        <el-input v-model="queryParams.content" placeholder="请输入公告内容" clearable />
      </el-form-item>
      <el-form-item label="负责人" prop="leaderName">
        <el-select v-model="queryParams.leaderName" placeholder="请选择负责人" clearable>
          <el-option 
            v-for="leader in leaderList" 
            :key="leader.leaderId" 
            :label="leader.leaderName" 
            :value="leader.leaderName" 
          />
        </el-select>
      </el-form-item>
      <el-form-item label="所属社团" prop="clubName">
        <el-input v-model="queryParams.clubName" placeholder="请输入社团名称" clearable />
      </el-form-item>
      <el-form-item label="发布时间">
        <el-date-picker 
          v-model="dateRange" 
          type="daterange" 
          value-format="YYYY-MM-DD" 
          range-separator="-"
          start-placeholder="开始日期" 
          end-placeholder="结束日期" 
        />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
        <el-button icon="Refresh" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <!-- Action Buttons -->
    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button type="primary" plain icon="Plus" @click="handleAdd">发布公告</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button type="danger" plain icon="Delete" @click="handleDelete">删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button type="warning" icon="Download" @click="handleExport">导出</el-button>
      </el-col>
    </el-row>

    <!-- Data Table -->
    <el-table 
      v-loading="loading" 
      :data="tableData" 
      @selection-change="handleSelectionChange"
    >
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="序号" type="index" width="50" align="center" />
      <el-table-column label="标题" prop="title" align="center" show-overflow-tooltip />
      <el-table-column label="公告内容" align="center" width="180">
  <template #default="scope">
    <div class="content-preview" v-html="scope.row.content"></div>
  </template>
</el-table-column>
      <el-table-column label="发布人" prop="leaderName" align="center" />
      <el-table-column label="发布时间" prop="createAt" width="160" align="center">
        <template #default="scope">
          <span>{{ parseTime(scope.row.createAt, '{y}-{m}-{d} {h}:{i}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="创建时间" prop="auCreateAt" width="160" align="center">
        <template #default="scope">
          <span>{{ parseTime(scope.row.createAt, '{y}-{m}-{d} {h}:{i}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="状态" align="center">
          <template #default="scope">
            <el-tag :type="getStatusTagType(scope.row.status)">
              {{ STATUS_MAP[scope.row.status] || '--' }}
            </el-tag>
          </template>
        </el-table-column>
      <el-table-column label="用户备注" prop="userRemark" align="center" />
      <el-table-column label="社团" prop="clubName" align="center" show-overflow-tooltip />
      <el-table-column label="操作" align="center" width="180">
        <template #default="scope">
          <el-button 
            link 
            type="info" 
            @click="handleDetail(scope.row)"
          >
            详情
          </el-button>
          <el-button 
            link 
            type="primary" 
            @click="handleAudit(scope.row)"
            v-if="['pending', 'rejected'].includes(scope.row.status)"
          >
            {{ scope.row.status === 'rejected' ? '重新通过' : '通过' }}
          </el-button>
          <el-button 
            link 
            type="danger" 
            @click="handleReject(scope.row)" 
            v-if="scope.row.status === 'pending'"
          >
            驳回
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- Pagination -->
    <pagination 
      v-show="total > 0" 
      :total="total" 
      v-model:page="queryParams.pageNum" 
      v-model:limit="queryParams.pageSize"
      @pagination="getList" 
    />

    <!-- Audit Dialog -->
    <el-dialog 
      v-model="auditDialog.visible" 
      :title="auditDialog.isApprove ? '审核通过' : '审核驳回'" 
      width="30%"
    >
      <el-form :model="auditForm" :rules="auditRules" ref="auditFormRef">
        <el-form-item label="备注" prop="remark">
          <el-input 
            v-model="auditForm.remark" 
            type="textarea" 
            placeholder="请输入审核备注" 
            :autosize="{ minRows: 4, maxRows: 6 }"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="auditDialog.visible = false">取消</el-button>
        <el-button type="primary" @click="submitAudit">确定</el-button>
      </template>
    </el-dialog>

    <!-- Detail Dialog -->
    <el-dialog
      v-model="detailDialog.visible"
      title="公告详情"
      width="40%"
    >
      <el-descriptions :column="1" border>
        <el-descriptions-item label="公告标题">{{ detailDialog.currentDetail?.title || '--' }}</el-descriptions-item>

        <el-descriptions-item label="公告内容">{{ detailDialog.currentDetail?.content || '--' }}</el-descriptions-item>
        
        <el-descriptions-item label="发布人">{{ detailDialog.currentDetail?.leaderName || '--' }}</el-descriptions-item>
        <el-descriptions-item label="所属社团">{{ detailDialog.currentDetail?.clubName || '--' }}</el-descriptions-item>
        <el-descriptions-item label="发布时间">
          {{ parseTime(detailDialog.currentDetail?.createAt) || '--' }}
        </el-descriptions-item>
        <el-descriptions-item label="状态">
          {{ statusMap[detailDialog.currentDetail?.status] || '--' }}
        </el-descriptions-item>
        <el-descriptions-item label="用户备注">
          {{ detailDialog.currentDetail?.userRemark || '--' }}
        </el-descriptions-item>
      </el-descriptions>
      
      <template #footer>
        <el-button @click="detailDialog.visible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { listAuditAnnouncements, approveAuditAnnouncement, rejectAuditAnnouncement } from '@/api/manage/audit'
import { loadAllParams } from "@/api/page.js"
import { listLeaderName } from '@/api/manage/club'
import { getInfo } from '@/api/login'
import { ElMessage } from 'element-plus'

// Constants
const STATUS_MAP = {
  pending: '待审核',
  published: '已发布',
  rejected: '已驳回'
}

// State
const loading = ref(false)
const showSearch = ref(true)
const tableData = ref([])
const total = ref(0)
const dateRange = ref([])
const selectedIds = ref([])
const leaderList = ref([])
const auditFormRef = ref(null)

// Query parameters
const queryParams = reactive({
  pageNum: 1,
  pageSize: 10,
  title: null,
  content: null,
  leaderName: null,
  clubName: null,
  params: {
    beginCreatedAt: null,
    endCreatedAt: null
  }
})

// Audit dialog state
const auditDialog = reactive({
  visible: false,
  isApprove: true
})

// Audit form
const auditForm = reactive({
  auditId: null,
  announcementId: null,
  remark: '',
  processorId: null
})

// Validation rules
const auditRules = {
  remark: [
    { required: true, message: '备注不能为空', trigger: 'blur' },
    { min: 5, max: 200, message: '长度在5到200个字符', trigger: 'blur' }
  ]
}

// Detail dialog state
const detailDialog = reactive({
  visible: false,
  currentDetail: null
})

// Computed properties
const statusMap = computed(() => STATUS_MAP)

// Lifecycle hooks
onMounted(() => {
  getList()
  fetchLeaderList()
})

// Methods
/**
 * Fetch announcement list data
 */
async function getList() {
  try {
    loading.value = true
    
    // Set date range parameters
    if (dateRange.value && dateRange.value.length === 2) {
      queryParams.params.beginCreatedAt = dateRange.value[0]
      queryParams.params.endCreatedAt = dateRange.value[1]
    } else {
      queryParams.params.beginCreatedAt = null
      queryParams.params.endCreatedAt = null
    }
    
    const response = await listAuditAnnouncements(queryParams)
    tableData.value = response.rows
    total.value = response.total
  } catch (error) {
    console.error('Failed to fetch announcements:', error)
    ElMessage.error('数据加载失败，请重试')
  } finally {
    loading.value = false
  }
}

/**
 * Handle search button click
 */
function handleQuery() {
  if(queryParams.title || queryParams.content || queryParams.leaderName || queryParams.clubName) {
    queryParams.pageNum = 1
    getList()
  }
  else return
}

/**
 * Reset search form
 */
function resetQuery() {
  // Reset form fields
  queryParams.title = null
  queryParams.content = null
  queryParams.leaderName = null
  queryParams.clubName = null
  dateRange.value = []
  
  // Reset pagination and refresh data
  queryParams.pageNum = 1
  getList()
}

/**
 * Handle table selection change
 */
function handleSelectionChange(selection) {
  selectedIds.value = selection.map(item => item.announcementId)
}

/**
 * Handle add button click (placeholder)
 */
function handleAdd() {
  ElMessage.info('发布公告功能待实现')
}

/**
 * Handle delete button click (placeholder)
 */
function handleDelete() {
  if (selectedIds.value.length === 0) {
    ElMessage.warning('请选择要删除的记录')
    return
  }
  ElMessage.info('删除功能待实现')
}

/**
 * Handle export button click (placeholder)
 */
function handleExport() {
  ElMessage.info('导出功能待实现')
}

/**
 * Handle detail button click
 */
function handleDetail(row) {
  detailDialog.currentDetail = { ...row }
  detailDialog.visible = true
}

/**
 * Open audit dialog for approval
 */
function handleAudit(row) {
  auditDialog.isApprove = true
  openAuditDialog(row)
}

/**
 * Open audit dialog for rejection
 */
function handleReject(row) {
  auditDialog.isApprove = false
  openAuditDialog(row)
}

/**
 * Open the audit dialog
 */
function openAuditDialog(row) {
  auditForm.auditId = row.auditId
  auditForm.announcementId = row.announcementId
  auditForm.remark = ''
  auditDialog.visible = true
}

/**
 * Submit audit decision
 */
async function submitAudit() {
  try {
    // Validate form
    await auditFormRef.value.validate()
    
    // Get current user ID
    const userId = await getCurrentUserId()
    
    // Prepare request params
    const params = {
      auditId: auditForm.auditId,
      relatedId: auditForm.announcementId,
      remark: auditForm.remark,
      processorId: userId
    }

    // Call appropriate API based on action type
    if (auditDialog.isApprove) {
      await approveAuditAnnouncement(params)
    } else {
      // Ensure remark is provided for rejection
      if (!params.remark.trim()) {
        ElMessage.error("驳回操作必须填写备注")
        return
      }
      await rejectAuditAnnouncement(params)
    }

    // Show success message and refresh data
    ElMessage.success('操作成功')
    auditDialog.visible = false
    getList()
    
  } catch (error) {
    // Handle errors
    console.error('审核操作失败:', error)
    const errorMsg = error.response?.data?.msg || error.message || '操作失败'
    ElMessage.error(errorMsg)
  }
}

/**
 * Fetch leader list data
 */
async function fetchLeaderList() {
  try {
    const response = await listLeaderName(loadAllParams)
    leaderList.value = response.rows
  } catch (error) {
    console.error('Failed to load leader list:', error)
    ElMessage.error('负责人列表加载失败')
  }
}

/**
 * Get current user ID
 */
async function getCurrentUserId() {
  try {
    const res = await getInfo()
    return res.user.userId
  } catch (error) {
    console.error('Failed to get user info:', error)
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

/* Detail dialog styles */
:deep(.el-descriptions__body) {
  background-color: #f8f8f9;
}
:deep(.el-descriptions__title) {
  min-width: 100px;
  text-align: right;
}
</style>