<template>
  <view class="login-container">
    <!-- 背景装饰 -->
    <view class="bg-decoration"></view>
    
    <!-- 登录卡片 -->
    <view class="login-card">
      <!-- 顶部Logo -->
      <view class="logo-container">
        <view class="logo">
          <i class="fa fa-user-circle-o"></i>
        </view>
        <view class="app-name">快乐社团平台</view>
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
        
        <!-- 错误提示 -->
        <view class="error-message" v-if="message">
          <i class="fa fa-exclamation-circle"></i>
          <text>{{ message }}</text>
        </view>
        
        <!-- 登录按钮 -->
        <button class="login-btn" @click="login">
          <text>登录</text>
        </button>
        
        <!-- 注册链接 -->
        <view class="register-link">
          <text>还没有账号？</text>
          <text class="register-text" @click="goRegister">立即注册</text>
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
import { mapMutations } from 'vuex'

export default {
  data() {
    return {
      username: '',
      password: '',
      message: '',
      loading: false
    }
  },
  methods: {
    ...mapMutations(['setUserInfo']),

    login() {
      // 表单验证
      if (!this.username.trim()) {
        this.showError('请输入用户名')
        return
      }
      
      if (!this.password.trim()) {
        this.showError('请输入密码')
        return
      }
      
      // 显示加载状态
      this.loading = true
      this.message = ''
      
      uni.request({
        url: 'http://localhost:8080/happy/login',
        method: 'GET',
        data: {
          username: this.username,
          password: this.password
        },
        success: (res) => {
          if (res.data.code === 200) {
            // 登录成功
            const userInfo = res.data.data
            
            // 保存用户信息
            this.setUserInfo(userInfo)
            uni.setStorageSync('userInfo', userInfo)
            
            // 跳转到首页
            uni.switchTab({
              url: '/pages/index/index',
              success: () => {
                uni.showToast({
                  title: '登录成功',
                  icon: 'success'
                })
              }
            })
          } else {
            // 登录失败
            this.showError(res.data.msg || '用户名或密码错误')
          }
        },
        fail: (err) => {
          // 请求失败
          this.showError('网络请求失败，请稍后重试')
          console.error('登录请求失败:', err)
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
    
    goRegister() {
      uni.navigateTo({
        url: '/pages/register/register'
      })
    }
  }
}
</script>

<style lang="scss" scoped>
$primary-color: #7d79f4;
$secondary-color: #9d99ff;
$error-color: #ff4d4f;
$text-primary: #333;
$text-secondary: #666;
$text-tertiary: #999;
$bg-color: #f5f5f7;

.login-container {
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
  top: -100rpx;
  left: -100rpx;
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
  bottom: -300rpx;
  right: -200rpx;
  width: 500rpx;
  height: 500rpx;
  border-radius: 50%;
  background: linear-gradient(135deg, $secondary-color 0%, $primary-color 100%);
  opacity: 0.08;
}

.login-card {
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
  background: linear-gradient(135deg, $primary-color 0%, $secondary-color 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20rpx;
  box-shadow: 0 6rpx 20rpx rgba(125, 121, 244, 0.3);
  
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

.login-btn {
  width: 100%;
  height: 88rpx;
  background: linear-gradient(135deg, $primary-color 0%, $secondary-color 100%);
  border-radius: 44rpx;
  color: white;
  font-size: 32rpx;
  font-weight: 500;
  margin-top: 20rpx;
  box-shadow: 0 8rpx 20rpx rgba(125, 121, 244, 0.3);
  transition: all 0.3s;
  
  &:active {
    transform: scale(0.98);
    box-shadow: 0 4rpx 10rpx rgba(125, 121, 244, 0.3);
  }
  
  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
}

.register-link {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 40rpx;
  font-size: 26rpx;
  color: $text-tertiary;
  
  .register-text {
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
    