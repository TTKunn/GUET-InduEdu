<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="社团名" prop="clubId">
        <el-input
          v-model="queryParams.clubName"
          placeholder="请输入社团名字"
          clearable
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="学号" prop="publisherId">
        <el-input
          v-model="queryParams.userName"
          placeholder="请输入申报人学号"
          clearable
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="姓名" prop="publisherId" width="100px">
        <el-input
          v-model="queryParams.nickName"
          placeholder="请输入申报人姓名"
          clearable
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="类型" prop="type">
        <!-- 类型选择框 -->
        <el-select v-model="queryParams.type" placeholder="请选择成果类型" clearable style="width: 100%">
          <el-option v-for="option in typeOptions" :key="option.dictValue" :label="option.dictLabel"
            :value="option.dictValue" />
        </el-select>
      </el-form-item>
      <el-form-item label="成果标题" prop="title">
        <el-input
          v-model="queryParams.title"
          placeholder="请输入成果标题"
          clearable
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="获得日期" style="width: 260px">
        <el-date-picker
          v-model="daterangeAchieveDate"
          value-format="YYYY-MM-DD"
          type="daterange"
          range-separator="-"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
        ></el-date-picker>
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
          v-hasPermi="['manage:achievement:add']"
        >新增</el-button>
      </el-col> -->
      <el-col :span="1.5">
        <el-button
          type="success"
          plain
          icon="Edit"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['manage:achievement:edit']"
        >修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="Delete"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['manage:achievement:remove']"
        >删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="Download"
          @click="handleExport"
          v-hasPermi="['manage:achievement:export']"
        >导出</el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="achievementList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="序号" type="index" align="center" prop="achievementId" width="55" />
      <el-table-column label="社团" align="center" prop="clubName" show-overflow-tooltip/>
      <el-table-column label="申报人" align="center" prop="userName"  width="60" show-overflow-tooltip/>
      <el-table-column label="申报人" align="center" prop="nickName" width="70" />
      <el-table-column label="成果标题" align="center" prop="title" show-overflow-tooltip />
      <el-table-column label="成果类型" prop="type" align="center">
        <template #default="scope">
          {{ typeOptions.find(option => option.dictValue === scope.row.type)?.dictLabel || '--' }}
        </template>
      </el-table-column>
      <!-- <el-table-column label="详细描述" align="center" prop="description" show-overflow-tooltip /> -->
      <el-table-column label="获得日期" align="center" prop="achieveDate" width="120">
        <template #default="scope">
          <span>{{ parseTime(scope.row.achieveDate, '{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="证书地址" align="center" prop="certificateUrl" width="100">
        <template #default="scope">
          <image-preview :src="scope.row.certificateUrl" :width="50" :height="50"/>
        </template>
      </el-table-column>
      <el-table-column label="核验状态" align="center" prop="status" >
        <template #default="scope">
          <el-tag :type="statusTagType(scope.row.status)">
            {{ statusChineseMap[scope.row.status] || scope.row.status }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width" width="250px">
        <template #default="scope">
          <el-button link type="primary" @click="handleDetails(scope.row)">详情</el-button>
          <el-button link type="primary" @click="handleUpdate(scope.row)" v-hasPermi="['manage:achievement:edit']">修改</el-button>
          <el-button link type="primary" @click="handleDelete(scope.row)" v-hasPermi="['manage:achievement:remove']">删除</el-button>
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

    <!-- 添加或修改成果管理对话框 -->
    <el-dialog :title="title" v-model="open" width="500px" append-to-body>
      <el-form ref="achievementRef" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="社团ID" prop="clubId">
          <el-input v-model="form.clubId" placeholder="请输入社团ID" />
        </el-form-item>
        <el-form-item label="发布人ID" prop="publisherId">
          <el-input v-model="form.publisherId" placeholder="请输入发布人ID" />
        </el-form-item>
        <el-form-item label="成果标题" prop="title">
          <el-input v-model="form.title" placeholder="请输入成果标题" />
        </el-form-item>
        <el-form-item label="详细描述" prop="description">
          <el-input v-model="form.description" type="textarea" placeholder="请输入内容" />
        </el-form-item>
        <el-form-item label="获得日期" prop="achieveDate">
          <el-date-picker clearable
            v-model="form.achieveDate"
            type="date"
            value-format="YYYY-MM-DD"
            placeholder="请选择获得日期">
          </el-date-picker>
        </el-form-item>
        <el-form-item label="证书地址" prop="certificateUrl">
          <el-input v-model="form.certificateUrl" type="textarea" placeholder="请输入内容" />
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
        <el-descriptions-item label="社团">{{ detailData.clubName }}</el-descriptions-item>
        <el-descriptions-item label="发布人">{{ detailData.userName }}</el-descriptions-item>
        <el-descriptions-item label="成果标题">{{ detailData.title }}</el-descriptions-item>
        <el-descriptions-item label="成果类型">{{ detailData.type }}</el-descriptions-item>
        <el-descriptions-item label="详细描述">{{ detailData.description }}</el-descriptions-item>
        <el-descriptions-item label="获得日期">{{ parseTime(detailData.achieveDate, '{y}-{m}-{d}') }}</el-descriptions-item>
        <el-descriptions-item label="核验状态">
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

<script setup name="Achievement">
import { listAchievement, getAchievement, delAchievement, addAchievement, updateAchievement } from "@/api/manage/achievement";

const { proxy } = getCurrentInstance();

// 成果类型选项
const typeOptions = ref([
  { dictValue: 'competition', dictLabel: '竞赛' },
  { dictValue: 'project', dictLabel: '项目' },
  { dictValue: 'other', dictLabel: '其他' }
])
const typeList = computed(() => typeOptions.value || []);

// 类型选项声明

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
    userName: null
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
      { required: true, message: "成果类型不能为空", trigger: "change" }
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

/** 查询成果管理列表 */
function getList() {
  loading.value = true;
  queryParams.value.params = {};
  if (daterangeAchieveDate.value && daterangeAchieveDate.value.length === 2) {
    queryParams.value.params["beginAchieveDate"] = daterangeAchieveDate.value[0];
    queryParams.value.params["endAchieveDate"] = daterangeAchieveDate.value[1];
  }
  listAchievement(queryParams.value).then(response => {
    achievementList.value = response.rows;
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
  const _achievementId = row.achievementId || ids.value
  getAchievement(_achievementId).then(response => {
    form.value = response.data;
    open.value = true;
    title.value = "修改成果管理";
  });
}

/** 提交按钮 */
function submitForm() {
  proxy.$refs["achievementRef"].validate(valid => {
    if (valid) {
      if (form.value.achievementId != null) {
        updateAchievement(form.value).then(response => {
          proxy.$modal.msgSuccess("修改成功");
          open.value = false;
          getList();
        });
      } else {
        addAchievement(form.value).then(response => {
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
  const _achievementIds = row.achievementId || ids.value;
  proxy.$modal.confirm('是否确认删除成果管理编号为"' + _achievementIds + '"的数据项？').then(function() {
    return delAchievement(_achievementIds);
  }).then(() => {
    getList();
    proxy.$modal.msgSuccess("删除成功");
  }).catch((error) => {
    console.error("删除失败:", error);
    proxy.$modal.msgError("删除失败");
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

getList();

const statusChineseMap = {
  pending: '待核验',
  published: '已核验',
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
</script>
