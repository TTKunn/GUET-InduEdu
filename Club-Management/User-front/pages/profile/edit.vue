<template>
  <view class="container">
    <!-- 表单容器 -->
    <view class="form-container">
      <!-- 头像上传 -->
      <view class="avatar-upload">
        <text class="upload-label">头像</text>
        <view class="avatar-wrapper" @click="chooseImage">
          <image 
            :src="userInfo.avatar ? getFullImageUrl(userInfo.avatar) : '/static/avatar.png'" 
            class="avatar" 
            mode="aspectFill"
          />
          <view class="upload-hint">
            <i class="fa fa-camera"></i>
            <text>点击更换</text>
          </view>
        </view>
      </view>
      
      <!-- 表单内容 -->
      <view class="form-content">
        <view class="form-item">
          <text class="item-label">昵称</text>
          <input 
            type="text" 
            class="item-input" 
            :value="formData.nickName || ''" 
            @input="updateField('nickName', $event.detail.value)"
            placeholder="请输入昵称"
          />
        </view>
        
        <view class="form-item">
          <text class="item-label">邮箱</text>
          <input 
            type="email" 
            class="item-input" 
            :value="formData.email || ''" 
            @input="updateField('email', $event.detail.value)"
            placeholder="请输入邮箱"
          />
        </view>
        
        <view class="form-item">
          <text class="item-label">手机号</text>
          <input 
            type="number" 
            class="item-input" 
            :value="formData.phonenumber || ''" 
            @input="updateField('phonenumber', $event.detail.value)"
            placeholder="请输入手机号"
          />
        </view>
        
        <view class="form-item">
          <text class="item-label">性别</text>
          <view class="gender-selector">
            <view 
              class="gender-option" 
              :class="{'active': formData.sex === '0'}" 
              @click="updateField('sex', '0')"
            >
              <text>男</text>
            </view>
            <view 
              class="gender-option" 
              :class="{'active': formData.sex === '1'}" 
              @click="updateField('sex', '1')"
            >
              <text>女</text>
            </view>
            <view 
              class="gender-option" 
              :class="{'active': formData.sex === '2'}" 
              @click="updateField('sex', '2')"
            >
              <text>保密</text>
            </view>
          </view>
        </view>
        
        <!-- 修改为下拉选择 -->
        <view class="form-item relative">
          <text class="item-label">部门</text>
          <view class="dept-selector" @click="showDeptList = true">
            <text class="selector-value">{{ selectedDeptName || '请选择部门' }}</text>
            <i class="fa fa-chevron-down selector-icon"></i>
          </view>
          
          <!-- 部门下拉列表 -->
          <view class="dept-list absolute" v-show="showDeptList">
            <view 
              class="dept-item" 
              v-for="dept in deptList" 
              :key="dept.deptId" 
              @click="selectDept(dept)"
            >
              <text>{{ dept.deptName }}</text>
            </view>
          </view>
        </view>
      </view>
      
      <!-- 提交按钮 -->
      <view class="submit-container">
        <button class="submit-btn" @click="submitForm">
          <text>保存修改</text>
        </button>
      </view>
    </view>
  </view>
</template>

<script>
import { mapState } from 'vuex'

export default {
  data() {
    return {
      baseUrl: "http://localhost:8080",
      tempAvatarPath: '', // 临时头像路径
      formData: {}, // 表单数据
      deptList: [], // 部门列表
      showDeptList: false, // 控制部门下拉列表显示
      selectedDeptId: '', // 选中的部门ID
      selectedDeptName: '' // 选中的部门名称
    }
  },
  computed: {
    ...mapState(['userInfo'])
  },
  onLoad() {
    // 初始化表单数据为当前用户信息的副本
    this.formData = JSON.parse(JSON.stringify(this.userInfo));
    // 初始化部门信息
    this.selectedDeptId = this.userInfo.deptId || '';
    this.selectedDeptName = this.userInfo.deptName || '';
    // 加载部门列表
    this.loadDeptList();
  },
  methods: {
    // 获取完整图片URL
    getFullImageUrl(relativeUrl) {
      if (!relativeUrl) {
        return '/static/avatar.png';
      }
      return `${this.baseUrl}${relativeUrl}`;
    },
    
    // 更新表单字段
    updateField(field, value) {
      this.formData[field] = value;
    },
    
    // 加载部门列表
    loadDeptList() {
      uni.request({
        url: `${this.baseUrl}/happy/dept/list`,
        method: 'GET',
        success: (res) => {
          if (res.data.code === 200) {
            this.deptList = res.data.data || [];
          } else {
            uni.showToast({
              title: '获取部门列表失败',
              icon: 'none'
            });
          }
        },
        fail: () => {
          uni.showToast({
            title: '网络错误，获取部门列表失败',
            icon: 'none'
          });
        }
      });
    },
    
    // 选择部门
    selectDept(dept) {
      this.selectedDeptId = dept.deptId;
      this.selectedDeptName = dept.deptName;
      this.formData.deptId = dept.deptId; // 更新表单数据中的部门ID
      this.formData.deptName = dept.deptName; // 更新表单数据中的部门名称
      this.showDeptList = false;
    },
    
    // 选择图片
    chooseImage() {
      uni.chooseImage({
        count: 1,
        sizeType: ['original', 'compressed'],
        sourceType: ['album', 'camera'],
        success: (res) => {
          this.tempAvatarPath = res.tempFilePaths[0];
          // 显示加载提示
          uni.showLoading({
            title: '上传中...'
          });
          
          // 上传图片
          this.uploadAvatar();
        }
      });
    },
    
    // 上传头像
    uploadAvatar() {
      if (!this.tempAvatarPath) return;
      
      uni.uploadFile({
        url: `${this.baseUrl}/common/upload`,
        filePath: this.tempAvatarPath,
        name: 'file',
        success: (res) => {
          const result = JSON.parse(res.data);
          if (result.code === 200) {
            this.formData.avatar = result.data.url;
            uni.showToast({
              title: '头像上传成功',
              icon: 'success'
            });
          } else {
            uni.showToast({
              title: '头像上传失败',
              icon: 'none'
            });
          }
        },
        fail: () => {
          uni.showToast({
            title: '网络错误，上传失败',
            icon: 'none'
          });
        },
        complete: () => {
          uni.hideLoading();
        }
      });
    },
    
    // 提交表单
    submitForm() {
      // 简单验证
      if (!this.formData.nickName) {
        uni.showToast({
          title: '请输入昵称',
          icon: 'none'
        });
        return;
      }
      
      if (!this.selectedDeptId) {
        uni.showToast({
          title: '请选择部门',
          icon: 'none'
        });
        return;
      }
      
      // 显示加载提示
      uni.showLoading({
        title: '保存中...'
      });
      
      // 提交表单数据
      uni.request({
        url: `${this.baseUrl}/happy/user/update`,
        method: 'POST',
        data: this.formData,
        success: (res) => {
          if (res.data.code === 200) {
            // 更新Vuex中的用户信息
            this.$store.commit('setUserInfo', this.formData);
            
            uni.showToast({
              title: '修改成功',
              icon: 'success'
            });
            
            // 返回上一页
            setTimeout(() => {
              uni.navigateBack();
            }, 1500);
          } else {
            uni.showToast({
              title: res.data.msg || '修改失败',
              icon: 'none'
            });
          }
        },
        fail: () => {
          uni.showToast({
            title: '网络错误，修改失败',
            icon: 'none'
          });
        },
        complete: () => {
          uni.hideLoading();
        }
      });
    }
  }
}
</script>

<style lang="scss" scoped>
$primary-color: #7d79f4;
$secondary-color: #9d99ff;
$text-primary: #333;
$text-secondary: #666;
$text-tertiary: #999;
$border-color: #f0f0f0;
$bg-color: #f5f5f5;

.container {
  background-color: $bg-color;
  min-height: 100vh;
}

.form-container {
	height: 95vh;
  background-color: white;
  margin: 20rpx;
  border-radius: 20rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

.avatar-upload {
  padding: 40rpx 30rpx;
  border-bottom: 2rpx solid $border-color;
  
  .upload-label {
    font-size: 28rpx;
    color: $text-secondary;
    margin-bottom: 20rpx;
    display: block;
  }
  
  .avatar-wrapper {
    position: relative;
    width: 160rpx;
    height: 160rpx;
    margin: 0 auto;
    
    .avatar {
      width: 100%;
      height: 100%;
      border-radius: 50%;
      border: 2rpx solid $border-color;
    }
    
    .upload-hint {
      position: absolute;
      bottom: 0;
      right: 0;
      width: 50rpx;
      height: 50rpx;
      background-color: rgba(0, 0, 0, 0.6);
      border-radius: 50%;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      
      i {
        color: white;
        font-size: 24rpx;
      }
      
      text {
        color: white;
        font-size: 18rpx;
      }
    }
  }
}

.form-content {
  padding: 0 30rpx;
}

.form-item {
  display: flex;
  align-items: center;
  padding: 30rpx 0;
  border-bottom: 2rpx solid $border-color;
  
  &:last-child {
    border-bottom: none;
  }
  
  .item-label {
    font-size: 28rpx;
    color: $text-secondary;
    width: 200rpx;
  }
  
  .item-input {
    flex: 1;
    font-size: 28rpx;
    color: $text-primary;
    text-align: right;
  }
}

.gender-selector {
  flex: 1;
  display: flex;
  justify-content: flex-end;
  
  .gender-option {
    padding: 12rpx 30rpx;
    border-radius: 30rpx;
    margin-left: 20rpx;
    font-size: 28rpx;
    color: $text-secondary;
    border: 2rpx solid $border-color;
    
    &.active {
      background-color: $primary-color;
      color: white;
      border-color: $primary-color;
    }
  }
}

/* 新增部门选择器样式 */
.relative {
  position: relative;
}

.absolute {
  position: absolute;
  left: 0;
  right: 0;
  top: 100%;
  margin-top: 10rpx;
  background-color: white;
  border-radius: 12rpx;
  box-shadow: 0 6rpx 20rpx rgba(0, 0, 0, 0.1);
  max-height: 300rpx;
  overflow-y: auto;
  z-index: 10;
}

.dept-selector {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 28rpx;
  color: $text-primary;
}

.selector-value {
  flex: 1;
  text-align: right;
  color: $text-tertiary;
}

.selector-value:not(:empty) {
  color: $text-primary;
}

.selector-icon {
  color: $text-tertiary;
  font-size: 24rpx;
}

.dept-list {
  // 样式在.absolute中定义
}

.dept-item {
  padding: 20rpx 30rpx;
  font-size: 28rpx;
  color: $text-primary;
  border-bottom: 2rpx solid $border-color;
  
  &:last-child {
    border-bottom: none;
  }
  
  &:hover {
    background-color: $bg-color;
  }
}

.submit-container {
  padding: 40rpx 30rpx;
}

.submit-btn {
  width: 100%;
  height: 90rpx;
  background: linear-gradient(135deg, $primary-color 0%, $secondary-color 100%);
  color: white;
  font-size: 32rpx;
  font-weight: 500;
  border-radius: 45rpx;
  box-shadow: 0 6rpx 16rpx rgba(125, 121, 244, 0.3);
}
</style>
    