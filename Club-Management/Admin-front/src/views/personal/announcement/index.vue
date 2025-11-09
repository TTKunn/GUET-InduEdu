<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch" label-width="80px">
      <el-form-item label="公告类型" prop="type">
        <el-select v-model="queryParams.type" placeholder="全部类型" clearable>
          <el-option label="公共公告" value="public" />
          <el-option label="内部公告" value="internal" />
        </el-select>
      </el-form-item>
      <el-form-item label="公告标题" prop="title">
        <el-input v-model="queryParams.title" placeholder="请输入公告标题" clearable @keyup.enter="handleQuery" />
      </el-form-item>
      <el-form-item label="发布人" prop="publisher">
        <el-input v-model="queryParams.userName" placeholder="学号" clearable style="width: 120px" />
        <el-input v-model="queryParams.nickName" placeholder="姓名" clearable style="width: 120px; margin-left: 10px" />
      </el-form-item>
      <el-form-item label="公告状态" prop="status">
        <el-select v-model="queryParams.status" placeholder="全部状态" clearable>
          <el-option label="待审批" value="pending" />
          <el-option label="已发布" value="published" />
          <el-option label="已驳回" value="rejected" />
        </el-select>
      </el-form-item>
      <el-form-item label="发布时间" prop="createdAt">
        <el-date-picker 
          v-model="daterangeCreatedAt" 
          type="daterange" 
          range-separator="至"
          start-placeholder="开始日期" 
          end-placeholder="结束日期"
          value-format="YYYY-MM-DD"
          clearable
        />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
        <el-button icon="Refresh" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button type="primary" plain icon="Plus" @click="handleAdd" v-hasPermi="['personal:announcement:add']">
          新增
        </el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button 
          type="success" 
          plain 
          icon="Edit" 
          :disabled="single" 
          @click="handleUpdate"
          v-hasPermi="['personal:announcement:edit']">
          修改
        </el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button 
          type="danger" 
          plain 
          icon="Delete" 
          :disabled="multiple" 
          @click="handleDelete"
          v-hasPermi="['personal:announcement:remove']">
          删除
        </el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button 
          type="warning" 
          plain 
          icon="Download" 
          @click="handleExport"
          v-hasPermi="['personal:announcement:export']">
          导出
        </el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="handleQuery" />
    </el-row>

    <!-- 公告表格 -->
    <el-table
      v-loading="loading"
      :data="announcementList"
      @selection-change="handleSelectionChange"
      :row-key="row => row.announcementId"
      style="width: 100%"
    >
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="序号" type="index" align="center" width="60" />
      <el-table-column label="公告标题" align="center" prop="title" min-width="150" show-overflow-tooltip />
      <el-table-column label="公告类型" align="center" prop="type" width="100">
        <template #default="{row}">
          <el-tag :type="row.type === 'public' ? '' : 'success'">
            {{ row.type === 'public' ? '公共' : '内部' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="公告内容" align="center" min-width="180" show-overflow-tooltip>
        <template #default="{row}">
          <div class="content-preview">{{ stripHtml(row.content) }}</div>
        </template>
      </el-table-column>
      <el-table-column label="发布人" align="center" width="150">
        <template #default="{row}">
          <div>{{ row.userName }} {{ row.nickName }}</div>
          <!-- <div>{{ row.nickName }}</div> -->
        </template>
      </el-table-column>
      <el-table-column label="状态" align="center" prop="status" width="100">
        <template #default="{row}">
          <el-tag :type="statusTagType(row.status)">
            {{ statusChineseMap[row.status] || row.status }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="发布时间" align="center" prop="createdAt" width="150">
        <template #default="{row}">
          {{ parseTime(row.createdAt, '{y}-{m}-{d}') }}
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" width="180" fixed="right">
        <template #default="{row}">
          <el-button link type="primary" @click="handleDetails(row)">详情</el-button>
          <el-button 
            link 
            type="primary" 
            @click="handleUpdate(row)"
            v-hasPermi="['personal:announcement:edit']">
            修改
          </el-button>
          <el-button 
            link 
            type="danger" 
            @click="handleDelete(row)"
            v-hasPermi="['personal:announcement:remove']">
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination 
      v-show="total > 0" 
      :total="total" 
      v-model:page="queryParams.pageNum" 
      v-model:limit="queryParams.pageSize" 
      @pagination="getList" 
    />

    <!-- 添加或修改公告对话框 -->
    <el-dialog :title="title" v-model="open" width="800px" append-to-body>
      <el-form ref="announcementRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="公告标题" prop="title">
          <el-input v-model="form.title" placeholder="请输入公告标题" />
        </el-form-item>
        <el-form-item label="公告类型" prop="type" v-if="!form.announcementId">
          <el-radio-group v-model="form.type">
            <el-radio label="public">公共公告</el-radio>
            <el-radio label="internal">内部公告</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="公告内容" prop="content">
          <editor v-model="form.content" :min-height="300" />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="cancel">取 消</el-button>
          <el-button type="primary" @click="submitForm">确 定</el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 详情对话框 -->
    <el-dialog title="公告详情" v-model="detailOpen" width="700px" append-to-body>
      <el-descriptions :column="1" border>
        <!-- <el-descriptions-item label="公告ID">{{ detailData.announcementId }}</el-descriptions-item> -->
        <el-descriptions-item label="公告标题">{{ detailData.title }}</el-descriptions-item>
        <el-descriptions-item label="公告类型">
          {{ detailData.type === 'public' ? '公共公告' : '内部公告' }}
        </el-descriptions-item>
        <el-descriptions-item label="公告内容">
          <div class="content-full" v-html="detailData.content"></div>
        </el-descriptions-item>
        <el-descriptions-item label="发布人">
          {{ detailData.userName }} ({{ detailData.nickName }})
        </el-descriptions-item>
        <el-descriptions-item label="发布社团">{{ detailData.clubName }}</el-descriptions-item>
        <el-descriptions-item label="发布时间">
          {{ parseTime(detailData.createdAt, '{y}-{m}-{d} {h}:{i}') }}
        </el-descriptions-item>
        <el-descriptions-item label="公告状态">
          <el-tag :type="statusTagType(detailData.status)">
            {{ statusChineseMap[detailData.status] || detailData.status }}
          </el-tag>
        </el-descriptions-item>
      </el-descriptions>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="detailOpen = false">关 闭</el-button>
          <el-button type="primary" @click="detailOpen = false">确 定</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup name="Announcement">
import { listAnnouncement, getAnnouncement, delAnnouncement, addAnnouncement, updateAnnouncement } from "@/api/personal/announcement";
import { selectClubIdByUserId } from '@/api/personal/club'
const { proxy } = getCurrentInstance();
import { getInfo } from '@/api/login'

const announcementList = ref([]);
const loading = ref(true);
const ids = ref([]);
const single = ref(true);
const multiple = ref(true);
const total = ref(0);
const title = ref("");
const open = ref(false);
const detailOpen = ref(false);
const showSearch = ref(true);
const daterangeCreatedAt = ref([]);

const data = reactive({
  form: {},
  queryParams: {
    pageNum: 1,
    pageSize: 10,
    title: undefined,
    userName: undefined,
    nickName: undefined,
    status: undefined,
    type: undefined,
    clubId: undefined
  },
  rules: {
    title: [{ required: true, message: "公告标题不能为空", trigger: "blur" }],
    content: [{ required: true, message: "公告内容不能为空", trigger: "blur" }],
    type: [{ required: true, message: "请选择公告类型", trigger: "change" }]
  }
});

const { form, queryParams, rules } = toRefs(data);
const detailData = ref({});

/** 查询公告列表 */
async function getList() {
  loading.value = true;
  
  // 设置时间范围参数
  queryParams.value.params = {};
  if (daterangeCreatedAt.value && daterangeCreatedAt.value.length === 2) {
    queryParams.value.params.beginCreatedAt = daterangeCreatedAt.value[0];
    queryParams.value.params.endCreatedAt = daterangeCreatedAt.value[1];
  }
  
  try {
    const userId = await getCurrentUserId();
    const clubId = await selectClubIdByUserId(userId);
    queryParams.value.clubId = clubId;
    
    const response = await listAnnouncement(queryParams.value);
    announcementList.value = response.rows;
    total.value = response.total;
  } catch (error) {
    proxy.$modal.msgError("获取公告列表失败，请稍后重试");
    console.error(error);
  } finally {
    loading.value = false;
  }
}

/** 搜索按钮操作 */
function handleQuery() {
  queryParams.value.pageNum = 1;
  getList();
}

/** 重置按钮操作 */
function resetQuery() {
  daterangeCreatedAt.value = [];
  proxy.resetForm("queryRef");
  queryParams.value = {
    pageNum: 1,
    pageSize: 10,
    title: undefined,
    userName: undefined,
    nickName: undefined,
    status: undefined,
    type: undefined,
    clubId: queryParams.value.clubId // 保留社团ID
  };
  handleQuery();
}

/** 多选框选中数据 */
function handleSelectionChange(selection) {
  ids.value = selection.map(item => item.announcementId);
  single.value = selection.length !== 1;
  multiple.value = !selection.length;
}

/** 新增按钮操作 */
function handleAdd() {
  reset();
  open.value = true;
  title.value = "添加公告";
}

/** 修改按钮操作 */
function handleUpdate(row) {
  reset();
  const announcementId = row?.announcementId || ids.value[0];
  if (!announcementId) {
    proxy.$modal.msgError("请先选择要修改的公告");
    return;
  }
  
  getAnnouncement(announcementId).then(response => {
    form.value = response.data;
    open.value = true;
    title.value = "修改公告";
  }).catch(error => {
    proxy.$modal.msgError("获取公告详情失败");
    console.error(error);
  });
}

/** 提交按钮 */
async function submitForm() {
  await proxy.$refs["announcementRef"].validate(async (valid) => {
    if (valid) {
      try {
        if (form.value.announcementId != null) {
          await updateAnnouncement(form.value);
          proxy.$modal.msgSuccess("修改成功");
        } else {
          const userId = await getCurrentUserId();
          const clubId = await selectClubIdByUserId(userId);
          form.value.publisherId = userId;
          form.value.clubId = clubId;
          form.value.status = 'pending'; // 默认待审批状态
          await addAnnouncement(form.value);
          proxy.$modal.msgSuccess("新增成功");
        }
        open.value = false;
        await getList();
      } catch (error) {
        proxy.$modal.msgError(error.message || "操作失败");
      }
    }
  });
}

/** 删除按钮操作 */
function handleDelete(row) {
  const announcementIds = row?.announcementId ? [row.announcementId] : ids.value;
  if (!announcementIds.length) {
    proxy.$modal.msgError("请先选择要删除的公告");
    return;
  }
  
  proxy.$modal.confirm('是否确认删除选中的公告？').then(async () => {
    await delAnnouncement(announcementIds);
    getList();
    proxy.$modal.msgSuccess("删除成功");
    ids.value = [];
    handleSelectionChange([]);
  }).catch(() => {});
}

/** 导出按钮操作 */
function handleExport() {
  proxy.download('personal/announcement/export', {
    ...queryParams.value
  }, `announcement_${new Date().getTime()}.xlsx`)
}

// 表单重置
function reset() {
  form.value = {
    announcementId: null,
    title: null,
    content: null,
    publisherId: null,
    type: 'public', // 默认公共公告
    status: null,
    createdAt: null,
    deletedAt: null
  };
  proxy.resetForm("announcementRef");
}

// 取消按钮
function cancel() {
  open.value = false;
  reset();
}

// 详情查看
function handleDetails(row) {
  detailData.value = { ...row };
  detailOpen.value = true;
}

// 状态映射
const statusChineseMap = {
  pending: '待审批',
  published: '已发布',
  rejected: '已驳回'
};

// 状态标签类型
const statusTagType = (status) => {
  const typeMap = {
    pending: 'warning',
    published: 'success',
    rejected: 'danger'
  };
  return typeMap[status] || '';
};

// 去除HTML标签
const stripHtml = (html) => {
  if (!html) return '';
  return html.replace(/<[^>]*>/g, '').substring(0, 100) + '...';
};

// 获取当前用户ID
async function getCurrentUserId() {
  try {
    const res = await getInfo()
    return res.user.userId
  } catch (error) {
    console.error('Failed to get user info:', error)
    throw new Error('用户信息获取失败')
  }
}

onMounted(() => {
  getList();
});
</script>

<style scoped>
.content-preview {
  max-height: 60px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.content-full {
  max-width: 100%;
  word-break: break-word;
  line-height: 1.6;
}

.content-full :deep(img) {
  max-width: 100%;
  height: auto;
}

.app-container {
  padding: 20px;
}

.dialog-footer {
  text-align: right;
}

.el-descriptions {
  margin-top: 20px;
}

.el-descriptions-item__label {
  width: 100px;
}
</style>