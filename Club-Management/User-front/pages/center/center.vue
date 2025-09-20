<template>
  <view class="container">
    <!-- 顶部个人信息卡片 -->
    <view class="profile-card">
      <view class="avatar-container">
        <image :src="getFullImageUrl(userInfo.avatar)" class="avatar" mode="aspectFill"/>
        <text class="username">{{ userInfo.username || '未设置' }}</text>
      </view>
      <view class="stats">
        <view class="stat-item">
          <text class="stat-value">1</text>
          <text class="stat-label">社团</text>
        </view>
        <view class="stat-item">
          <text class="stat-value">5</text>
          <text class="stat-label">活动</text>
        </view>
		<!-- 2025/5/20 古烜坤写的假数据嘻嘻哈哈哈 -->
<!--        <view class="stat-item">
          <text class="stat-value">0</text>
          <text class="stat-label">公告</text>
        </view> -->
      </view>
    </view>
    
    <!-- 个人信息详情 -->
    <view class="info-container">
      <view class="section-title">基本信息</view>
      
      <view class="info-list">
        <view class="info-item">
          <text class="item-label">昵称</text>
          <text class="item-value">{{ userInfo.nickName || '未设置' }}</text>
        </view>
        
        <view class="info-item">
          <text class="item-label">邮箱</text>
          <text class="item-value">{{ userInfo.email || '未设置' }}</text>
        </view>
        
        <view class="info-item">
          <text class="item-label">手机号</text>
          <text class="item-value">{{ userInfo.phonenumber || '未设置' }}</text>
        </view>
        
        <view class="info-item">
          <text class="item-label">性别</text>
          <text class="item-value">{{ formatGender(userInfo.sex) }}</text>
        </view>
        
        <view class="info-item">
          <text class="item-label">部门</text>
          <text class="item-value">{{ userInfo.deptName || '未设置' }}</text>
        </view>
      </view>
    </view>
    
    <!-- 操作按钮 -->
    <view class="action-container">
      <button class="edit-btn" @click="navigateToEdit">
        <text class="btn-text">修改个人信息</text>
      </button>
    </view>
    
    <!-- 社团活动快捷入口 -->
    <view class="quick-actions">
      <view class="action-item" @click="navigateToClubs">
        <text class="action-icon"><i class="fa fa-users"></i></text>
        <text class="action-text">我的社团</text>
      </view>
      <view class="action-item" @click="navigateToActivities">
        <text class="action-icon"><i class="fa fa-calendar"></i></text>
        <text class="action-text">我的活动</text>
      </view>
    </view>
  </view>
</template>

<script>
import { mapState } from 'vuex'

export default {
  data() {
    return {
		// 以后还是要把基础地址分离出来，我开发小程序这个只花了4天，我不是很会前端，所有没有配置api地址到配置文件，望谅解
      // 后期 api统一分离出来
	  // 2025-5-20
	  baseUrl: "http://localhost:8080" // 后端API基础地址
    }
  },
  computed: {
    ...mapState(['userInfo']) // 从 Vuex 获取 userInfo
  },
  onLoad() {
    this.loadUserInfo();
  },
  methods: {
    // 加载用户信息
    loadUserInfo() {
      const userId = this.userInfo.userId;
      if (!userId) {
        uni.showToast({
          title: '未登录或用户ID缺失',
          icon: 'none'
        });
        return;
      }
      uni.request({
        url: `${this.baseUrl}/happy/user/detail/${userId}`,
        method: 'GET',
        success: (res) => {
          if (res.data.code === 200) {
            this.$store.commit('setUserInfo', res.data.data);
          } else {
            uni.showToast({
              title: res.data.msg || '获取用户信息失败',
              icon: 'none'
            });
          }
        },
        fail: (err) => {
          console.error('获取用户信息失败:', err);
          uni.showToast({
            title: '获取用户信息失败',
            icon: 'none'
          });
        }
      });
    },

    // 获取完整图片URL
    getFullImageUrl(relativeUrl) {
      if (!relativeUrl) {
        return '/static/avatar.png';
      }
      return `${this.baseUrl}${relativeUrl}`;
    },

    // 格式化性别
    formatGender(genderCode) {
      if (genderCode === '0') return '男';
      if (genderCode === '1') return '女';
      return '未知';
    },

    // 导航到编辑页面
    navigateToEdit() {
      uni.navigateTo({
        url: '/pages/profile/edit'
      })
    },
    
    // 导航到社团页面
    navigateToClubs() {
      uni.switchTab({
          url: '/pages/club/list' // 确保这个路径是在 app.json 的 tabBar.list 中配置的
        })
    },
    
    // 导航到活动页面
    navigateToActivities() {
      uni.navigateTo({
        url: '/pages/activity/my'
      })
    }
  }
}
</script>

<style lang="scss">
.container {
  background-color: #f5f5f5;
  min-height: 100vh;
}

/* 个人信息卡片 */
.profile-card {
  background: linear-gradient(135deg, #7d79f4 0%, #9d99ff 100%);
  padding: 40rpx 0;
  margin: 20rpx;
  border-radius: 20rpx;
  box-shadow: 0 10rpx 20rpx rgba(0, 0, 0, 0.1);
  
  .avatar-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 30rpx;
    
    .avatar {
      width: 160rpx;
      height: 160rpx;
      border-radius: 50%;
      border: 4rpx solid white;
      box-shadow: 0 4rpx 10rpx rgba(0, 0, 0, 0.1);
    }
    
    .username {
      color: white;
      font-size: 36rpx;
      font-weight: 500;
      margin-top: 20rpx;
    }
  }
  
  .stats {
    display: flex;
    justify-content: space-around;
    padding: 0 40rpx;
    
    .stat-item {
      display: flex;
      flex-direction: column;
      align-items: center;
      
      .stat-value {
        color: white;
        font-size: 32rpx;
        font-weight: bold;
      }
      
      .stat-label {
        color: rgba(255, 255, 255, 0.8);
        font-size: 24rpx;
        margin-top: 10rpx;
      }
    }
  }
}

/* 信息容器 */
.info-container {
  background-color: white;
  margin: 20rpx;
  border-radius: 20rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.05);
  
  .section-title {
    font-size: 32rpx;
    font-weight: 500;
    color: #333;
    padding: 24rpx 30rpx;
    border-bottom: 2rpx solid #f0f0f0;
  }
  
  .info-list {
    padding: 20rpx 0;
    
    .info-item {
      display: flex;
      padding: 24rpx 30rpx;
      border-bottom: 2rpx solid #f0f0f0;
      
      &:last-child {
        border-bottom: none;
      }
      
      .item-label {
        font-size: 28rpx;
        color: #666;
        width: 240rpx;
      }
      
      .item-value {
        font-size: 28rpx;
        color: #333;
        flex: 1;
        text-align: right;
      }
    }
  }
}

/* 操作按钮 */
.action-container {
  margin: 40rpx 20rpx;
  
  .edit-btn {
    background: linear-gradient(135deg, #7d79f4 0%, #9d99ff 100%);
    color: white;
    font-size: 32rpx;
    height: 90rpx;
    line-height: 90rpx;
    border-radius: 45rpx;
    box-shadow: 0 6rpx 16rpx rgba(125, 121, 244, 0.3);
    
    .btn-text {
      font-weight: 500;
    }
  }
}

/* 快捷操作 */
.quick-actions {
  display: flex;
  margin: 20rpx;
  background-color: white;
  border-radius: 20rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.05);
  
  .action-item {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 30rpx 0;
    
    .action-icon {
      font-size: 48rpx;
      color: #7d79f4;
      margin-bottom: 16rpx;
    }
    
    .action-text {
      font-size: 28rpx;
      color: #333;
    }
  }
}
</style>
    