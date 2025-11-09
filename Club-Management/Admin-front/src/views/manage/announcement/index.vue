<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="公告标题" prop="title">
        <el-input
          v-model="queryParams.title"
          placeholder="请输入公告标题"
          clearable
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="社团" prop="title">
        <el-input
          v-model="queryParams.clubName"
          placeholder="请输入所属社团"
          clearable
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="学号" prop="publisherId">
        <el-input
          v-model="queryParams.userName"
          placeholder="请输入发布人学号"
          clearable
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="名字" prop="publisherId" width="200">
        <el-input
          v-model="queryParams.nickName"
          placeholder="请输入发布人名字"
          clearable
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="发布时间" style="width: 260px">
        <el-date-picker
          v-model="daterangeCreatedAt"
          value-format="YYYY-MM-DD"
          type="daterange"
          range-separator="-"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
        ></el-date-picker>
      </el-form-item>
      <el-form-item style="margin-left: 70px">
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
          v-hasPermi="['manage:announcement:add']"
        >新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          plain
          icon="Edit"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['manage:announcement:edit']"
        >修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="Delete"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['manage:announcement:remove']"
        >删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="Download"
          @click="handleExport"
          v-hasPermi="['manage:announcement:export']"
        >导出</el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="announcementList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="序号" type="index" align="center" prop="announcementId" width="55" />
      <el-table-column label="公告标题" align="center" prop="title" />
      <el-table-column label="公告内容" align="center" prop="content"  width="180" show-overflow-tooltip/>
      <el-table-column label="发布学号" align="center" prop="userName" />
      <el-table-column label="发布名字" align="center" prop="nickName" />
      <el-table-column label="发布社团" align="center" prop="clubName" />
      <el-table-column label="公告状态" align="center" prop="status" >
        <template #default="scope">
          <el-tag :type="statusTagType(scope.row.status)">
            {{ statusChineseMap[scope.row.status] || scope.row.status }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="发布时间" align="center" prop="createdAt" width="180">
        <template #default="scope">
          <span>{{ parseTime(scope.row.createdAt, '{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width" width="180">
        <template #default="scope">
          <el-button link type="primary" @click="handleDetails(scope.row)">详情</el-button>
          <el-button link type="primary" @click="handleUpdate(scope.row)" v-hasPermi="['manage:announcement:edit']">修改</el-button>
          <el-button link type="primary" @click="handleDelete(scope.row)" v-hasPermi="['manage:announcement:remove']">删除</el-button>
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

    <!-- 添加或修改公告管理对话框 -->
    <el-dialog :title="title" v-model="open" width="500px" append-to-body>
      <el-form ref="announcementRef" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="公告标题" prop="title">
          <el-input v-model="form.title" placeholder="请输入公告标题" />
        </el-form-item>
        <el-form-item label="公告内容">
          <editor v-model="form.content" :min-height="192"/>
        </el-form-item>
        <el-form-item label="发布人ID" prop="publisherId">
          <el-input v-model="form.publisherId" placeholder="请输入发布人ID" />
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
    <el-dialog title="公告详情" v-model="detailOpen" width="600px" append-to-body>
      <el-descriptions :column="1" border>
        <el-descriptions-item label="公告ID">{{ detailData.announcementId }}</el-descriptions-item>
        <el-descriptions-item label="公告标题">{{ detailData.title }}</el-descriptions-item>
        <el-descriptions-item label="公告内容">{{ detailData.content }}</el-descriptions-item>
        <el-descriptions-item label="发布人">{{ detailData.userName }}</el-descriptions-item>
        <el-descriptions-item label="发布社团">{{ detailData.clubName }}</el-descriptions-item>
        <el-descriptions-item label="公告状态">
          <el-tag :type="statusTagType(detailData.status)">
            {{ statusChineseMap[detailData.status] || detailData.status }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="发布时间">{{ parseTime(detailData.createdAt, '{y}-{m}-{d}') }}</el-descriptions-item>
      </el-descriptions>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="detailOpen = false">关 闭</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup name="Announcement">
import { listAnnouncement, getAnnouncement, delAnnouncement, addAnnouncement, updateAnnouncement } from "@/api/manage/announcement";

const { proxy } = getCurrentInstance();

const announcementList = ref([]);
const open = ref(false);
const loading = ref(true);
const showSearch = ref(true);
const ids = ref([]);
const single = ref(true);
const multiple = ref(true);
const total = ref(0);
const title = ref("");
const daterangeCreatedAt = ref([]);
const detailOpen = ref(false);
const detailData = ref({});

const data = reactive({
  form: {},
  queryParams: {
    pageNum: 1,
    pageSize: 10,
    title: null,
    content: null,
    publisherId: null,
    status: null,
    createdAt: null,
    nickName: null,
    userName: null,
    clubName: null
  },
  rules: {
    title: [
      { required: true, message: "公告标题不能为空", trigger: "blur" }
    ],
    content: [
      { required: true, message: "公告内容不能为空", trigger: "blur" }
    ],
    publisherId: [
      { required: true, message: "发布人ID不能为空", trigger: "blur" }
    ],
  }
});

const { queryParams, form, rules } = toRefs(data);

/** 查询公告管理列表 */
function getList() {
  loading.value = true;
  queryParams.value.params = {};
  if (null != daterangeCreatedAt && '' != daterangeCreatedAt) {
    queryParams.value.params["beginCreatedAt"] = daterangeCreatedAt.value[0];
    queryParams.value.params["endCreatedAt"] = daterangeCreatedAt.value[1];
  }
  listAnnouncement(queryParams.value).then(response => {
    announcementList.value = response.rows;
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
    announcementId: null,
    title: null,
    content: null,
    publisherId: null,
    type: null,
    status: null,
    createdAt: null,
    deletedAt: null
  };
  proxy.resetForm("announcementRef");
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
  queryParams.value = {};
  handleQuery();
}

// 多选框选中数据
function handleSelectionChange(selection) {
  ids.value = selection.map(item => item.announcementId);
  single.value = selection.length != 1;
  multiple.value = !selection.length;
}

/** 新增按钮操作 */
function handleAdd() {
  reset();
  open.value = true;
  title.value = "添加公告管理";
}

/** 修改按钮操作 */
function handleUpdate(row) {
  reset();
  const _announcementId = row.announcementId || ids.value
  getAnnouncement(_announcementId).then(response => {
    form.value = response.data;
    open.value = true;
    title.value = "修改公告管理";
  });
}

/** 提交按钮 */
function submitForm() {
  proxy.$refs["announcementRef"].validate(valid => {
    if (valid) {
      if (form.value.announcementId != null) {
        updateAnnouncement(form.value).then(response => {
          proxy.$modal.msgSuccess("修改成功");
          open.value = false;
          getList();
        });
      } else {
        addAnnouncement(form.value).then(response => {
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
  const _announcementIds = row.announcementId || ids.value;
  proxy.$modal.confirm('是否确认删除公告管理编号为"' + _announcementIds + '"的数据项？').then(function() {
    return delAnnouncement(_announcementIds);
  }).then(() => {
    getList();
    proxy.$modal.msgSuccess("删除成功");
  }).catch(() => {});
}

/** 导出按钮操作 */
function handleExport() {
  proxy.download('manage/announcement/export', {
    ...queryParams.value
  }, `announcement_${new Date().getTime()}.xlsx`)
}

/** 详情按钮操作 */
function handleDetails(row) {
  detailData.value = row;
  detailOpen.value = true;
}

getList();

const statusChineseMap = {
  pending: '待审批',
  published: '已发布',
  rejected: '已驳回'
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
