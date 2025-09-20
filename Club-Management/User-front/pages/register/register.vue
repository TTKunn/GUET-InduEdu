<template>
  <view class="register-container">
    <!-- 背景装饰 -->
    <view class="bg-decoration"></view>
    
    <!-- 注册卡片 -->
    <view class="register-card">
      <!-- 顶部Logo -->
      <view class="logo-container">
        <view class="logo">
          <i class="fa fa-user-plus"></i>
        </view>
        <view class="app-name">快乐社团平台</view>
        <view class="subtitle">创建您的账号</view>
      </view>
      
      <!-- 表单 -->
      <view class="form-container">
        <view class="form-group">
          <view class="input-icon">
            <i class="fa fa-user-o"></i>
          </view>
          <input 
            v-model="username" 
            placeholder="请输入用户名" 
            class="form-input"
            placeholder-class="placeholder-style"
          />
        </view>
        
        <view class="form-group">
          <view class="input-icon">
            <i class="fa fa-id-card-o"></i>
          </view>
          <input 
            v-model="name" 
            placeholder="请输入姓名" 
            class="form-input"
            placeholder-class="placeholder-style"
          />
        </view>
        
        <view class="form-group relative"> <!-- 添加relative类 -->
          <view class="input-icon">
            <i class="fa fa-building-o"></i>
          </view>
          <view class="select-wrapper" @click="showDeptList = true">
            <text class="select-value">{{ selectedDeptName || '请选择学院' }}</text>
            <i class="fa fa-chevron-down select-icon"></i>
          </view>
          
          <!-- 学院下拉列表 -->
          <view class="dept-list absolute" v-show="showDeptList"> <!-- 添加absolute类 -->
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
        
        <view class="form-group gender-group">
          <view class="input-icon">
            <i class="fa fa-venus-mars"></i>
          </view>
          <view class="gender-options">
            <view 
              class="gender-option" 
              :class="{'active': gender === '0'}" 
              @click="gender = '0'"
            >
              <text>男</text>
            </view>
            <view 
              class="gender-option" 
              :class="{'active': gender === '1'}" 
              @click="gender = '1'"
            >
              <text>女</text>
            </view>
            <view 
              class="gender-option" 
              :class="{'active': gender === '2'}" 
              @click="gender = '2'"
            >
              <text>保密</text>
            </view>
          </view>
        </view>
        
        <view class="form-group">
          <view class="input-icon">
            <i class="fa fa-lock"></i>
          </view>
          <input 
            v-model="password" 
            placeholder="请输入密码" 
            password 
            class="form-input"
            placeholder-class="placeholder-style"
          />
        </view>
        
        <view class="form-group">
          <view class="input-icon">
            <i class="fa fa-lock"></i>
          </view>
          <input 
            v-model="confirmPassword" 
            placeholder="请再次输入密码" 
            password 
            class="form-input"
            placeholder-class="placeholder-style"
          />
        </view>
        
        <!-- 错误提示 -->
        <view class="error-message" v-if="message">
          <i class="fa fa-exclamation-circle"></i>
          <text>{{ message }}</text>
        </view>
        
        <!-- 注册按钮 -->
        <button class="register-btn" @click="register">
          <text>注册</text>
        </button>
        
        <!-- 登录链接 -->
        <view class="login-link">
          <text>已有账号？</text>
          <text class="login-text" @click="goLogin">立即登录</text>
        </view>
      </view>
    </view>
    
    <!-- 底部版权信息 -->
    <view class="copyright">
      <text>© 2025 快乐社团平台 版权所有</text>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      name: '',
      deptId: '',      // 新增：学院ID
      selectedDeptName: '', // 新增：选中的学院名称
      deptList: [],    // 新增：学院列表
      showDeptList: false, // 新增：控制下拉列表显示
      gender: '2', // 默认保密
      password: '',
      confirmPassword: '',
      message: '',
      loading: false
    }
  },
  onLoad() {
    // 页面加载时获取学院列表
    this.loadDeptList();
  },
  methods: {
    // 加载学院列表
    loadDeptList() {
      uni.request({
        url: 'http://localhost:8080/happy/dept/list',
        method: 'GET',
        success: (res) => {
          if (res.data.code === 200) {
            this.deptList = res.data.data || [];
          } else {
            uni.showToast({
              title: '获取学院列表失败',
              icon: 'none'
            });
          }
        },
        fail: () => {
          uni.showToast({
            title: '网络错误，获取学院列表失败',
            icon: 'none'
          });
        }
      });
    },
    
    // 选择学院
    selectDept(dept) {
      this.deptId = dept.deptId;
      this.selectedDeptName = dept.deptName;
      this.showDeptList = false;
    },
    
    register() {
      // 表单验证
      if (!this.username.trim()) {
        this.showError('请输入用户名')
        return
      }
      
      if (!this.name.trim()) {
        this.showError('请输入姓名')
        return
      }
      
      if (!this.deptId) {
        this.showError('请选择学院')
        return
      }
      
      if (!this.password.trim()) {
        this.showError('请输入密码')
        return
      }
      
      // 密码强度验证（示例：至少6个字符）
      if (this.password.length < 6) {
        this.showError('密码长度至少为6个字符')
        return
      }
      
      if (this.password !== this.confirmPassword) {
        this.showError('两次输入的密码不一致')
        return
      }
      
      // 显示加载状态
      this.loading = true
      this.message = ''
      
      uni.request({
        url: 'http://localhost:8080/happy/register',
        method: 'POST',
        data: {
          username: this.username,
          password: this.password,
          name: this.name,
          deptId: this.deptId, // 保存deptId而非deptName
          gender: this.gender
        },
        success: (res) => {
          if (res.data.code === 200) {
            // 注册成功
            uni.showToast({
              title: '注册成功，请登录',
              icon: 'success',
              duration: 2000
            })
            
            // 延迟跳转到登录页面
            setTimeout(() => {
              uni.navigateTo({
                url: '/pages/login/login'
              })
            }, 2000)
          } else {
            // 注册失败
            this.showError(res.data.msg || '注册失败，请重试')
          }
        },
        fail: (err) => {
          // 请求失败
          this.showError('网络请求失败，请稍后重试')
          console.error('注册请求失败:', err)
        },
        complete: () => {
          // 隐藏加载状态
          this.loading = false
        }
      })
    },
    
    showError(msg) {
      this.message = msg
      
      // 3秒后自动清除错误信息
      setTimeout(() => {
        this.message = ''
      }, 3000)
    },
    
    goLogin() {
      uni.navigateBack()
    }
  }
}
</script>

<style lang="scss" scoped>
$primary-color: #7d79f4;
$secondary-color: #9d99ff;
$success-color: #34C759;
$error-color: #ff4d4f;
$text-primary: #333;
$text-secondary: #666;
$text-tertiary: #999;
$bg-color: #f5f5f7;

.register-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: $bg-color;
  position: relative;
  overflow: hidden;
}

.bg-decoration {
  position: absolute;
  top: -150rpx;
  right: -150rpx;
  width: 400rpx;
  height: 400rpx;
  border-radius: 50%;
  background: linear-gradient(135deg, $primary-color 0%, $secondary-color 100%);
  opacity: 0.1;
  z-index: 0;
}

.bg-decoration::after {
  content: '';
  position: absolute;
  bottom: -200rpx;
  left: -200rpx;
  width: 500rpx;
  height: 500rpx;
  border-radius: 50%;
  background: linear-gradient(135deg, $secondary-color 0%, $primary-color 100%);
  opacity: 0.08;
}

.register-card {
  width: 85%;
  max-width: 600rpx;
  background-color: white;
  border-radius: 24rpx;
  box-shadow: 0 10rpx 40rpx rgba(0, 0, 0, 0.08);
  padding: 60rpx 40rpx;
  position: relative;
  z-index: 1;
  transform: translateY(-30rpx);
}

.logo-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 60rpx;
}

.logo {
  width: 120rpx;
  height: 120rpx;
  background: linear-gradient(135deg, $success-color 0%, #22C55E 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20rpx;
  box-shadow: 0 6rpx 20rpx rgba(52, 199, 89, 0.3);
  
  i {
    color: white;
    font-size: 60rpx;
  }
}

.app-name {
  font-size: 36rpx;
  font-weight: 500;
  color: $text-primary;
}

.subtitle {
  font-size: 28rpx;
  color: $text-secondary;
  margin-top: 10rpx;
}

.form-container {
  width: 100%;
}

.form-group {
  display: flex;
  align-items: center;
  border-bottom: 2rpx solid #e6e6e6;
  padding: 15rpx 0;
  margin-bottom: 30rpx;
  transition: border-color 0.3s;
  
  &:focus-within {
    border-color: $primary-color;
  }
}

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

.gender-group {
  align-items: flex-start;
}

.input-icon {
  width: 40rpx;
  margin-right: 20rpx;
  color: $text-tertiary;
  
  i {
    font-size: 28rpx;
  }
}

.form-input {
  flex: 1;
  font-size: 28rpx;
  color: $text-primary;
  height: 40rpx;
}

.select-wrapper {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 28rpx;
  color: $text-primary;
  height: 40rpx;
}

.select-value {
  flex: 1;
  text-align: right;
  color: $text-tertiary;
}

.select-value:not(:empty) {
  color: $text-primary;
}

.select-icon {
  color: $text-tertiary;
  font-size: 24rpx;
}

.dept-list {
  // 原样式移到了.absolute类中
}

.dept-item {
  padding: 20rpx 30rpx;
  font-size: 28rpx;
  color: $text-primary;
  border-bottom: 2rpx solid #f5f5f5;
  
  &:last-child {
    border-bottom: none;
  }
  
  &:hover {
    background-color: #f5f5f5;
  }
}

.gender-options {
  flex: 1;
  display: flex;
}

.gender-option {
  padding: 10rpx 30rpx;
  border-radius: 30rpx;
  margin-right: 20rpx;
  font-size: 28rpx;
  color: $text-secondary;
  border: 2rpx solid #e6e6e6;
  transition: all 0.3s;
  
  &.active {
    background-color: $primary-color;
    color: white;
    border-color: $primary-color;
  }
}

.placeholder-style {
  color: $text-tertiary;
}

.error-message {
  display: flex;
  align-items: center;
  color: $error-color;
  font-size: 24rpx;
  margin-bottom: 30rpx;
  padding: 10rpx 0;
  opacity: 0;
  animation: fadeIn 0.3s forwards;
  
  i {
    margin-right: 10rpx;
  }
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10rpx); }
  to { opacity: 1; transform: translateY(0); }
}

.register-btn {
  width: 100%;
  height: 88rpx;
  background: linear-gradient(135deg, $success-color 0%, #22C55E 100%);
  border-radius: 44rpx;
  color: white;
  font-size: 32rpx;
  font-weight: 500;
  margin-top: 20rpx;
  box-shadow: 0 8rpx 20rpx rgba(52, 199, 89, 0.3);
  transition: all 0.3s;
  
  &:active {
    transform: scale(0.98);
    box-shadow: 0 4rpx 10rpx rgba(52, 199, 89, 0.3);
  }
  
  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
}

.login-link {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 40rpx;
  font-size: 26rpx;
  color: $text-tertiary;
  
  .login-text {
    color: $primary-color;
    margin-left: 10rpx;
    font-weight: 500;
    text-decoration: underline;
    cursor: pointer;
  }
}

.copyright {
  position: absolute;
  bottom: 40rpx;
  font-size: 22rpx;
  color: $text-tertiary;
}
</style>
    