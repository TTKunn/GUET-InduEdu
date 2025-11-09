<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="举办方" prop="clubId">
        <el-input v-model="queryParams.clubName" placeholder="请输入举办方社团名称" clearable @keyup.enter="handleQuery" />
      </el-form-item>
      <el-form-item label="活动名称" prop="name">
        <el-input v-model="queryParams.name" placeholder="请输入活动名称" clearable @keyup.enter="handleQuery" />
      </el-form-item>
      <el-form-item label="开始时间" style="width: 260px">
        <el-date-picker v-model="daterangeStartTime" value-format="YYYY-MM-DD HH:mm" type="datetimerange"
          range-separator="-" start-placeholder="开始日期和时间" end-placeholder="结束日期和时间"></el-date-picker>
      </el-form-item>
      <el-form-item label="结束时间" style="width: 260px">
        <el-date-picker v-model="daterangeEndTime" value-format="YYYY-MM-DD HH:mm" type="datetimerange"
          range-separator="-" start-placeholder="开始日期和时间" end-placeholder="结束日期和时间"></el-date-picker>
      </el-form-item>
      <el-form-item label="活动地点" prop="location">
        <el-input v-model="queryParams.location" placeholder="请输入活动地点" clearable @keyup.enter="handleQuery" />
      </el-form-item>
      <el-form-item label="姓名" prop="organizerId">
        <el-input v-model="queryParams.nickName" placeholder="请输入负责人姓名" clearable @keyup.enter="handleQuery" />
      </el-form-item>
      <el-form-item label="学号" prop="organizerId">
        <el-input v-model="queryParams.userName" placeholder="请输入负责人学号" clearable @keyup.enter="handleQuery" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
        <el-button icon="Refresh" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button type="primary" plain icon="Plus" @click="handleAdd" v-hasPermi="['manage:activity:add']">新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button type="success" plain icon="Edit" :disabled="single" @click="handleUpdate"
          v-hasPermi="['manage:activity:edit']">修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button type="danger" plain icon="Delete" :disabled="multiple" @click="handleDelete"
          v-hasPermi="['manage:activity:remove']">删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button type="warning" plain icon="Download" @click="handleExport"
          v-hasPermi="['manage:activity:export']">导出</el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="activityList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="50" align="center" />
      <el-table-column label="序号" type="index" align="center" prop="activityId" width="50" />
      <el-table-column label="社团名字" align="center" prop="clubName" show-overflow-tooltip/>
      <el-table-column label="活动名称" align="center" prop="name" />
      <!-- <el-table-column label="活动描述" align="center" prop="description" /> -->
      <el-table-column label="活动地点" align="center" prop="location" width="100" show-overflow-tooltip />
      <el-table-column label="负责学号" align="center" prop="userName" width="100" />
      <el-table-column label="负责人" align="center" prop="nickName" />
      <el-table-column label="开始时间" align="center" prop="startTime" width="160">
        <template #default="scope">
          <span>{{ parseTime(scope.row.startTime, '{y}-{m}-{d} {h}:{i}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="结束时间" align="center" prop="endTime" width="150">
        <template #default="scope">
          <span>{{ parseTime(scope.row.endTime, '{y}-{m}-{d} {h}:{i}') }}</span>
        </template>
      </el-table-column>
      <!-- 判断活动是否已经结束（若当前系统时间大于结束时间，则活动状态为已结束） -->
      <el-table-column label="活动状态" align="center">
        <template #default="scope">
          <el-tag :type="getActivityStatusType(scope.row.startTime, scope.row.endTime)">
            {{ getActivityStatusLabel(scope.row.startTime, scope.row.endTime) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="审批状态" align="center" prop="status">
        <template #default="scope">
          <el-tag :type="statusTagType(scope.row.status)">
            {{ statusChineseMap[scope.row.status] || scope.row.status }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width" width="180">
        <template #default="scope">
          <el-button link type="primary" @click="handleDetails(scope.row)">详情</el-button>
          <el-button link type="primary" @click="handleUpdate(scope.row)"
            v-hasPermi="['manage:activity:edit']">修改</el-button>
          <el-button link type="primary" @click="handleDelete(scope.row)"
            v-hasPermi="['manage:activity:remove']">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total > 0" :total="total" v-model:page="queryParams.pageNum" v-model:limit="queryParams.pageSize"
      @pagination="getList" />

    <!-- 添加或修改活动管理对话框 -->
    <el-dialog :title="title" v-model="open" width="500px" append-to-body>
      <el-form ref="activityRef" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="活动名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入活动名称" />
        </el-form-item>
        <el-form-item label="活动描述" prop="description">
          <el-input v-model="form.description" type="textarea" placeholder="请输入内容" />
        </el-form-item>

        <el-form-item label="开始时间" prop="startTime">
          <el-date-picker clearable v-model="form.startTime" type="datetime" value-format="YYYY-MM-DD HH:mm:ss"
            placeholder="请选择开始时间" style="width: 100%;" />
        </el-form-item>

        <el-form-item label="结束时间" prop="endTime">
          <el-date-picker clearable v-model="form.endTime" type="datetime" value-format="YYYY-MM-DD HH:mm:ss"
            placeholder="请选择结束时间" style="width: 100%;" />
        </el-form-item>

        <el-form-item label="活动地点" prop="location">
          <el-input v-model="form.location" placeholder="请输入活动地点" />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button type="primary" @click="submitForm">确 定</el-button>
          <el-button @click="cancel">取 消</el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 详情对话框 -->
    <el-dialog title="活动详情" v-model="detailOpen" width="600px" append-to-body>
      <el-descriptions :column="1" border>
        <el-descriptions-item label="活动ID">{{ detailData.activityId }}</el-descriptions-item>
        <el-descriptions-item label="社团">{{ detailData.clubName }}</el-descriptions-item>
        <el-descriptions-item label="活动名称">{{ detailData.name }}</el-descriptions-item>
        <el-descriptions-item label="活动描述">{{ detailData.description }}</el-descriptions-item>
        <el-descriptions-item label="活动地点">{{ detailData.location }}</el-descriptions-item>
        <el-descriptions-item label="负责人">{{ detailData.userName }}</el-descriptions-item>
        <el-descriptions-item label="开始时间">{{ parseTime(detailData.startTime, '{y}-{m}-{d} {h}:{i}')
        }}</el-descriptions-item>
        <el-descriptions-item label="结束时间">{{ parseTime(detailData.endTime, '{y}-{m}-{d} {h}:{i}')
        }}</el-descriptions-item>
        <el-descriptions-item label="活动状态">
          <el-tag :type="getActivityStatusType(detailData.endTime)">
            {{ getActivityStatusLabel(detailData.endTime) }}
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
import { listActivity, getActivity, delActivity, addActivity, updateActivity } from "@/api/manage/activity";

const { proxy } = getCurrentInstance();

const activityList = ref([]);
const open = ref(false);
const loading = ref(true);
const showSearch = ref(true);
const ids = ref([]);
const single = ref(true);
const multiple = ref(true);
const total = ref(0);
const title = ref("");
const daterangeStartTime = ref([]);
const daterangeEndTime = ref([]);
const detailOpen = ref(false);
const detailData = ref({});

const data = reactive({
  form: {},
  queryParams: {
    pageNum: 1,
    pageSize: 10,
    clubId: null,
    name: null,
    description: null,
    startTime: null,
    endTime: null,
    location: null,
    organizerId: null,
    status: null,
    nickName: null,
    clubName: null,
    userName: null
  },
  rules: {
    name: [
      { required: true, message: "活动名称不能为空", trigger: "blur" }
    ],
    description: [
      { required: true, message: "活动描述不能为空", trigger: "blur" }
    ],
    startTime: [
      { required: true, message: "开始时间不能为空", trigger: "blur" }
    ],
    endTime: [
      { required: true, message: "结束时间不能为空", trigger: "blur" }
    ],
    location: [
      { required: true, message: "活动地点不能为空", trigger: "blur" }
    ],
  }
});

const { queryParams, form, rules } = toRefs(data);

/** 查询活动管理列表 */
function getList() {
  loading.value = true;
  queryParams.value.params = {};
  if (null != daterangeStartTime && '' != daterangeStartTime) {
    queryParams.value.params["beginStartTime"] = daterangeStartTime.value[0];
    queryParams.value.params["endStartTime"] = daterangeStartTime.value[1];
  }
  if (null != daterangeEndTime && '' != daterangeEndTime) {
    queryParams.value.params["beginEndTime"] = daterangeEndTime.value[0];
    queryParams.value.params["endEndTime"] = daterangeEndTime.value[1];
  }
  listActivity(queryParams.value).then(response => {
    activityList.value = response.rows;
    total.value = response.total;
    loading.value = false;
  });
}

// 取消按钮
function cancel() {
  open.value = false;
  reset();
}

// 表单重置
function reset() {
  form.value = {
    activityId: null,
    clubId: null,
    name: null,
    description: null,
    startTime: null,
    endTime: null,
    location: null,
    organizerId: null,
    visibility: null,
    status: null,
    deletedAt: null
  };
  proxy.resetForm("activityRef");
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
  queryParams.value = {};
  handleQuery();
}

// 多选框选中数据
function handleSelectionChange(selection) {
  ids.value = selection.map(item => item.activityId);
  single.value = selection.length != 1;
  multiple.value = !selection.length;
}

/** 新增按钮操作 */
function handleAdd() {
  reset();
  open.value = true;
  title.value = "添加活动管理";
}

/** 修改按钮操作 */
function handleUpdate(row) {
  reset();
  const _activityId = row.activityId || ids.value
  getActivity(_activityId).then(response => {
    form.value = response.data;
    open.value = true;
    title.value = "修改活动管理";
  });
}

/** 提交按钮 */
function submitForm() {
  proxy.$refs["activityRef"].validate(valid => {
    if (valid) {
      if (form.value.activityId != null) {
        updateActivity(form.value).then(response => {
          proxy.$modal.msgSuccess("修改成功");
          open.value = false;
          getList();
        });
      } else {
        addActivity(form.value).then(response => {
          proxy.$modal.msgSuccess("新增成功");
          open.value = false;
          getList();
        });
      }
    }
  });
}

/** 删除按钮操作 */
function handleDelete(row) {
  const _activityIds = row.activityId || ids.value;
  proxy.$modal.confirm('是否确认删除活动管理编号为"' + _activityIds + '"的数据项？').then(function () {
    return delActivity(_activityIds);
  }).then(() => {
    getList();
    proxy.$modal.msgSuccess("删除成功");
  }).catch(() => { });
}

/** 导出按钮操作 */
function handleExport() {
  proxy.download('manage/activity/export', {
    ...queryParams.value
  }, `activity_${new Date().getTime()}.xlsx`)
}

getList();

const statusChineseMap = {
  pending: '待审批',
  published: '已通过',
  rejected: '未通过'
};

const statusTagType = (status) => {
  const typeMap = {
    pending: 'warning',
    published: 'success',
    rejected: 'danger'
  };
  return typeMap[status] || '';
};

/** 详情按钮操作 */
function handleDetails(row) {
  detailData.value = row;
  detailOpen.value = true;
}

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
    return 'warning'; // For '未开始'
  } else if (now >= start && now < end) {
    return 'success'; // For '进行中'
  } else {
    return 'info'; // For '已结束'
  }
};
</script>
