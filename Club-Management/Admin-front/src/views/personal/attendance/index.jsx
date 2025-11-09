<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="成员学号" prop="userId">
        <el-input v-model="queryParams.userName" placeholder="请输入成员学号" clearable @keyup.enter="handleQuery" />
      </el-form-item>
      <el-form-item label="成员名字" prop="userId">
        <el-input v-model="queryParams.nickName" placeholder="请输入成员名字" clearable @keyup.enter="handleQuery" />
      </el-form-item>
      <el-form-item label="签到时间" style="width: 260px">
        <el-date-picker v-model="daterangeClockInTime" value-format="YYYY-MM-DD HH:mm" type="datetimerange"
          range-separator="-" start-placeholder="开始时间" end-placeholder="结束时间"
          :default-time="[new Date(2000, 1, 1, 0, 0), new Date(2000, 1, 1, 23, 59)]"></el-date-picker>
      </el-form-item>

      <el-form-item label="签退时间" style="width: 260px">
        <el-date-picker v-model="daterangeClockOutTime" value-format="YYYY-MM-DD HH:mm" type="datetimerange"
          range-separator="-" start-placeholder="开始时间" end-placeholder="结束时间"
          :default-time="[new Date(2000, 1, 1, 0, 0), new Date(2000, 1, 1, 23, 59)]"></el-date-picker>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
        <el-button icon="Refresh" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <el-row :gutter="10" class="mb8">
      <!-- <el-col :span="1.5">
        <el-button
          type="primary"
          plain
          icon="Plus"
          @click="handleAdd"
          v-hasPermi="['personal:attendance:add']"
        >新增</el-button>
      </el-col> -->
      <!-- <el-col :span="1.5">
        <el-button
          type="success"
          plain
          icon="Edit"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['personal:attendance:edit']"
        >修改</el-button>
      </el-col> -->
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="Delete"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['personal:attendance:remove']"
        >删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="Download"
          @click="handleExport"
          v-hasPermi="['personal:attendance:export']"
        >导出</el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="attendanceList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="序号" type="index" align="center" prop="attendanceId" width="55" />
      <!-- <el-table-column label="所属社团" align="center" prop="clubName" show-overflow-tooltip/> -->
      <el-table-column label="成员学号" align="center" prop="userName" width="120" />
      <el-table-column label="成员名字" align="center" prop="nickName" width="120" />
      <el-table-column label="签到时间" align="center" prop="clockInTime" width="180">
        <template #default="scope">
          <span>{{ parseTime(scope.row.clockInTime, '{y}-{m}-{d} {h}:{i}:{s}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="签退时间" align="center" prop="clockOutTime" width="180">
        <template #default="scope">
          <span>{{ parseTime(scope.row.clockOutTime, '{y}-{m}-{d} {h}:{i}:{s}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="学习时长" align="center" prop="studyDuration">
        <template #default="scope">
          <span>{{ scope.row.studyDuration }} 分钟</span>
        </template>
      </el-table-column>
      <el-table-column label="考勤状态" align="center" prop="status" />
      <el-table-column label="备注" align="center" prop="notes">
        <template #default="scope">
          <span>{{ scope.row.notes || '暂无备注' }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template #default="scope">
          <el-button link type="primary" @click="handleDetails(scope.row)">详情</el-button>
          <el-button link type="primary" @click="handleDelete(scope.row)"
            v-hasPermi="['manage:attendance:remove']">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    
    <pagination
      v-show="total>0"
      :total="total"
      v-model:page="queryParams.pageNum"
      v-model:limit="queryParams.pageSize"
      @pagination="getList"
    />

    <!-- 添加或修改考勤管理对话框 -->
    <el-dialog :title="title" v-model="open" width="500px" append-to-body>
      <el-form ref="attendanceRef" :model="form" :rules="rules" label-width="80px">
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button type="primary" @click="submitForm">确 定</el-button>
          <el-button @click="cancel">取 消</el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 新增详情对话框 -->
  <el-dialog title="考勤详情" v-model="detailOpen" width="600px" append-to-body>
    <el-descriptions :column="1" border>
      <el-descriptions-item label="所属社团">{{ detailData.clubName }}</el-descriptions-item>
      <el-descriptions-item label="成员学号">{{ detailData.userName }}</el-descriptions-item>
      <el-descriptions-item label="成员名字">{{ detailData.nickName }}</el-descriptions-item>
      <el-descriptions-item label="签到时间">
        {{ parseTime(detailData.clockInTime, '{y}-{m}-{d} {h}:{i}:{s}') }}
      </el-descriptions-item>
      <el-descriptions-item label="签退时间">
        {{ parseTime(detailData.clockOutTime, '{y}-{m}-{d} {h}:{i}:{s}') }}
      </el-descriptions-item>
      <el-descriptions-item label="学习时长">{{ detailData.studyDuration }} 分钟</el-descriptions-item>
      <el-descriptions-item label="考勤状态">{{ detailData.status }}</el-descriptions-item>
      <el-descriptions-item label="备注">{{ detailData.notes || '暂无备注' }}</el-descriptions-item>
    </el-descriptions>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="detailOpen = false">关 闭</el-button>
      </div>
    </template>
  </el-dialog>
  </div>
</template>

<script setup name="Attendance">
import { listAttendance, getAttendance, delAttendance, addAttendance, updateAttendance } from "@/api/personal/attendance";
import { getInfo } from '@/api/login'
import { selectClubIdByUserId } from '@/api/personal/club'
const { proxy } = getCurrentInstance();

const attendanceList = ref([]);
const open = ref(false);
const loading = ref(true);
const showSearch = ref(true);
const ids = ref([]);
const single = ref(true);
const multiple = ref(true);
const total = ref(0);
const title = ref("");
const daterangeClockInTime = ref([]);
const daterangeClockOutTime = ref([]);

const data = reactive({
  form: {},
  queryParams: {
    pageNum: 1,
    pageSize: 10,
    userId: null,
    clockInTime: null,
    clockOutTime: null,
    studyDuration: null,
    status: null,
    notes: null,
    clubId: null
  },
  rules: {
  }
});

const { queryParams, form, rules } = toRefs(data);

/** 查询考勤管理列表 */
async function getList() {
  loading.value = true;
  queryParams.value.params = {};

  if (daterangeClockInTime.value && daterangeClockInTime.value.length === 2) {
    queryParams.value.params["beginClockInTime"] = daterangeClockInTime.value[0];
    queryParams.value.params["endClockInTime"] = daterangeClockInTime.value[1];
  }

  if (daterangeClockOutTime.value && daterangeClockOutTime.value.length === 2) {
    queryParams.value.params["beginClockOutTime"] = daterangeClockOutTime.value[0];
    queryParams.value.params["endClockOutTime"] = daterangeClockOutTime.value[1];
  }

  try {
    const userId = await getCurrentUserId();
    const clubId = await selectClubIdByUserId(userId);
    queryParams.value.clubId = clubId
    // console.log(queryParams.value)
    const response = await listAttendance(queryParams.value);
    attendanceList.value = response.rows;
    total.value = response.total;
    loading.value = false;
  } catch (error) {
    console.error('Failed to fetch attendance list:', error);
    proxy.$modal.msgError("加载失败，请重试");
    loading.value = false;
  }
}
// 取消按钮
function cancel() {
  open.value = false;
  reset();
}

// 表单重置
function reset() {
  form.value = {
    attendanceId: null,
    clubId: null,
    userId: null,
    clockInTime: null,
    clockOutTime: null,
    studyDuration: null,
    status: null,
    notes: null,
    createdAt: null,
    updatedAt: null,
    deletedAt: null
  };
  proxy.resetForm("attendanceRef");
}

/** 搜索按钮操作 */
function handleQuery() {
  queryParams.value.pageNum = 1;
  getList();
}

/** 重置按钮操作 */
function resetQuery() {
  daterangeClockInTime.value = [];
  daterangeClockOutTime.value = [];
  proxy.resetForm("queryRef");
  queryParams.value = {};
  handleQuery();
}

// 多选框选中数据
function handleSelectionChange(selection) {
  ids.value = selection.map(item => item.attendanceId);
  single.value = selection.length != 1;
  multiple.value = !selection.length;
}

/** 新增按钮操作 */
function handleAdd() {
  reset();
  open.value = true;
  title.value = "添加考勤管理";
}

/** 修改按钮操作 */
function handleUpdate(row) {
  reset();
  const _attendanceId = row.attendanceId || ids.value
  getAttendance(_attendanceId).then(response => {
    form.value = response.data;
    open.value = true;
    title.value = "修改考勤管理";
  });
}

/** 提交按钮 */
function submitForm() {
  proxy.$refs["attendanceRef"].validate(valid => {
    if (valid) {
      if (form.value.attendanceId != null) {
        updateAttendance(form.value).then(response => {
          proxy.$modal.msgSuccess("修改成功");
          open.value = false;
          getList();
        });
      } else {
        addAttendance(form.value).then(response => {
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
  const _attendanceIds = row.attendanceId || ids.value;
  proxy.$modal.confirm('是否确认删除考勤管理编号为"' + _attendanceIds + '"的数据项？').then(function() {
    return delAttendance(_attendanceIds);
  }).then(() => {
    getList();
    proxy.$modal.msgSuccess("删除成功");
  }).catch(() => {});
}

/** 导出按钮操作 */
function handleExport() {
  proxy.download('personal/attendance/export', {
    ...queryParams.value
  }, `attendance_${new Date().getTime()}.xlsx`)
}

getList();

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

  // 新增详情相关变量
const detailOpen = ref(false);
const detailData = ref({});

/** 详情按钮操作 */
function handleDetails(row) {
  detailData.value = {
    ...row,
    // 如果需要处理特殊字段可以在这里转换
  };
  detailOpen.value = true;
}
</script>
