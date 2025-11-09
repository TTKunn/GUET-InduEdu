<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch" label-width="80px">
      <el-form-item label="活动名称" prop="name">
        <el-input v-model="queryParams.name" placeholder="请输入活动名称" clearable @keyup.enter="handleQuery" />
      </el-form-item>
      <el-form-item label="活动类型" prop="visibility">
        <el-select 
          v-model="queryParams.visibility" 
          placeholder="全部类型" 
          clearable
          style="width: 120px"
        >
          <el-option label="公开活动" value="public" />
          <el-option label="内部活动" value="internal" />
        </el-select>
      </el-form-item>
      <el-form-item label="负责人" prop="organizer">
        <el-input v-model="queryParams.userName" placeholder="学号" clearable style="width: 120px" />
        <el-input v-model="queryParams.nickName" placeholder="姓名" clearable style="width: 120px; margin-left: 10px" />
      </el-form-item>
      <el-form-item label="审批状态" prop="status">
        <el-select v-model="queryParams.status" placeholder="全部状态" clearable style="width: 120px">
          <el-option label="待审批" value="pending" />
          <el-option label="已通过" value="published" />
          <el-option label="未通过" value="rejected" />
        </el-select>
      </el-form-item>
      <el-form-item label="开始时间" style="width: 273px">
        <el-date-picker v-model="daterangeStartTime" value-format="YYYY-MM-DD HH:mm" type="datetimerange"
          range-separator="-" start-placeholder="开始日期和时间" end-placeholder="结束日期和时间"></el-date-picker>
      </el-form-item>
      <el-form-item label="结束时间" style="width: 280px">
        <el-date-picker v-model="daterangeEndTime" value-format="YYYY-MM-DD HH:mm" type="datetimerange"
          range-separator="-" start-placeholder="开始日期和时间" end-placeholder="结束日期和时间"></el-date-picker>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
        <el-button icon="Refresh" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button 
          type="primary" 
          plain 
          icon="Plus" 
          @click="handleAdd" 

        >
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

        >
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

        >
          删除
        </el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button 
          type="warning" 
          plain 
          icon="Download" 
          @click="handleExport"

        >
          导出
        </el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="handleQuery" />
    </el-row>

    <!-- 活动表格 -->
    <el-table
      v-loading="loading"
      :data="activityList"
      @selection-change="handleSelectionChange"
      :row-key="row => row.activityId"
      style="width: 100%"
    >
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="序号" type="index" align="center" width="60" />
      <el-table-column label="活动名称" align="center" prop="name" min-width="150" show-overflow-tooltip />
      <el-table-column label="活动类型" align="center" prop="visibility" width="100">
        <template #default="{row}">
          <el-tag :type="row.visibility === 'public' ? '' : 'success'">
            {{ row.visibility === 'public' ? '公开' : '内部' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="活动描述" align="center" min-width="180" show-overflow-tooltip>
        <template #default="{row}">
          <div class="content-preview">{{ row.description || '无描述' }}</div>
        </template>
      </el-table-column>
      <el-table-column label="负责人" align="center" width="150">
        <template #default="{row}">
          <div>{{ row.userName }} {{ row.nickName }}</div>
        </template>
      </el-table-column>
      <el-table-column label="活动状态" align="center" width="100">
        <template #default="{row}">
          <el-tag :type="getActivityStatusType(row.startTime, row.endTime)">
            {{ getActivityStatusLabel(row.startTime, row.endTime) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="审批状态" align="center" prop="status" width="100">
        <template #default="{row}">
          <el-tag :type="statusTagType(row.status)">
            {{ statusChineseMap[row.status] || row.status }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="开始时间" align="center" prop="startTime" width="150">
        <template #default="{row}">
          {{ parseTime(row.startTime, '{y}-{m}-{d}') }}
        </template>
      </el-table-column>
      <el-table-column label="结束时间" align="center" prop="endTime" width="150">
        <template #default="{row}">
          {{ parseTime(row.endTime, '{y}-{m}-{d}') }}
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" width="180" fixed="right">
        <template #default="{row}">
          <el-button link type="primary" @click="handleDetails(row)">详情</el-button>
          <el-button 
            link 
            type="primary" 
            @click="handleUpdate(row)"
            v-hasPermi="['manage:activity:edit']"
          >
            修改
          </el-button>
          <el-button 
            link 
            type="danger" 
            @click="handleDelete(row)"
            v-hasPermi="['manage:activity:remove']"
          >
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

    <!-- 添加或修改活动对话框 -->
    <el-dialog :title="title" v-model="open" width="700px" append-to-body>
      <el-form ref="activityRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="活动名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入活动名称" />
        </el-form-item>
        <el-form-item label="活动类型" prop="visibility" v-if="!form.activityId">
          <el-radio-group v-model="form.visibility">
            <el-radio label="public">公开活动</el-radio>
            <el-radio label="internal">内部活动</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="活动描述" prop="description">
          <el-input 
            v-model="form.description" 
            type="textarea" 
            :rows="4" 
            placeholder="请输入活动描述" 
            show-word-limit
            maxlength="500"
          />
        </el-form-item>
        <el-form-item label="活动地点" prop="location">
          <el-input v-model="form.location" placeholder="请输入活动地点" />
        </el-form-item>
        <el-form-item label="开始时间" prop="startTime">
          <el-date-picker 
            v-model="form.startTime" 
            type="datetime"
            placeholder="请选择开始时间"
            value-format="YYYY-MM-DD HH:mm:ss"
            :disabled-date="disabledStartDate"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="结束时间" prop="endTime">
          <el-date-picker 
            v-model="form.endTime" 
            type="datetime"
            placeholder="请选择结束时间"
            value-format="YYYY-MM-DD HH:mm:ss"
            :disabled-date="disabledEndDate"
            style="width: 100%"
          />
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
    <el-dialog title="活动详情" v-model="detailOpen" width="700px" append-to-body>
      <el-descriptions :column="1" border>
        <el-descriptions-item label="活动名称">{{ detailData.name }}</el-descriptions-item>
        <el-descriptions-item label="活动类型">
          {{ detailData.visibility === 'public' ? '公开活动' : '内部活动' }}
        </el-descriptions-item>
        <el-descriptions-item label="活动描述">
          <div class="content-full">{{ detailData.description || '无描述' }}</div>
        </el-descriptions-item>
        <el-descriptions-item label="活动地点">{{ detailData.location }}</el-descriptions-item>
        <el-descriptions-item label="负责人">
          {{ detailData.userName }} ({{ detailData.nickName }})
        </el-descriptions-item>
        <el-descriptions-item label="开始时间">
          {{ parseTime(detailData.startTime, '{y}-{m}-{d} {h}:{i}') }}
        </el-descriptions-item>
        <el-descriptions-item label="结束时间">
          {{ parseTime(detailData.endTime, '{y}-{m}-{d} {h}:{i}') }}
        </el-descriptions-item>
        <el-descriptions-item label="活动状态">
          <el-tag :type="getActivityStatusType(detailData.startTime, detailData.endTime)">
            {{ getActivityStatusLabel(detailData.startTime, detailData.endTime) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="审批状态">
          <el-tag :type="statusTagType(detailData.status)">
            {{ statusChineseMap[detailData.status] || detailData.status }}
          </el-tag>
        </el-descriptions-item>
      </el-descriptions>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="detailOpen = false">关 闭</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup name="Activity">
import { listActivity, getActivity, delActivity, addActivity, updateActivity } from "@/api/personal/activity";
import { getInfo } from '@/api/login'
import { selectClubIdByUserId } from '@/api/personal/club'
import dayjs from 'dayjs'
const { proxy } = getCurrentInstance();

const activityList = ref([]);
const loading = ref(true);
const ids = ref([]);
const single = ref(true);
const multiple = ref(true);
const total = ref(0);
const title = ref("");
const open = ref(false);
const detailOpen = ref(false);
const showSearch = ref(true);
const daterangeStartTime = ref([]);
const daterangeEndTime = ref([]);

const data = reactive({
  form: {
    visibility: 'public' // 默认公开活动
  },
  queryParams: {
    pageNum: 1,
    pageSize: 10,
    name: undefined,
    userName: undefined,
    nickName: undefined,
    status: undefined,
    visibility: undefined,
    clubId: undefined
  },
  rules: {
    name: [{ required: true, message: "活动名称不能为空", trigger: "blur" }],
    description: [{ required: true, message: "活动描述不能为空", trigger: "blur" }],
    location: [{ required: true, message: "活动地点不能为空", trigger: "blur" }],
    startTime: [{ required: true, message: "请选择开始时间", trigger: "change" }],
    endTime: [{ required: true, message: "请选择结束时间", trigger: "change" }],
    visibility: [{ required: true, message: "请选择活动类型", trigger: "change" }]
  }
});

const { form, queryParams, rules } = toRefs(data);
const detailData = ref({});

/** 查询活动列表 */
async function getList() {
  loading.value = true;
  
  // 设置时间范围参数
  queryParams.value.params = {};
  if (daterangeStartTime.value && daterangeStartTime.value.length === 2) {
    queryParams.value.params.beginStartTime = daterangeStartTime.value[0];
    queryParams.value.params.endStartTime = daterangeStartTime.value[1];
  }
  if (daterangeEndTime.value && daterangeEndTime.value.length === 2) {
    queryParams.value.params.beginEndTime = daterangeEndTime.value[0];
    queryParams.value.params.endEndTime = daterangeEndTime.value[1];
  }
  
  try {
    const userId = await getCurrentUserId();
    const clubId = await selectClubIdByUserId(userId);
    queryParams.value.clubId = clubId;
    
    const response = await listActivity(queryParams.value);
    activityList.value = response.rows;
    total.value = response.total;
  } catch (error) {
    proxy.$modal.msgError("获取活动列表失败，请稍后重试");
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
  daterangeStartTime.value = [];
  daterangeEndTime.value = [];
  proxy.resetForm("queryRef");
  queryParams.value = {
    pageNum: 1,
    pageSize: 10,
    name: undefined,
    userName: undefined,
    nickName: undefined,
    status: undefined,
    visibility: undefined,
    clubId: queryParams.value.clubId // 保留社团ID
  };
  handleQuery();
}

/** 多选框选中数据 */
function handleSelectionChange(selection) {
  ids.value = selection.map(item => item.activityId);
  single.value = selection.length !== 1;
  multiple.value = !selection.length;
}

/** 新增按钮操作 */
function handleAdd() {
  reset();
  open.value = true;
  title.value = "添加活动";
}

/** 修改按钮操作 */
function handleUpdate(row) {
  reset();
  const activityId = row?.activityId || ids.value[0];
  if (!activityId) {
    proxy.$modal.msgError("请先选择要修改的活动");
    return;
  }
  
  getActivity(activityId).then(response => {
    form.value = {
      ...response.data,
      startTime: dayjs(response.data.startTime).format('YYYY-MM-DD HH:mm:ss'),
      endTime: dayjs(response.data.endTime).format('YYYY-MM-DD HH:mm:ss')
    };
    open.value = true;
    title.value = "修改活动";
  }).catch(error => {
    proxy.$modal.msgError("获取活动详情失败");
    console.error(error);
  });
}

/** 提交按钮 */
async function submitForm() {
  await proxy.$refs["activityRef"].validate(async (valid) => {
    if (valid) {
      try {
        if (form.value.activityId != null) {
          await updateActivity(form.value);
          proxy.$modal.msgSuccess("修改成功");
        } else {
          const userId = await getCurrentUserId();
          const clubId = await selectClubIdByUserId(userId);
          form.value.organizerId = userId;
          form.value.clubId = clubId;
          form.value.status = 'pending'; // 默认待审批状态
          await addActivity(form.value);
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
  const activityIds = row?.activityId ? [row.activityId] : ids.value;
  if (!activityIds.length) {
    proxy.$modal.msgError("请先选择要删除的活动");
    return;
  }
  
  proxy.$modal.confirm('是否确认删除选中的活动？').then(async () => {
    await delActivity(activityIds);
    getList();
    proxy.$modal.msgSuccess("删除成功");
    ids.value = [];
    handleSelectionChange([]);
  }).catch(() => {});
}

/** 导出按钮操作 */
function handleExport() {
  proxy.download('manage/activity/export', {
    ...queryParams.value
  }, `activity_${new Date().getTime()}.xlsx`)
}

// 表单重置
function reset() {
  form.value = {
    activityId: null,
    name: null,
    description: null,
    location: null,
    startTime: null,
    endTime: null,
    organizerId: null,
    clubId: null,
    visibility: 'public', // 默认公开活动
    status: null
  };
  proxy.resetForm("activityRef");
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
  published: '已通过',
  rejected: '未通过'
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

// 活动状态判断
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

const getActivityStatusType = (startTime, endTime) => {
  const now = new Date();
  const start = new Date(startTime);
  const end = new Date(endTime);

  if (now < start) {
    return 'warning'; // 未开始
  } else if (now >= start && now < end) {
    return 'success'; // 进行中
  } else {
    return 'info'; // 已结束
  }
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

// 禁用开始时间（不能选择当前时间之前的日期）
const disabledStartDate = (time) => {
  return time.getTime() < Date.now() - 24 * 60 * 60 * 1000;
};

// 禁用结束时间（不能选择开始时间之前的日期）
const disabledEndDate = (time) => {
  if (!form.value.startTime) return time.getTime() < Date.now() - 24 * 60 * 60 * 1000;
  const startTime = new Date(form.value.startTime).getTime();
  return time.getTime() < startTime;
};

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