<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="学号" prop="publisherId">
        <el-input v-model="queryParams.userName" placeholder="请输入申报人学号" clearable @keyup.enter="handleQuery" />
      </el-form-item>
      <el-form-item label="姓名" prop="publisherId" width="100px">
        <el-input v-model="queryParams.nickName" placeholder="请输入申报人姓名" clearable @keyup.enter="handleQuery" />
      </el-form-item>
      <el-form-item label="标题" prop="title">
        <el-input v-model="queryParams.title" placeholder="请输入成果标题" clearable @keyup.enter="handleQuery" />
      </el-form-item>
      <el-form-item label="类型" prop="type">
        <el-select v-model="queryParams.type" placeholder="请选择成果类型" clearable style="width: 100%">
          <el-option v-for="option in typeOptions" :key="option.dictValue" :label="option.dictLabel"
            :value="option.dictValue" />
        </el-select>
      </el-form-item>
      <el-form-item label="获得日期" style="width: 308px">
        <el-date-picker v-model="daterangeAchieveDate" value-format="YYYY-MM-DD" type="daterange" range-separator="-"
          start-placeholder="开始日期" end-placeholder="结束日期"></el-date-picker>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
        <el-button icon="Refresh" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button type="primary" plain icon="Plus" @click="handleAdd"
          >新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button type="success" plain icon="Edit" :disabled="single" @click="handleUpdate"
          >修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button type="danger" plain icon="Delete" :disabled="multiple" @click="handleDelete"
          >删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button type="warning" plain icon="Download" @click="handleExport"
          >导出</el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="achievementList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="序号" type="index" align="center" prop="achievementId" width="55" />
      <el-table-column label="发布人学号" align="center" prop="userName" width="90" />
      <el-table-column label="发布人姓名" align="center" prop="nickName" width="90" />
      <el-table-column label="成果标题" align="center" prop="title" show-overflow-tooltip />
      <el-table-column label="成果类型" prop="type" align="center">
        <template #default="scope">
          {{ typeList.find(option => option.dictValue === scope.row.type)?.dictLabel || '--' }}
        </template>
      </el-table-column>
      <el-table-column label="详细描述" align="center" prop="description" show-overflow-tooltip />
      <el-table-column label="获得日期" align="center" prop="achieveDate" width="160">
        <template #default="scope">
          <span>{{ parseTime(scope.row.achieveDate, '{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="证书地址" align="center" prop="certificateUrl" width="100">
        <template #default="scope">
          <image-preview :src="scope.row.certificateUrl" :width="50" :height="50" />
        </template>
      </el-table-column>
      <el-table-column label="核验状态" align="center" prop="status">
        <template #default="scope">
          <el-tag :type="statusTagType(scope.row.status)">
            {{ statusChineseMap[scope.row.status] || scope.row.status }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width" width="250px">
        <template #default="scope">
          <el-button link type="primary" @click="handleDetails(scope.row)">详情</el-button>
          <el-button link type="primary" @click="handleUpdate(scope.row)"
            v-hasPermi="['manage:achievement:edit']">修改</el-button>
          <el-button link type="primary" @click="showParticipants(scope.row.participants)"
            v-hasPermi="['manage:achievement:view']">参与人员</el-button>
          <el-button link type="primary" @click="handleDelete(scope.row)"
            v-hasPermi="['manage:achievement:remove']">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total > 0" :total="total" v-model:page="queryParams.pageNum" v-model:limit="queryParams.pageSize"
      @pagination="getList" />

    <!-- 添加或修改成果管理对话框 -->
    <el-dialog :title="title" v-model="open" width="500px" append-to-body>
      <el-form ref="achievementRef" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="成果标题" prop="title">
          <el-input v-model="form.title" placeholder="请输入成果标题" />
        </el-form-item>
        <el-form-item label="详细描述" prop="description">
          <el-input v-model="form.description" type="textarea" placeholder="请输入内容" />
        </el-form-item>
        <el-form-item label="成果类型" prop="type">
          <el-select v-model="form.type" placeholder="请选择成果类型" clearable style="width: 100%">
            <el-option v-for="option in typeOptions" :key="option.dictValue" :label="option.dictLabel"
              :value="option.dictValue" />
          </el-select>
        </el-form-item>
        <el-form-item label="获得日期" prop="achieveDate">
          <el-date-picker clearable v-model="form.achieveDate" type="date" value-format="YYYY-MM-DD"
            placeholder="请选择获得日期">
          </el-date-picker>
        </el-form-item>
        <el-form-item label="证书地址" prop="certificateUrl">
          <image-upload v-model="form.certificateUrl" />
        </el-form-item>
        <el-form-item label="参与人员" prop="participantIds">
          <el-select v-model="form.participantIds" multiple filterable collapse-tags collapse-tags-tooltip
            placeholder="请选择参与人员" style="width: 100%">
            <el-option v-for="member in memberList" :key="member.userId" :label="member.nickname || member.userName"
              :value="member.userId" />
          </el-select>
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
    <el-dialog title="成果详情" v-model="detailOpen" width="600px" append-to-body>
      <el-descriptions :column="1" border>
        <el-descriptions-item label="成果ID">{{ detailData.achievementId }}</el-descriptions-item>
        <el-descriptions-item label="发布人">{{ detailData.userName }}</el-descriptions-item>
        <el-descriptions-item label="成果标题">{{ detailData.title }}</el-descriptions-item>
        <el-descriptions-item label="成果类型">
          {{ typeOptions.find(o => o.dictValue === detailData.type)?.dictLabel || '--' }}
        </el-descriptions-item>
        <el-descriptions-item label="详细描述">{{ detailData.description }}</el-descriptions-item>
        <el-descriptions-item label="获得日期">{{ parseTime(detailData.achieveDate, '{y}-{m}-{d}') }}</el-descriptions-item>
        <el-descriptions-item label="核验状态">
          <el-tag :type="statusTagType(detailData.status)">
            {{ statusChineseMap[detailData.status] || detailData.status }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="证书">
          <div v-if="detailData.certificateUrl">
            <el-image :src="detailData.certificateUrl" :preview-src-list="[detailData.certificateUrl]" fit="contain"
              style="max-width: 200px; max-height: 150px;" hide-on-click-modal>
              <template #error>
                <div class="image-error">无法加载图片</div>
              </template>
            </el-image>
          </div>
          <span v-else>--</span>
        </el-descriptions-item>
      </el-descriptions>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="detailOpen = false">关 闭</el-button>
        </div>
      </template>
    </el-dialog>
    
    <!-- 参与人员弹窗 -->
    <el-dialog 
      title="参与人员列表" 
      v-model="participantDialogVisible" 
      width="500px"
      append-to-body>
      <el-table :data="currentParticipants" border style="width: 100%">
        <el-table-column prop="userName" label="学号" align="center" width="120"/>
        <el-table-column prop="nickName" label="姓名" align="center"/>
        <!-- <el-table-column prop="deptName" label="部门" align="center"/>
        <el-table-column prop="position" label="职位" align="center"/> -->
      </el-table>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="participantDialogVisible = false">关 闭</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup name="Achievement">
import { listAchievement, getAchievement, delAchievement, addAchievement, updateAchievement } from "@/api/personal/achievement";
import { getInfo } from '@/api/login'
import { selectClubIdByUserId } from '@/api/personal/club'
import { listMembersByClubId } from '@/api/personal/membership'
const { proxy } = getCurrentInstance();

// 状态管理
const participantDialogVisible = ref(false)
const currentParticipants = ref([])

// 类型选项声明
const typeOptions = ref([
  { dictValue: 'competition', dictLabel: '竞赛' },
  { dictValue: 'project', dictLabel: '项目' },
  { dictValue: 'other', dictLabel: '其他' }
]);

// 计算属性
const typeList = computed(() => typeOptions.value || []);

const achievementList = ref([]);
const open = ref(false);
const loading = ref(true);
const showSearch = ref(true);
const ids = ref([]);
const single = ref(true);
const multiple = ref(true);
const total = ref(0);
const title = ref("");
const daterangeAchieveDate = ref([]);
const detailOpen = ref(false);
const detailData = ref({});

const data = reactive({
  form: {},
  queryParams: {
    pageNum: 1,
    pageSize: 10,
    clubId: null,
    publisherId: null,
    title: null,
    type: null,
    achieveDate: null,
    status: null,
    nickName: null,
    clubName: null,
    userName: null,
    achieveDate: null,
  },
  rules: {
    clubId: [
      { required: true, message: "社团ID不能为空", trigger: "blur" }
    ],
    publisherId: [
      { required: true, message: "发布人ID不能为空", trigger: "blur" }
    ],
    title: [
      { required: true, message: "成果标题不能为空", trigger: "blur" }
    ],
    type: [
      { required: true, message: "成果类型不能为空", trigger: "blur" }
    ],
    description: [
      { required: true, message: "详细描述不能为空", trigger: "blur" }
    ],
    achieveDate: [
      { required: true, message: "获得日期不能为空", trigger: "blur" }
    ],
  }
});

const { queryParams, form, rules } = toRefs(data);
const memberList = ref([]);

/** 查询成果管理列表 */
async function getList() {
  loading.value = true;
  queryParams.value.params = {};
  try {
    if (daterangeAchieveDate.value && daterangeAchieveDate.value.length === 2) {
      queryParams.value.params["beginAchieveDate"] = daterangeAchieveDate.value[0];
      queryParams.value.params["endAchieveDate"] = daterangeAchieveDate.value[1];
    }

    const userId = await getCurrentUserId();
    const clubId = await selectClubIdByUserId(userId);

    if (!clubId) {
      throw new Error("用户未加入任何社团");
    }

    queryParams.value.clubId = clubId;
    const response = await listAchievement(queryParams.value);

    achievementList.value = response.rows.map(item => ({
      ...item,
      participants: item.participants || []
    }))
    total.value = response.total;

    // 获取成员列表
    const memberResponse = await listMembersByClubId(clubId);
    memberList.value = memberResponse.data.map(m => ({
      ...m,
      membershipId: m.membershipId,
      displayName: m.nickName || m.userName
    }))
  } catch (error) {
    proxy.$modal.msgError(error.message || "加载失败");
  } finally {
    loading.value = false;
  }
}

// 显示参与人员
const showParticipants = (participants) => {
  currentParticipants.value = participants || []
  participantDialogVisible.value = true
}

// 取消按钮
function cancel() {
  open.value = false;
  reset();
}

// 表单重置
function reset() {
  form.value = {
    achievementId: null,
    clubId: null,
    publisherId: null,
    title: null,
    type: null,
    description: null,
    achieveDate: null,
    certificateUrl: null,
    status: null,
    createdAt: null,
    deletedAt: null
  };
  proxy.resetForm("achievementRef");
}

/** 搜索按钮操作 */
function handleQuery() {
  queryParams.value.pageNum = 1;
  getList();
}

/** 重置按钮操作 */
function resetQuery() {
  daterangeAchieveDate.value = [];
  proxy.resetForm("queryRef");
  queryParams.value = {};
  handleQuery();
}

// 多选框选中数据
function handleSelectionChange(selection) {
  ids.value = selection.map(item => item.achievementId);
  single.value = selection.length != 1;
  multiple.value = !selection.length;
}

/** 新增按钮操作 */
function handleAdd() {
  reset();
  open.value = true;
  title.value = "添加成果管理";
}

/** 修改按钮操作 */
function handleUpdate(row) {
  reset();
  const _achievementId = row?.achievementId || ids.value[0]
  if (!_achievementId) {
    return proxy.$modal.msgError("请选择要修改的记录");
  }
  getAchievement(_achievementId).then(response => {
    form.value = {
      ...response.data,
      type: response.data.type // 确保type字段存在且值正确
    };
    open.value = true;
    title.value = "修改成果管理";
  });
}

/** 提交按钮 */
async function submitForm() {
  proxy.$refs["achievementRef"].validate(async (valid) => {
    if (valid) {
      try {
        if (form.value.achievementId != null) {
          await updateAchievement(form.value);
          proxy.$modal.msgSuccess("修改成功");
        } else {
          const userId = await getCurrentUserId();
          const clubId = await selectClubIdByUserId(userId);
          form.value.publisherId = userId;
          form.value.clubId = clubId;
          await addAchievement(form.value);
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
  const achievementIds = row?.achievementId
    ? [row.achievementId]
    : ids.value;

  if (achievementIds.length === 0) {
    proxy.$modal.msgError("请选择要删除的记录");
    return;
  }

  proxy.$modal.confirm(`确认删除选中的${achievementIds.length}条记录？`).then(async () => {
    await delAchievement(achievementIds);
    await getList();
    proxy.$modal.msgSuccess("删除成功");
  }).catch(error => {
    proxy.$modal.msgError(error.message || "删除取消");
  });
}

/** 详情按钮操作 */
function handleDetails(row) {
  detailData.value = row;
  detailOpen.value = true;
}

/** 导出按钮操作 */
function handleExport() {
  proxy.download('manage/achievement/export', {
    ...queryParams.value
  }, `achievement_${new Date().getTime()}.xlsx`)
}

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

// 状态映射
const statusChineseMap = {
  pending: '待核验',
  published: '已核验',
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

// 格式化时间函数（假设已全局注册）
const parseTime = (time, format) => {
  // 这里简化处理，实际项目中应该使用全局注册的工具函数
  if (!time) return '';
  const date = new Date(time);
  const year = date.getFullYear();
  const month = date.getMonth() + 1;
  const day = date.getDate();
  return format.replace('{y}', year)
               .replace('{m}', month.toString().padStart(2, '0'))
               .replace('{d}', day.toString().padStart(2, '0'));
}

// 初始化加载数据
getList();
</script>

<style>
.image-error {
  padding: 10px;
  color: #f56c6c;
  background-color: #fef0f0;
  border-radius: 4px;
}
</style>    