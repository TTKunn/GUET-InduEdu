<template>
    <div class="app-container">
      <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch" label-width="68px">
        <el-form-item label="社员学号" prop="userId">
          <el-input v-model="queryParams.userName" placeholder="请输入学号" clearable @keyup.enter="handleQuery" />
        </el-form-item>
        <el-form-item label="社员名字" prop="userId">
          <el-input v-model="queryParams.nickName" placeholder="请输入名字" clearable @keyup.enter="handleQuery" />
        </el-form-item>
        <el-form-item label="周期状态" prop="status">
          <el-select v-model="queryParams.status" placeholder="请选择状态" clearable style="width: 200px">
            <el-option-group label="在籍状态">
              <el-option label="试用期" value="probation" />
              <el-option label="在社中" value="active" />
              <el-option label="申请中" value="apply" />
            </el-option-group>
            <el-option-group label="离籍状态">
              <el-option label="已毕业" value="graduated" />
              <el-option label="已退出" value="quit" />
              <el-option label="未通过考核" value="failed" />
            </el-option-group>
          </el-select>
        </el-form-item>
  
        <el-form-item label="加入时间" style="width: 260px">
          <el-date-picker v-model="daterangeJoinTime" value-format="YYYY-MM-DD" type="daterange" range-separator="-"
            start-placeholder="开始日期" end-placeholder="结束日期" :shortcuts="dateShortcuts"></el-date-picker>
        </el-form-item>
        <el-form-item label="退出时间" style="width: 260px">
          <el-date-picker v-model="daterangeExitTime" value-format="YYYY-MM-DD" type="daterange" range-separator="-"
            start-placeholder="开始日期" end-placeholder="结束日期" :shortcuts="dateShortcuts"></el-date-picker>
        </el-form-item>
        <el-form-item label="学习时长" prop="totalStudyDuration">
          <el-select v-model="queryParams.totalStudyDuration" placeholder="请选择学习时长范围" clearable style="width: 200px">
            <el-option label="30分钟以下" value="0-30" />
            <el-option label="30-120分钟" value="30-120" />
            <el-option label="2-4小时" value="120-240" />
            <el-option label="4小时以上" value="240-9999" />
          </el-select>
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
            v-hasPermi="['personal:membership:add']"
          >新增</el-button>
        </el-col> -->
        <el-col :span="1.5">
          <el-button type="success" plain icon="Edit" :disabled="single" @click="handleUpdate"
            v-hasPermi="['personal:membership:edit']">更改状态</el-button>
        </el-col>
        <!-- <el-col :span="1.5">
          <el-button type="danger" plain icon="Delete" :disabled="multiple" @click="handleDelete"
            v-hasPermi="['personal:membership:remove']">删除</el-button>
        </el-col> -->
        <el-col :span="1.5">
          <el-button type="warning" plain icon="Download" @click="handleExport"
            v-hasPermi="['personal:membership:export']">导出</el-button>
        </el-col>
        <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
      </el-row>
  
      <el-table v-loading="loading" :data="membershipList" @selection-change="handleSelectionChange">
    <!-- 序号列保持原样 -->
    <el-table-column type="selection" width="55" align="center" />
    <el-table-column label="序号" type="index" align="center" width="60" />
    
    <!-- 基本信息放在前面 -->
    <el-table-column label="社员名字" align="center" prop="nickName" width="120" />
    <el-table-column label="社员学号" align="center" prop="userName" width="150" />
    
    <!-- 状态信息 -->
    <el-table-column label="周期状态" align="center" width="120">
      <template #default="{ row }">
        <el-tag :type="getStatusTagType(row.status)" size="small">
          {{ formatStatus(row.status) }}
        </el-tag>
      </template>
    </el-table-column>
    
    <!-- 时间信息 -->
    <el-table-column label="加社时间" align="center" width="150">
      <template #default="scope">
        <span>{{ parseTime(scope.row.joinTime, '{y}-{m}-{d}') }}</span>
      </template>
    </el-table-column>
    <!-- activityParticipation -->
    <el-table-column label="活动参与次数" align="center" width="120">
      <template #default="scope">
        <span>{{ scope.row.activityParticipation || '--' }}</span>
      </template>
    </el-table-column>
    <!-- achievementCount -->
    <el-table-column label="活动完成次数" align="center" width="120">
      <template #default="scope">
        <span>{{ scope.row.achievementCount || '--' }}</span>
      </template>
    </el-table-column>
    <el-table-column label="退社状态 || 时间" align="center" width="155">
      <template #default="{ row }">
        <div v-if="row.status === 'probation' || row.status === 'active' || row.status === 'failed'" 
             class="in-membership">
          <el-icon><CircleCheck /></el-icon>
          <span>在籍</span>
        </div>
        <span v-else-if="row.exitTime">{{ parseTime(row.exitTime, '{y}-{m}-{d}') }}</span>
        <span v-else>--</span>
      </template>
    </el-table-column>
    
    <!-- 学习时长 -->
    <el-table-column label="学习时长" align="center" width="160">
      <template #default="{ row }">
        <el-tag :type="getDurationTagType(row.totalStudyDuration)" size="small">
          {{ formatMinutes(row.totalStudyDuration) }}
        </el-tag>
      </template>
    </el-table-column>
    
    <!-- 操作列 -->
    <el-table-column label="操作" align="center" width="230" fixed="right">
      <template #default="scope">
        <!-- 查看成果 -->
        <el-button link type="primary" size="small" @click="handleAchievements(scope.row.userId)">
          查看成果
        </el-button>
        <!-- 查看参与的活动 -->
        <el-button link type="primary" size="small" @click="handleActivities(scope.row.userId)">
          查看参与的活动
        </el-button>
        <el-button link type="primary" size="small" @click="handleDetail(scope.row)">详情</el-button>
        <el-button link type="primary" size="small" @click="handleUpdate(scope.row)"
                   v-hasPermi="['personal:membership:edit']">更改状态</el-button>
      </template>
    </el-table-column>
  </el-table>
  
      <pagination v-show="total > 0" :total="total" v-model:page="queryParams.pageNum" v-model:limit="queryParams.pageSize"
        @pagination="getList" />
  
      <!-- 添加或修改社团成员关系对话框 -->
      <el-dialog :title="title" v-model="open" width="500px" append-to-body>
        <el-form ref="membershipRef" :model="form" :rules="rules" label-width="80px">
          <el-form-item label="状态" prop="status">
            <el-select v-model="form.status" placeholder="请选择状态">
              <el-option v-for="item in statusOptions" :key="item.value" :label="item.label" :value="item.value" />
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
  
      <!-- 成员详情对话框 -->
  <el-dialog title="成员详情" v-model="detailVisible" width="700px" append-to-body>
    <el-descriptions :column="2" border>
      <el-descriptions-item label="社员学号">{{ detailInfo.userName }}</el-descriptions-item>
      <el-descriptions-item label="社员名字">{{ detailInfo.nickName }}</el-descriptions-item>
      <el-descriptions-item label="加社时间">{{ parseTime(detailInfo.joinTime, '{y}-{m}-{d}') }}</el-descriptions-item>
      <el-descriptions-item label="周期状态">
        <el-tag :type="getStatusTagType(detailInfo.status)">
          {{ formatStatus(detailInfo.status) }}
        </el-tag>
      </el-descriptions-item>
      <el-descriptions-item label="退社时间" v-if="detailInfo.exitTime">
        {{ parseTime(detailInfo.exitTime, '{y}-{m}-{d}') }}
      </el-descriptions-item>
      <el-descriptions-item label="累计学习时长">
        <el-tag :type="getDurationTagType(detailInfo.totalStudyDuration)">
          {{ formatMinutes(detailInfo.totalStudyDuration) }}
        </el-tag>
      </el-descriptions-item>
      <!-- 可以添加更多详情字段 -->
    </el-descriptions>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="detailVisible = false">关 闭</el-button>
      </div>
    </template>
  </el-dialog>
  <el-dialog title="成果" v-model="achievementDialogVisible" width="500px">
    <el-table :data="achievementData">
      <el-table-column label="成果ID" prop="achievementId"></el-table-column>
      <el-table-column label="标题" prop="title"></el-table-column>
      <el-table-column label="类型" prop="type"></el-table-column>
      <el-table-column label="描述" prop="description"></el-table-column>
      <el-table-column label="完成日期" prop="achieveDate"></el-table-column>
      <el-table-column label="证书地址" align="center" prop="certificateUrl" width="100">
        <template #default="scope">
          <image-preview :src="scope.row.certificateUrl" :width="50" :height="50" />
        </template>
      </el-table-column>
      <el-table-column label="状态" prop="status"></el-table-column>
      <el-table-column label="角色" prop="role"></el-table-column>
      <el-table-column label="贡献" prop="contribution"></el-table-column>
    </el-table>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="achievementDialogVisible = false">关 闭</el-button>
      </div>
    </template>
  </el-dialog>
  <el-dialog title="参与活动" v-model="activityDialogVisible" width="500px">
    <pre>{{ activityData }}</pre>
    <template #footer>
      <div class="dialog-footer">
        <el-form-item label="活动ID" prop="activityId">
          <el-input v-model="activityData.activityId" placeholder="请输入活动ID" clearable></el-input>
        </el-form-item>
        <el-form-item label="活动名称" prop="activityName">
          <el-input v-model="activityData.activityName" placeholder="请输入活动名称" clearable></el-input>
        </el-form-item>
        <el-button type="primary" @click="handleActivitySearch">搜索</el-button>
        <el-button icon="Refresh" @click="handleActivityReset">重置</el-button>
        <el-table :data="activityData">
          <el-table-column label="活动ID" prop="activityId"></el-table-column>
          <el-table-column label="活动名称" prop="activityName"></el-table-column>
          <el-table-column label="活动类型" prop="activityType"></el-table-column>
          <el-table-column label="活动时间" prop="activityTime"></el-table-column>
          <el-table-column label="活动地点" prop="activityLocation"></el-table-column>
          <el-table-column label="参与人数" prop="participantCount"></el-table-column>
        </el-table>
        <el-button @click="activityDialogVisible = false">关 闭</el-button>
      </div>
    </template>
  </el-dialog>
    </div>
  </template>
  
  <script setup name="Membership">
  import { listMembership, getMembership, delMembership, addMembership, updateMembership , listAchievementsByMemberId, listActivitiesByMemberId} from "@/api/personal/membership";
  import { getInfo } from '@/api/login'
  import { selectClubIdByUserId } from '@/api/personal/club'
  const { proxy } = getCurrentInstance();
  
  const membershipList = ref([]);
  const open = ref(false);
  const loading = ref(true);
  const showSearch = ref(true);
  const ids = ref([]);
  const single = ref(true);
  const multiple = ref(true);
  const total = ref(0);
  const title = ref("");
  const daterangeJoinTime = ref([]);
  const daterangeExitTime = ref([]);
  
  const data = reactive({
    form: {},
    queryParams: {
      pageNum: 1,
      pageSize: 10,
      userId: null,
      clubId: null,
      joinTime: null,
      status: null,
      exitTime: null,
      totalStudyDuration: null
    },
    rules: {
      userId: [
        { required: true, message: "用户ID不能为空", trigger: "blur" }
      ],
      clubId: [
        { required: true, message: "社团ID不能为空", trigger: "blur" }
      ],
      joinTime: [
        { required: true, message: "加入时间不能为空", trigger: "blur" }
      ],
      status: [
        { required: true, message: "状态不能为空", trigger: "change" }
      ],
    }
  });
  
  const { queryParams, form, rules } = toRefs(data);
  
  /** 查询社团成员关系列表 */
  async function getList() {
    loading.value = true;
    queryParams.value.params = {};
  
    // 处理日期范围
    if (daterangeJoinTime.value && daterangeJoinTime.value.length === 2) {
      queryParams.value.params["beginJoinTime"] = daterangeJoinTime.value[0];
      queryParams.value.params["endJoinTime"] = daterangeJoinTime.value[1];
    }
  
    if (daterangeExitTime.value && daterangeExitTime.value.length === 2) {
      queryParams.value.params["beginExitTime"] = daterangeExitTime.value[0];
      queryParams.value.params["endExitTime"] = daterangeExitTime.value[1];
    }
  
    // 处理学习时长范围
    if (queryParams.value.totalStudyDuration) {
      const [min, max] = queryParams.value.totalStudyDuration.split('-');
      queryParams.value.params["minStudyDuration"] = min;
      queryParams.value.params["maxStudyDuration"] = max;
    }
  
    try {
      const userId = await getCurrentUserId();
      const clubId = await selectClubIdByUserId(userId);
      queryParams.value.clubId = clubId;
  
      const response = await listMembership(queryParams.value);
      membershipList.value = response.rows;
      total.value = response.total;
      loading.value = false;
    } catch (error) {
      console.error('Failed to fetch membership list:', error);
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
      membershipId: null,
      userId: null,
      clubId: null,
      joinTime: null,
      status: null,
      exitTime: null,
      deletedAt: null,
      totalStudyDuration: null
    };
    proxy.resetForm("membershipRef");
  }
  
  /** 搜索按钮操作 */
  function handleQuery() {
    queryParams.value.pageNum = 1;
    getList();
  }
  
  /** 重置按钮操作 */
  function resetQuery() {
    daterangeJoinTime.value = [];
    daterangeExitTime.value = [];
    proxy.resetForm("queryRef");
    queryParams.value = {};
    handleQuery();
  }
  
  // 多选框选中数据
  function handleSelectionChange(selection) {
    ids.value = selection.map(item => item.membershipId);
    single.value = selection.length != 1;
    multiple.value = !selection.length;
  }
  
  /** 新增按钮操作 */
  function handleAdd() {
    reset();
    open.value = true;
    title.value = "添加社团成员关系";
  }
  
  /** 修改按钮操作 */
  function handleUpdate(row) {
    reset();
    const _membershipId = row.membershipId || ids.value
    console.log(_membershipId)
    getMembership(_membershipId).then(response => {
      form.value = response.data;
      open.value = true;
      title.value = "修改社团成员生命周期";
    });
  }
  
  /** 提交按钮 */
  function submitForm() {
    proxy.$refs["membershipRef"].validate(valid => {
      if (valid) {
        if (form.value.membershipId != null) {
          updateMembership(form.value).then(response => {
            proxy.$modal.msgSuccess("修改成功");
            open.value = false;
            getList();
          });
        } else {
          addMembership(form.value).then(response => {
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
    const _membershipIds = row.membershipId || ids.value;
    proxy.$modal.confirm('是否确认删除社团成员关系编号为"' + _membershipIds + '"的数据项？').then(function () {
      return delMembership(_membershipIds);
    }).then(() => {
      getList();
      proxy.$modal.msgSuccess("删除成功");
    }).catch(() => { });
  }
  
  /** 导出按钮操作 */
  function handleExport() {
    proxy.download('personal/membership/export', {
      ...queryParams.value
    }, `membership_${new Date().getTime()}.xlsx`)
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
  
  const statusOptions = ref([
    { value: 'probation', label: '试用期' },
    { value: 'active', label: '在社中' },
    { value: 'graduated', label: '已毕业' },
    { value: 'quit', label: '已退出' },
    { value: 'apply', label: '申请中' },
    { value: 'failed', label: '未通过考核' }  // 新增状态
  ])
  
  // 状态文本转换
  const formatStatus = (status) => {
    const statusMap = {
      probation: '试用期',
      active: '在社中',
      graduated: '已毕业',
      quit: '已退出',
      apply: '申请中',
      failed: '未通过考核'  // 新增状态文本
    }
    return statusMap[status] || status
  }
  // 状态标签类型（不同状态显示不同颜色）
  const getStatusTagType = (status) => {
    const typeMap = {
      probation: 'warning',  // 黄色
      active: 'success',    // 绿色
      graduated: 'info',   // 蓝色
      quit: 'danger',      // 红色
      failed: 'danger'     // 红色（与已退出相同）
    }
    return typeMap[status] || ''
  }
  const achievementDialogVisible = ref(false);
  const activityDialogVisible = ref(false);
  const achievementData = ref([]);
  const activityData = ref([]);
  
  const formatMinutes = (minutes) => {
    if (minutes === null || minutes === undefined) return '无记录';
  
    // 超过4小时显示"X小时"（省略分钟）
    if (minutes >= 240) {
      return `${Math.round(minutes / 60)}小时`;
    }
  
    // 1-4小时显示"X小时Y分钟"
    if (minutes >= 60) {
      const hours = Math.floor(minutes / 60);
      const mins = minutes % 60;
      return `${hours}小时${mins > 0 ? `${mins}分钟` : ''}`;
    }
  
    // 不足1小时显示"X分钟"
    return `${minutes}分钟`;
  }
  
  const getDurationTagType = (minutes) => {
    if (!minutes) return 'info';
    if (minutes < 30) return 'danger';    // 红色-学习不足
    if (minutes < 120) return 'warning'; // 黄色-一般
    return 'success';                     // 绿色-良好
  }
  
  const dateShortcuts = [
    {
      text: '最近一周',
      value: () => {
        const end = new Date()
        const start = new Date()
        start.setTime(start.getTime() - 3600 * 1000 * 24 * 7)
        return [start, end]
      }
    },
    {
      text: '最近一个月',
      value: () => {
        const end = new Date()
        const start = new Date()
        start.setTime(start.getTime() - 3600 * 1000 * 24 * 30)
        return [start, end]
      }
    },
    {
      text: '最近三个月',
      value: () => {
        const end = new Date()
        const start = new Date()
        start.setTime(start.getTime() - 3600 * 1000 * 24 * 90)
        return [start, end]
      }
    }
  ]
  
  // 添加响应式变量
  const detailVisible = ref(false);
  const detailInfo = ref({});
  
  // 添加详情处理方法
  function handleDetail(row) {
    detailInfo.value = {
      ...row
    };
    detailVisible.value = true;
  }

  // handleAchievements
  function handleAchievements(userId) {
    console.log(userId)
    listAchievementsByMemberId(userId).then(response => {
      // 假设接口返回格式为 { msg, code, data }
      achievementData.value = response.data || [];
      achievementDialogVisible.value = true;
    }).catch(error => {
      console.error('获取成果信息失败:', error);
      proxy.$modal.msgError('获取成果信息失败，请重试');
    });
  }

  // handleActivities
  function handleActivities(userId) {
    console.log(userId)
    listActivitiesByMemberId(userId).then(response => {
      // 假设接口返回格式为 { msg, code, data }
      activityData.value = response.data || [];
      activityDialogVisible.value = true;
    }).catch(error => {
      console.error('获取活动信息失败:', error);
      proxy.$modal.msgError('获取活动信息失败，请重试');
    });
  }

  // 时间格式化函数
  const parseTime = (time, cFormat) => {
    if (arguments.length === 0) {
      return null
    }
    const format = cFormat || '{y}-{m}-{d} {h}:{i}:{s}'
    let date
    if (typeof time === 'object') {
      date = time
    } else {
      if ((typeof time === 'string') && (/^[0-9]+$/.test(time))) {
        time = parseInt(time)
      }
      if ((typeof time === 'number') && (time.toString().length === 10)) {
        time = time * 1000
      }
      date = new Date(time)
    }
    const formatObj = {
      y: date.getFullYear(),
      m: date.getMonth() + 1,
      d: date.getDate(),
      h: date.getHours(),
      i: date.getMinutes(),
      s: date.getSeconds(),
      a: date.getDay()
    }
    const time_str = format.replace(/{([ymdhisa])+}/g, (result, key) => {
      const value = formatObj[key]
      // Note: getDay() returns 0 on Sunday
      if (key === 'a') { return ['日', '一', '二', '三', '四', '五', '六'][value ] }
      return value.toString().padStart(2, '0')
    })
    return time_str
  }
</script>
  
  
  <style scoped>
  .in-membership {
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--el-color-success);
  }
  
  .in-membership span {
    margin-left: 5px;
  }
  
  /* 在style部分添加 */
  .detail-dialog {
    .el-descriptions {
      margin-top: 20px;
    }
    .el-descriptions-item__label {
      width: 100px;
      text-align: right;
    }
  }
  </style>
  
  