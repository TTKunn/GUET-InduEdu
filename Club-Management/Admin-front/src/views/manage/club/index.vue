<template>
  <div class="app-container">
    <!-- 数据查询 -->
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="社团名称" prop="name">
        <el-input v-model="queryParams.name" placeholder="请输入社团名称" clearable @keyup.enter="handleQuery" />
      </el-form-item>

      <el-form-item label="分类搜索" prop="regionId" style="width: 260px">
        <el-select v-model="queryParams.categoryId" placeholder="请选择分类" clearable>
          <el-option v-for="item in categoryList" :key="item.categoryId" :label="item.name"
            :value="item.categoryId"></el-option>
        </el-select>

      </el-form-item>

      <el-form-item label="负责人" prop="leaderId" style="width: 260px">
        <el-select v-model="queryParams.leaderId" placeholder="请选择当前负责人" clearable>
          <el-option v-for="item in userList" :key="item.userId" :label="item.nickName" :value="item.userId"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="所属学院" prop="deptId" style="width: 260px">
        <el-select v-model="queryParams.deptId" placeholder="请选择所属学院" clearable>
          <el-option v-for="item in deptList" :key="item.deptId" :label="item.deptName" :value="item.deptId"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="成立时间" style="width: 260px">
        <el-date-picker v-model="daterangeCreatedAt" value-format="YYYY-MM-DD" type="daterange" range-separator="-"
          start-placeholder="开始日期" end-placeholder="结束日期"></el-date-picker>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
        <el-button icon="Refresh" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>
    <!-- 数据操作 -->
    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button type="primary" plain icon="Plus" @click="handleAdd" v-hasPermi="['manage:club:add']">新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button type="success" plain icon="Edit" :disabled="single" @click="handleUpdate"
          v-hasPermi="['manage:club:edit']">修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button type="danger" plain icon="Delete" :disabled="multiple" @click="handleDelete"
          v-hasPermi="['manage:club:remove']">删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button type="warning" plain icon="Download" @click="handleExport"
          v-hasPermi="['manage:club:export']">导出</el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>
    <!-- 数据展示 -->
    <el-table v-loading="loading" :data="clubList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="序号" align="center" width="50" type="index" prop="clubId" />
      <el-table-column label="LOGO地址" align="center" prop="logoUrl" width="100">
        <template #default="scope">
          <image-preview :src="scope.row.logoUrl" :width="50" :height="50"/>
        </template>
      </el-table-column>
      <el-table-column label="社团名称" align="center" prop="clubName" show-overflow-tooltip/>
      <!-- <el-table-column label="社团简介" align="center" show-overflow-tooltip prop="description" /> -->
      <el-table-column label="类型" align="center" prop="name" />
      <el-table-column label="当前负责人" align="center" prop="sysUser.nickName" show-overflow-tooltip/>
      <el-table-column label="所属学院" align="center" prop="sysDept.deptName" show-overflow-tooltip />
      <el-table-column label="成立时间" align="center" prop="createdAt" :formatter="formatDate" />
      <el-table-column label="状态" align="center" prop="status">
        <template #default="{ row }">
          {{
            { pending: '待审核', active: '活跃中', inactive: '已停用' }[row.status] || '--'
          }}
        </template>
      </el-table-column>
      <el-table-column label="社团人数" align="center" prop="memberCount" />
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width" width="250">
        <template #default="scope">
          <el-button link type="primary" @click="getMemberList(scope.row)" v-hasPermi="['manage:club:userList']">查看成员</el-button>
          <el-button link type="primary" @click="handleDetail(scope.row)">详情</el-button>
          <el-button link type="primary" @click="handleUpdate(scope.row)" v-hasPermi="['manage:club:edit']">修改</el-button>
          <el-button link type="primary" @click="handleDelete(scope.row)" v-hasPermi="['manage:club:remove']">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <!-- 分页 -->
    <pagination v-show="total > 0" :total="total" v-model:page="queryParams.pageNum" v-model:limit="queryParams.pageSize"
      @pagination="getList" />

    <!-- 添加或修改社团管理对话框 -->
    <el-dialog :title="title" v-model="open" width="600px" append-to-body>
      <el-form ref="clubRef" :model="form" :rules="rules" label-width="100px" label-position="left">
        <el-form-item label="社团名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入社团名称" />
        </el-form-item>
        <el-form-item label="社团简介" prop="description">
          <el-input v-model="form.description" type="textarea" placeholder="请输入内容" />
        </el-form-item>
        <el-form-item label="分类" prop="categoryId">
          <el-select v-model="form.categoryId" placeholder="请选择分类" clearable>
            <el-option v-for="item in categoryList" :key="item.categoryId" :label="item.name" :value="item.categoryId" />
          </el-select>
        </el-form-item>
        <el-form-item label="负责人" prop="leaderId">
          <el-select v-model="form.leaderId" placeholder="请选择当前负责人" clearable>
            <el-option v-for="item in userList" :key="item.userId" :label="item.nickName"
              :value="item.userId"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="所属部门" prop="deptId">
          <el-select v-model="form.deptId" placeholder="请选择所属学院" clearable>
            <el-option v-for="item in deptList" :key="item.deptId" :label="item.deptName"
              :value="item.deptId"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="LOGO地址" prop="logoUrl">
          <image-upload v-model="form.logoUrl"/>
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button type="primary" @click="submitForm">确 定</el-button>
          <el-button @click="cancel">取 消</el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 查看社团成员 -->
    <el-dialog title="成员列表" v-model="memberDialogVisible" width="500px" append-to-body>
      <el-table v-loading="memberLoading" :data="memberList">
        <el-table-column label="名称" align="center" prop="userName" show-overflow-tooltip />
        <!-- <el-table-column label="姓名" align="center" prop="nickName" /> -->
        <el-table-column label="性别" align="center" prop="sex">
          <template #default="{ row }">
            {{ { 0: '男', 1: '女', 2: '未知' }[row.sex] }}
          </template>
        </el-table-column>
        <!-- 联系方式 -->
        <el-table-column label="联系方式" align="center" prop="phonenumber" />
        <!-- 加入社团时间 -->
        <el-table-column label="加入时间" align="center" prop="joinTime" :formatter="formatDate" width="100" />
        <!-- 退出社团时间 -->
        <!-- <el-table-column label="退出时间" align="center" prop="quitTime" :formatter="formatDate" /> -->
        <el-table-column label="状态" align="center" prop="status">
          <template #default="{ row }">
            {{
              { probation: '试用', active: '正式', graduated: '毕业', quit: '退出' }[row.status] || ''
            }}
          </template>
        </el-table-column>
      </el-table>
      <template #footer>
        <el-button @click="memberDialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>

    <!-- Detail Dialog -->
    <el-dialog v-model="detailDialog.visible" title="社团详情" width="40%">
      <el-descriptions :column="1" border>
        <el-descriptions-item label="社团名称">{{ detailDialog.currentDetail?.name || '--' }}</el-descriptions-item>
        <el-descriptions-item label="社团简介">{{ detailDialog.currentDetail?.description || '--' }}</el-descriptions-item>
        <el-descriptions-item label="类型">{{ detailDialog.currentDetail?.category?.name || '--' }}</el-descriptions-item>
        <el-descriptions-item label="当前负责人">{{ detailDialog.currentDetail?.sysUser?.nickName || '--' }}</el-descriptions-item>
        <el-descriptions-item label="所属学院">{{ detailDialog.currentDetail?.sysDept?.deptName || '--' }}</el-descriptions-item>
        <el-descriptions-item label="成立时间">{{ formatDateFull(detailDialog.currentDetail?.createdAt) || '--' }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          {{ { pending: '待审核', active: '活跃中', inactive: '已停用' }[detailDialog.currentDetail?.status] || '未知' }}
        </el-descriptions-item>
        <el-descriptions-item label="社团人数">{{ detailDialog.currentDetail?.memberCount || '--' }}</el-descriptions-item>
      </el-descriptions>
      <template #footer>
        <el-button @click="detailDialog.visible = false">关闭</el-button>
      </template>
    </el-dialog>

  </div>
</template>

<script setup name="Club">
import { listClub, getClub, delClub, addClub, updateClub, listMember } from "@/api/manage/club";
import { listCategory } from "@/api/manage/category";
import { listDept } from "@/api/system/dept";
import { listUser } from "@/api/system/user";

const { proxy } = getCurrentInstance();

const clubList = ref([]);
const open = ref(false);
const loading = ref(true);
const showSearch = ref(true);
const ids = ref([]);
const single = ref(true);
const multiple = ref(true);
const total = ref(0);
const title = ref("");
const daterangeCreatedAt = ref([]);
const memberDialogVisible = ref(false);
const memberLoading = ref(false);
const clubInfoOpen = ref(false);

const data = reactive({
  form: {},
  queryParams: {
    pageNum: 1,
    pageSize: 10,
    name: null,
    categoryId: null,
    leaderId: null,
    deptId: null,
    createdAt: null,
    status: null,
  },
  rules: {
    name: [
      { required: true, message: "社团名称不能为空", trigger: "blur" }
    ],
    description: [
      { required: true, message: "社团简介不能为空", trigger: "blur" }
    ],
    categoryId: [
      { required: true, message: "请选择分类", trigger: "change" }  // 建议trigger用change
    ],
    leaderId: [
      { required: true, message: "请选择负责人", trigger: "change" }
    ],
    deptId: [
      { required: true, message: "请选择所属学院", trigger: "change" }
    ]
  }
});

const { queryParams, form, rules } = toRefs(data);

/** 查询社团管理列表 */
function getList() {
  loading.value = true;
  queryParams.value.params = {};
  // 设置时间区间参数（如果有）
  if (null != daterangeCreatedAt && '' != daterangeCreatedAt) {
    queryParams.value.params["beginCreatedAt"] = daterangeCreatedAt.value[0];
    queryParams.value.params["endCreatedAt"] = daterangeCreatedAt.value[1];
  }
  // 调用api
  listClub(queryParams.value).then(response => {
    clubList.value = response.rows;
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
    clubId: null,
    name: null,
    description: null,
    categoryId: null,
    leaderId: null,
    deptId: null,
    createdAt: null,
    status: null,
    logoUrl: null,
    deletedAt: null
  };
  proxy.resetForm("clubRef");
}

/** 搜索按钮操作 */
function handleQuery() {
  queryParams.value.pageNum = 1;
  getList();
}

/** 重置按钮操作 */
function resetQuery() {
  daterangeCreatedAt.value = [];
  queryParams.value = {};
  proxy.resetForm("queryRef");
  handleQuery();
}

// 多选框选中数据
function handleSelectionChange(selection) {
  ids.value = selection.map(item => item.clubId);
  single.value = selection.length != 1;
  multiple.value = !selection.length;
}

/** 新增按钮操作 */
function handleAdd() {
  reset();
  open.value = true;
  title.value = "添加社团管理";
}

/** 修改按钮操作 */
function handleUpdate(row) {
  reset();
  const _clubId = row.clubId || ids.value
  getClub(_clubId).then(response => {
    form.value = response.data;
    open.value = true;
    title.value = "修改社团管理";
  });
}

/** 提交按钮 */
function submitForm() {
  proxy.$refs["clubRef"].validate(valid => {
    if (valid) {
      if (form.value.clubId != null) {
        updateClub(form.value).then(response => {
          proxy.$modal.msgSuccess("修改成功");
          open.value = false;
          getList();
        });
      } else {
        addClub(form.value).then(response => {
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
  const _clubIds = row.clubId || ids.value;
  proxy.$modal.confirm('是否确认删除社团管理编号为"' + _clubIds + '"的数据项？').then(function () {
    return delClub(_clubIds);
  }).then(() => {
    getList();
    proxy.$modal.msgSuccess("删除成功");
  }).catch(() => { });
}

/** 导出按钮操作 */
function handleExport() {
  proxy.download('manage/club/export', {
    ...queryParams.value
  }, `club_${new Date().getTime()}.xlsx`)
}

/* 查询所有的条件对象 */
const loadAllParams = reactive({
  pageNum: 1,
  pageSize: 10000
})

/** 查询社团分类列表 */
const categoryList = ref([]);
function getCategoryList() {
  listCategory(loadAllParams).then(response => {
    categoryList.value = response.rows;
  });
}
//** 查询部门列表 */
const deptList = ref([]);
function getDeptList() {
  listDept(loadAllParams).then(response => {
    deptList.value = response.data;
  });
}
//** 查询用户列表 */
const userList = ref([]);

function getListUser() {
  listUser(loadAllParams).then(response => {
    userList.value = response.rows;
  });
}

//** 查询社团成员列表 */
const memberList = ref([]);
function getMemberList(row) {
  memberDialogVisible.value = true
  const _id = row.clubId
  console.log(_id)
  listMember(_id).then(response => {
    memberList.value = response.data;
  });
}

getListUser();
getCategoryList();
getDeptList();
getList();

//** 格式化时间 */
const formatDate = (row, column, cellValue) => {
  if (!cellValue) return '';
  const date = new Date(cellValue);
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');

  return `${year}-${month}-${day}`;
};
// ** 社团详情 */
const clubDetail = ref({});

// 更完整的日期格式化
const formatDateFull = (cellValue) => {
  if (!cellValue) return '';
  const date = new Date(cellValue);
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  }).replace(/\//g, '-');
};

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

// 获取社团详情
function getClubInfo(row) {
  clubInfoOpen.value = true;
  getClub(row.clubId).then(response => {
    clubDetail.value = response.data;

    // 自动滚动到弹窗顶部
    nextTick(() => {
      const dialog = document.querySelector('.el-dialog__body');
      if (dialog) dialog.scrollTop = 0;
    });
  }).catch(() => {
    proxy.$modal.msgError("获取详情失败");
  });
}
</script>
