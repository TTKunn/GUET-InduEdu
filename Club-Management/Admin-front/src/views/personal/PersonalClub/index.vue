<template>
  <div class="app-container">
    <el-card class="club-card" shadow="hover">
      <div class="club-header">
        <el-avatar :size="100" :src="clubInfo.logoUrl" class="club-logo">
          <img src="@/assets/images/club-default.png" />
        </el-avatar>
        <div class="club-title">
          <h2>{{ clubInfo.name }}</h2>
          <div class="club-status">
            <el-tag :type="getStatusTagType(clubInfo.status)" :effect="getStatusTagEffect(clubInfo.status)">
              {{ getStatusText(clubInfo.status) }}
            </el-tag>
          </div>
        </div>
      </div>

      <div class="club-content">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="社团简介">{{ clubInfo.description || '暂无简介' }}</el-descriptions-item>
          <el-descriptions-item label="分类">{{ clubInfo.categoryName }}</el-descriptions-item>
          <el-descriptions-item label="负责人">
            {{ clubInfo.userName }} ({{ clubInfo.nickName }})
          </el-descriptions-item>
          <el-descriptions-item label="所属学院">{{ clubInfo.deptName }}</el-descriptions-item>
          <el-descriptions-item label="成立时间">
            {{ parseTime(clubInfo.createdAt, '{y}年{m}月{d}日') }}
          </el-descriptions-item>
          <el-descriptions-item label="指导老师" v-if="clubInfo.advisorNames">
            <el-tag v-for="(name, index) in clubInfo.advisorNames.split(', ')" :key="index" type="info"
              style="margin-right: 8px; margin-bottom: 8px ; margin-top: 8px">
              {{ name }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="指导老师" v-else>暂无指导老师</el-descriptions-item>
          <!-- <el-descriptions-item label="社团成员数">
  {{ clubInfo.memberCount || 0 }}
</el-descriptions-item>
<el-descriptions-item label="社团成果数">
  {{ clubInfo.achievementCount || 0 }}
</el-descriptions-item> -->
        </el-descriptions>
      </div>

      <div class="club-footer">
        <el-button type="primary" @click="handleUpdate" icon="Edit" v-hasPermi="['personal:PersonalClub:edit']">
          修改社团信息
        </el-button>
      </div>
    </el-card>

    <!-- 修改社团信息对话框 -->
    <el-dialog :title="title" v-model="open" width="600px" append-to-body>
      <el-form ref="PersonalClubRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="社团名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入社团名称" />
        </el-form-item>
        <el-form-item label="社团简介" prop="description">
          <el-input v-model="form.description" type="textarea" rows="4" placeholder="请输入社团简介" />
        </el-form-item>
        <el-form-item label="LOGO地址" prop="logoUrl">
          <el-input v-model="form.logoUrl" placeholder="请输入LOGO图片地址" />
          <div class="el-upload__tip">建议上传正方形图片，尺寸不小于200×200像素</div>
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button type="primary" @click="submitForm">确 定</el-button>
          <el-button @click="cancel">取 消</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup name="PersonalClub">
import { listPersonalClub, getPersonalClub, updatePersonalClub } from "@/api/personal/PersonalClub";
import { getInfo } from '@/api/login'
import { selectClubIdByUserId } from '@/api/personal/club'
const { proxy } = getCurrentInstance();

const clubInfo = ref({
  clubId: null,
  name: '',
  description: '',
  categoryName: '',
  userName: '',
  nickName: '',
  deptName: '',
  createdAt: '',
  status: '0',
  logoUrl: '',
  advisorNames: '',
  advisorIds: ''
});

const open = ref(false);
const loading = ref(true);
const title = ref("");

const data = reactive({
  form: {},
  queryParams: {
    clubId: null
  },
  rules: {
    name: [
      { required: true, message: "社团名称不能为空", trigger: "blur" }
    ],
    description: [
      { required: true, message: "社团简介不能为空", trigger: "blur" }
    ],
    logoUrl: [
      { required: false, message: "LOGO地址不能为空", trigger: "blur" }
    ]
  }
});

const { queryParams, form, rules } = toRefs(data);

/** 查询社团信息 */
async function getClubInfo() {
  loading.value = true;

  try {
    // 获取当前用户ID
    const userId = await getCurrentUserId();
    // 根据用户ID获取社团ID
    const clubId = await selectClubIdByUserId(userId);

    if (!clubId) {
      proxy.$modal.msgError("您尚未创建或管理任何社团");
      loading.value = false;
      return;
    }

    // 获取社团详细信息
    const response = await getPersonalClub(clubId);
    clubInfo.value = response.data;
    loading.value = false;
  } catch (error) {
    console.error('Failed to fetch club info:', error);
    proxy.$modal.msgError("加载失败，请重试");
    loading.value = false;
  }
}

// 取消按钮
function cancel() {
  open.value = false;
}

// 表单重置
function reset() {
  form.value = {
    clubId: clubInfo.value.clubId,
    name: clubInfo.value.name,
    description: clubInfo.value.description,
    logoUrl: clubInfo.value.logoUrl,
    status: clubInfo.value.status
  };
  proxy.resetForm("PersonalClubRef");
}

/** 修改按钮操作 */
function handleUpdate() {
  reset();
  open.value = true;
  title.value = "修改社团信息";
}

/** 提交按钮 */
function submitForm() {
  proxy.$refs["PersonalClubRef"].validate(valid => {
    if (valid) {
      updatePersonalClub(form.value).then(response => {
        proxy.$modal.msgSuccess("修改成功");
        open.value = false;
        getClubInfo(); // 重新加载社团信息
      }).catch(error => {
        proxy.$modal.msgError("修改失败");
      });
    }
  });
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

// 状态文本映射
const statusTextMap = {
  pending: '审核中',
  active: '活跃',
  inactive: '已停用'
}

// 状态标签类型映射
const statusTagTypeMap = {
  pending: 'warning',
  active: 'success',
  inactive: 'danger'
}

// 状态标签效果映射
const statusTagEffectMap = {
  pending: 'light',
  active: 'dark',
  inactive: 'plain'
}

// 获取状态显示文本
const getStatusText = (status) => {
  return statusTextMap[status] || status
}

// 获取标签类型
const getStatusTagType = (status) => {
  return statusTagTypeMap[status] || 'info'
}

// 获取标签效果
const getStatusTagEffect = (status) => {
  return statusTagEffectMap[status] || 'light'
}

// 查看指导老师详情
function viewAdvisorProfile(advisorId) {
  // 这里可以添加跳转到指导老师详情的逻辑
  console.log('查看指导老师ID:', advisorId);
  // proxy.$router.push(`/system/advisor/profile/${advisorId}`);
}

getClubInfo();
</script>

<style scoped>
.club-card {
  max-width: 800px;
  margin: 20px auto;
}

.club-header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.club-logo {
  margin-right: 20px;
  border: 1px solid #eee;
}

.club-title {
  flex: 1;
}

.club-title h2 {
  margin: 0;
  font-size: 24px;
  color: #333;
}

.club-status {
  margin-top: 10px;
}

.club-content {
  margin: 20px 0;
}

.club-footer {
  text-align: center;
  margin-top: 20px;
}

.el-descriptions {
  margin-top: 20px;
}

.el-descriptions-item__label {
  width: 100px;
}
</style>