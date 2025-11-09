<template>
    <div class="app-container">
        <!-- Search Form -->
        <el-form :model="queryParams" ref="queryForm" :inline="true" v-show="showSearch" label-width="100px">
            <el-form-item label="社团名称" prop="clubName">
                <el-input v-model="queryParams.clubName" placeholder="请输入社团名称" clearable />
            </el-form-item>
            <el-form-item label="社团类型" prop="category">
                <el-select v-model="queryParams.categoryId" placeholder="请选择分类" clearable>
                    <el-option v-for="item in categoryList" :key="item.categoryId" :label="item.name"
                        :value="item.categoryId" />
                </el-select>
            </el-form-item>
            <el-form-item label="学院" prop="applicant">
                <el-select v-model="queryParams.deptId" placeholder="请选择所属学院" clearable>
                    <el-option v-for="item in deptList" :key="item.deptId" :label="item.deptName" :value="item.deptId" />
                </el-select>
            </el-form-item>
            <el-form-item label="申请时间">
                <el-date-picker v-model="dateRange" type="daterange" value-format="YYYY-MM-DD" range-separator="-"
                    start-placeholder="开始日期" end-placeholder="结束日期" />
            </el-form-item>
            <el-form-item>
                <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
                <el-button icon="Refresh" @click="resetQuery">重置</el-button>
            </el-form-item>
        </el-form>
        <!-- Action Buttons -->
        <el-row :gutter="10" class="mb8">
            <el-col :span="1.5">
                <el-button type="warning" icon="Download" @click="handleExport">导出</el-button>
            </el-col>
        </el-row>
        <!-- Data Table -->
        <el-table v-loading="loading" :data="tableData" @selection-change="handleSelectionChange">
            <el-table-column type="selection" width="55" align="center" />
            <el-table-column label="序号" type="index" width="50" align="center" />
            <el-table-column label="社团名称" prop="clubName" align="center" show-overflow-tooltip />
            <el-table-column label="社团简介" prop="description" align="center" show-overflow-tooltip />
            <el-table-column label="社团类型" prop="categoryName" align="center" />
            <el-table-column label="所属学院" prop="deptName" align="center" show-overflow-tooltip />
            <el-table-column label="申请人" prop="applicant" align="center" show-overflow-tooltip />

            <el-table-column label="申请时间" prop="createAt" width="180" align="center">
                <template #default="scope">
                    <span>{{ parseTime(scope.row.createAt, '{y}-{m}-{d} {h}:{i}') }}</span>
                </template>
            </el-table-column>
            <el-table-column label="申请理由" prop="userRemark" align="center" show-overflow-tooltip />
            <el-table-column label="状态" align="center">
          <template #default="scope">
            <el-tag :type="getStatusTagType(scope.row.status)">
              {{ STATUS_MAP[scope.row.status] || '--' }}
            </el-tag>
          </template>
        </el-table-column>
            <el-table-column label="操作" align="center" width="180">
                <template #default="scope">
                    <el-button link type="info" @click="handleDetail(scope.row)">详情</el-button>
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
        <!-- Pagination -->
        <pagination v-show="total > 0" :total="total" v-model:page="queryParams.pageNum"
            v-model:limit="queryParams.pageSize" @pagination="getList" />
        <!-- Audit Dialog -->
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

        <!-- Detail Dialog -->
        <el-dialog v-model="detailDialog.visible" title="社团详情" width="40%">
            <el-descriptions :column="1" border>
                <el-descriptions-item label="社团名称">{{ detailDialog.currentDetail?.clubName || '--' }}</el-descriptions-item>
                <el-descriptions-item label="社团简介">{{ detailDialog.currentDetail?.description || '--' }}</el-descriptions-item>
                <el-descriptions-item label="社团类型">{{ detailDialog.currentDetail?.categoryName || '--' }}</el-descriptions-item>
                <el-descriptions-item label="所属学院">{{ detailDialog.currentDetail?.deptName || '--' }}</el-descriptions-item>
                <el-descriptions-item label="申请人">{{ detailDialog.currentDetail?.applicant || '--' }}</el-descriptions-item>
                <el-descriptions-item label="申请时间">
                    {{ parseTime(detailDialog.currentDetail?.createAt) || '--' }}
                </el-descriptions-item>
                <el-descriptions-item label="申请理由">
                    {{ detailDialog.currentDetail?.userRemark || '--' }}
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
import { listAuditClub, approveAuditClub, rejectAuditClub } from "@/api/manage/audit"
import { listCategory } from "@/api/manage/category";
import { listDept } from "@/api/system/dept";
import { loadAllParams } from "@/api/page.js"
import { getInfo } from '@/api/login'


const { proxy } = getCurrentInstance()
// Constants
const STATUS_MAP = {
    pending: '待审核',
    approved: '已通过',
    rejected: '已驳回',
}
// state
const loading = ref(false)
const showSearch = ref(true)
const tableData = ref([])
const total = ref(0)
const dateRange = ref([])
const selectedIds = ref([])
const auditFormRef = ref(null)

// Query parameters
const queryParams = reactive({
    pageNum: 1,
    pageSize: 10,
    clubName: null,
    categoryId: null,
    deptId: null,
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
    clubId: null,
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

// Lifecycle hooks
onMounted(() => {
    getCategoryList()
    getDeptList()
    getList()
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

        const response = await listAuditClub(queryParams)
        tableData.value = response.rows
        total.value = response.total
    } catch (error) {
        console.error('Failed to fetch club:', error)
        proxy.$modal.msgError('数据加载失败')
    } finally {
        loading.value = false
    }
}

/**
 * Handle search button click
 */
function handleQuery() {
    if (queryParams.clubName || queryParams.categoryId || queryParams.deptId || dateRange.value) {
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
    queryParams.clubName = null
    queryParams.categoryId = null
    queryParams.deptId = null
    queryParams.params.beginCreatedAt = null
    queryParams.params.endCreatedAt = null
    queryParams.pageNum = 1
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
 * Handle export button click (placeholder)
 */
function handleExport() {
    proxy.$modal.msgInfo('导出功能待实现')
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
    auditForm.clubId = row.clubId
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
            await approveAuditClub(params)
        } else {
            // Ensure remark is provided for rejection
            if (!params.remark.trim()) {
                proxy.$modal.msgError("驳回操作必须填写备注")
                return
            }
            await rejectAuditClub(params)
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
 *  Get club category list 
*/
const categoryList = ref([]);
function getCategoryList() {
    listCategory(loadAllParams).then(response => {
        categoryList.value = response.rows;
    });
}
/** 
 * Get dept list 
*/
const deptList = ref([]);
function getDeptList() {
    listDept(loadAllParams).then(response => {
        deptList.value = response.data;
    });
}

// Detail dialog state
const detailDialog = reactive({
  visible: false,
  currentDetail: null
})

// Handle detail button click
function handleDetail(row) {
  detailDialog.currentDetail = { ...row }
  detailDialog.visible = true
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
```

```
