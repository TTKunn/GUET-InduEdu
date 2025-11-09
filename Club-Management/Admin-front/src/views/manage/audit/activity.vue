<template>
    <div class="app-container">
      <!-- Search Form -->
      <el-form :model="queryParams" ref="queryForm" :inline="true" v-show="showSearch" label-width="100px">
        <el-form-item label="活动名称" prop="activityName">
          <el-input v-model="queryParams.activityName" placeholder="请输入活动名称" clearable />
        </el-form-item>
        <el-form-item label="活动地点" prop="location">
          <el-input v-model="queryParams.location" placeholder="请输入活动地点" clearable />
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
        <el-form-item label="开始时间">
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
          <el-button type="primary" plain icon="Plus" @click="handleAdd">创建活动</el-button>
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
        <el-table-column label="活动名称" prop="activityName" align="center" show-overflow-tooltip />
        <el-table-column label="活动地点" prop="location" align="center" />
        <el-table-column label="开始时间" prop="startTime" width="180" align="center">
          <template #default="scope">
            <span>{{ parseTime(scope.row.startTime, '{y}-{m}-{d} {h}:{i}') }}</span>
          </template>
        </el-table-column>
        <el-table-column label="结束时间" prop="endTime" width="180" align="center">
          <template #default="scope">
            <span>{{ parseTime(scope.row.endTime, '{y}-{m}-{d} {h}:{i}') }}</span>
          </template>
        </el-table-column>
        
        <el-table-column label="负责人" prop="leaderName" align="center" />
              <!-- 判断活动是否已经结束（若当前系统时间大于结束时间，则活动状态为已结束） -->
      <el-table-column label="活动状态" align="center">
        <template #default="scope">
          <el-tag :type="getActivityStatusType(scope.row.startTime, scope.row.endTime)">
            {{ getActivityStatusLabel(scope.row.startTime, scope.row.endTime) }}
          </el-tag>
        </template>
      </el-table-column>
        <el-table-column label="状态" align="center">
          <template #default="scope">
            <el-tag :type="getStatusTagType(scope.row.status)">
              {{ STATUS_MAP[scope.row.status] || '--' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="社团" prop="clubName" align="center"  show-overflow-tooltip/>
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
        title="活动详情"
        width="40%"
      >
        <el-descriptions :column="1" border>
          <el-descriptions-item label="活动名称">{{ detailDialog.currentDetail?.activityName || '--' }}</el-descriptions-item>
          <el-descriptions-item label="活动简介">{{ detailDialog.currentDetail?.activityDescription || '--' }}</el-descriptions-item>
          <el-descriptions-item label="活动地点">{{ detailDialog.currentDetail?.location || '--' }}</el-descriptions-item>
          <el-descriptions-item label="负责人">{{ detailDialog.currentDetail?.leaderName || '--' }}</el-descriptions-item>
          <el-descriptions-item label="所属社团">{{ detailDialog.currentDetail?.clubName || '--' }}</el-descriptions-item>
          <el-descriptions-item label="开始时间">
            {{ parseTime(detailDialog.currentDetail?.startTime) || '--' }}
          </el-descriptions-item>
          <el-descriptions-item label="结束时间">
            {{ parseTime(detailDialog.currentDetail?.endTime) || '--' }}
          </el-descriptions-item>
          <el-descriptions-item label="状态">
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
  import { listAuditActivities, approveAuditActivity, rejectAuditActivity } from '@/api/manage/audit'
  import { loadAllParams } from "@/api/page.js"
  import { listLeaderName } from '@/api/manage/club'
  import { getInfo } from '@/api/login'
  
  const { proxy } = getCurrentInstance()
  
  // Constants
  const STATUS_MAP = {
    pending: '待审核',
    published: '已发布',
    rejected: '已驳回',
    ongoing: '进行中',
    completed: '已结束'
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
    activityName: null,
    location: null,
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
    activityId: null,
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

  // Lifecycle hooks
  onMounted(() => {
    getList()
    fetchLeaderList()
  })
  
  /**
   * Fetch activity list data
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
      
      const response = await listAuditActivities(queryParams)
      tableData.value = response.rows
      total.value = response.total
    } catch (error) {
      console.error('Failed to fetch activities:', error)
      proxy.$modal.msgError('数据加载失败')
    } finally {
      loading.value = false
    }
  }
  
  /**
   * Handle search button click
   */
  function handleQuery() {
    if(queryParams.activityName || queryParams.location || queryParams.leaderName || queryParams.clubName || dateRange.value) {
        queryParams.pageNum = 1
        getList()
    }
    else return
  }
  
  /**
   * Reset search form
   */
  function resetQuery() {
    proxy.resetForm('queryForm')
    dateRange.value = []
    getList()
  }
  
  /**
   * Handle table selection change
   */
  function handleSelectionChange(selection) {
    selectedIds.value = selection.map(item => item.activityId)
  }
  
  /**
   * Handle add button click (placeholder)
   */
  function handleAdd() {
    proxy.$modal.msgInfo('创建活动功能待实现')
  }
  
  /**
   * Handle delete button click (placeholder)
   */
  function handleDelete() {
    if (selectedIds.value.length === 0) {
      proxy.$modal.msgWarning('请选择要删除的记录')
      return
    }
    proxy.$modal.msgInfo('删除功能待实现')
  }
  
  /**
   * Handle export button click (placeholder)
   */
  function handleExport() {
    proxy.$modal.msgInfo('导出功能待实现')
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
    auditForm.activityId = row.activityId
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
        relatedId: auditForm.activityId,
        remark: auditForm.remark,
        processorId: userId
      }
  
      // Call appropriate API based on action type
      if (auditDialog.isApprove) {
        await approveAuditActivity(params)
      } else {
        // Ensure remark is provided for rejection
        if (!params.remark.trim()) {
          proxy.$modal.msgError("驳回操作必须填写备注")
          return
        }
        await rejectAuditActivity(params)
      }
  
      // Show success message and refresh data
      proxy.$modal.msgSuccess('操作成功')
      auditDialog.visible = false
      getList()
      
    } catch (error) {
      // Handle errors
      console.error('审核操作失败:', error)
      const errorMsg = error.response?.data?.msg || error.message || '操作失败'
      proxy.$modal.msgError(errorMsg)
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
      proxy.$modal.msgError('负责人列表加载失败')
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

  const getActivityStatusType = (startTime, endTime) => {
  const now = new Date();
  const start = new Date(startTime);
  const end = new Date(endTime);

  if (now < start) {
    return 'warning'; // For '未开始'
  } else if (now >= start && now < end) {
    return 'success'; // For '进行中'
  } else {
    return 'info'; // For '已结束'
  }
};
const getActivityStatusLabel = (startTime, endTime) => {
  if (!startTime && !endTime) return '未知';

  const now = new Date();
  const start = new Date(startTime);
  const end = new Date(endTime);

  if (now < start) {
    return '未开始';
  } else if (now >= start && now < end) {
    return '进行中';
  } else {
    return '已结束';
  }
};
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