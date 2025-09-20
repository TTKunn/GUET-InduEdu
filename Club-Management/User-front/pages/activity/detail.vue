<template>
  <view class="container">
    <!-- 顶部导航 -->
    <view class="header">
      <view class="back-btn" @click="goBack">
        <i class="fa fa-arrow-left"></i>
      </view>
      <view class="title">活动详情</view>
    </view>
    
    <!-- 活动内容 -->
    <view class="activity-container">
      <view class="activity-card" v-if="activity">
        <!-- 活动标题和状态 -->
        <view class="activity-header">
          <view class="activity-title">{{ activity.name }}</view>
          <view 
            class="status-tag" 
            :class="{
              'status-pending': activity.status === 0,
              'status-active': activity.status === 1,
              'status-ended': activity.status === 2
            }"
          >
            {{ getStatusText(activity.status) }}
          </view>
        </view>
        
        <!-- 活动信息 -->
        <view class="activity-info">
          <view class="info-item">
            <i class="fa fa-calendar-o"></i>
            <view class="info-content">
              <view class="info-title">活动时间</view>
              <view class="info-value">{{ formatDateTime(activity.startTime) }} - {{ formatDateTime(activity.endTime) }}</view>
            </view>
          </view>
          
          <view class="info-item">
            <i class="fa fa-map-marker"></i>
            <view class="info-content">
              <view class="info-title">活动地点</view>
              <view class="info-value">{{ activity.location }}</view>
            </view>
          </view>
          
          <view class="info-item">
            <i class="fa fa-user-o"></i>
            <view class="info-content">
              <view class="info-title">组织者</view>
              <view class="info-value">{{ activity.clubName || activity.nickName || '未知组织者' }}</view>
            </view>
          </view>
          
          <view class="info-item">
            <i class="fa fa-clock-o"></i>
            <view class="info-content">
              <view class="info-title">发布时间</view>
              <view class="info-value">{{ formatDateTime(activity.publishTime) }}</view>
            </view>
          </view>
          
          <view class="info-item">
            <i class="fa fa-users"></i>
            <view class="info-content">
              <view class="info-title">参与人数</view>
              <view class="info-value">{{ activity.participantCount || 0 }}人参与</view>
            </view>
          </view>
        </view>
        
        <!-- 活动描述 -->
        <view class="activity-description">
          <view class="section-header">
            <view class="section-title">活动详情</view>
          </view>
          <view class="section-content" v-html="activity.description"></view>
        </view>
        
        <!-- 操作按钮 -->
        <view class="action-buttons" v-if="showJoinButton">
          <button class="join-btn" @click="joinActivity">
            <i class="fa fa-check-circle"></i>
            <text>我要报名</text>
          </button>
        </view>
      </view>
      
      <!-- 加载状态 -->
      <view v-else class="loading-container">
        <view class="loading-spinner"></view>
        <text>加载中...</text>
      </view>
    </view>
  </view>
</template>

<script>
import { mapState } from 'vuex';

export default {
  computed: {
    ...mapState(['userInfo'])
  },
  data() {
    return {
      activity: null,
      showJoinButton: true
    }
  },
  onLoad(options) {
	  console.log(options.id)
    this.getActivityDetail(options.id);
  },
  methods: {
    getActivityDetail(id) {
      uni.showLoading({
        title: '加载中...'
      });
      
      uni.request({
        url: `http://localhost:8080/happy/activities/${id}`,
        method: 'GET',
        success: (res) => {
          if (res.data.code === 200) {
            this.activity = res.data.data;
            // 根据活动状态决定是否显示报名按钮
            if (this.activity.isEnded !== 0) { // 非未开始状态
              this.showJoinButton = false;
            }
          } else {
            uni.showToast({
              title: '获取活动详情失败',
              icon: 'none'
            });
          }
        },
        fail: () => {
          uni.showToast({
            title: '网络错误',
            icon: 'none'
          });
        },
        complete: () => {
          uni.hideLoading();
        }
      });
    },
    
    joinActivity() {
      // 检查用户是否已登录
      const userId = this.userInfo.userId;
      if (!userId) {
        uni.showModal({
          title: '提示',
          content: '请先登录再报名参加活动',
          success: (res) => {
            if (res.confirm) {
              uni.navigateTo({
                url: '/pages/login/login'
              });
            }
          }
        });
        return;
      }
      
      uni.showLoading({
        title: '报名中...'
      });
      
      uni.request({
        url: 'http://localhost:8080/happy/activities/join',
        method: 'POST',
        data: {
          activityId: this.activity.activityId,
          userId: userId
        },
        success: (res) => {
          if (res.data.code === 200) {
            uni.showToast({
              title: '报名成功',
              icon: 'success'
            });
            this.showJoinButton = false; // 报名成功后隐藏报名按钮
          } else {
            uni.showToast({
              title: res.data.msg || '报名失败',
              icon: 'none'
            });
          }
        },
        fail: () => {
          uni.showToast({
            title: '网络错误',
            icon: 'none'
          });
        },
        complete: () => {
          uni.hideLoading();
        }
      });
    },
    
    formatDateTime(dateStr) {
      if (!dateStr) return '未指定时间';
      const date = new Date(dateStr);
      return `${date.getFullYear()}-${(date.getMonth()+1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')} ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`;
    },
    
    getStatusText(status) {
      switch(status) {
        case 0: return '未开始';
        case 1: return '进行中';
        case 2: return '已结束';
        default: return '未知状态';
      }
    },
    
    goBack() {
      uni.navigateBack();
    }
  }
}
</script>

<style lang="scss" scoped>
$primary-color: #7d79f4;
$secondary-color: #9d99ff;
$status-pending: #FF9500;
$status-active: #34C759;
$status-ended: #999;
$text-primary: #333;
$text-secondary: #666;
$text-tertiary: #999;
$bg-color: #f5f5f7;

.container {
  background-color: $bg-color;
  min-height: 100vh;
}

.header {
  height: 88rpx;
  background-color: white;
  display: flex;
  align-items: center;
  padding: 0 30rpx;
  box-shadow: 0 2rpx 4rpx rgba(0, 0, 0, 0.05);
  
  .back-btn {
    width: 40rpx;
    height: 40rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    color: $text-primary;
  }
  
  .title {
    flex: 1;
    text-align: center;
    font-size: 36rpx;
    font-weight: 500;
    color: $text-primary;
  }
}

.activity-container {
  padding: 20rpx;
}

.activity-card {
  background-color: white;
  border-radius: 16rpx;
  padding: 30rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.05);
}

.activity-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30rpx;
}

.activity-title {
  font-size: 36rpx;
  font-weight: 500;
  color: $text-primary;
  max-width: 80%;
}

.status-tag {
  padding: 6rpx 16rpx;
  border-radius: 18rpx;
  font-size: 24rpx;
  color: white;
}

.status-pending {
  background-color: $status-pending;
}

.status-active {
  background-color: $status-active;
}

.status-ended {
  background-color: $status-ended;
}

.activity-info {
  margin-bottom: 30rpx;
}

.info-item {
  display: flex;
  align-items: center;
  padding: 15rpx 0;
  border-bottom: 1rpx solid #f5f5f7;
  
  i {
    width: 40rpx;
    color: $primary-color;
    font-size: 28rpx;
  }
}

.info-content {
  flex: 1;
  
  .info-title {
    font-size: 26rpx;
    color: $text-tertiary;
  }
  
  .info-value {
    font-size: 28rpx;
    color: $text-secondary;
  }
}

.activity-description {
  margin-bottom: 30rpx;
}

.section-header {
  margin-bottom: 20rpx;
  padding-bottom: 15rpx;
  border-bottom: 2rpx solid #f5f5f7;
}

.section-title {
  font-size: 32rpx;
  font-weight: 500;
  color: $text-primary;
  position: relative;
  
  &::before {
    content: '';
    position: absolute;
    left: 0;
    bottom: -15rpx;
    width: 60rpx;
    height: 4rpx;
    background-color: $primary-color;
    border-radius: 2rpx;
  }
}

.section-content {
  font-size: 28rpx;
  color: $text-secondary;
  line-height: 1.8;
  
  img {
    max-width: 100%;
    height: auto;
    margin: 20rpx 0;
    border-radius: 8rpx;
  }
  
  p {
    margin-bottom: 20rpx;
  }
  
  h1, h2, h3, h4, h5, h6 {
    color: $text-primary;
    font-weight: 500;
    margin-top: 30rpx;
    margin-bottom: 20rpx;
  }
  
  ul, ol {
    margin-left: 40rpx;
    margin-bottom: 20rpx;
  }
  
  li {
    margin-bottom: 10rpx;
  }
}

.action-buttons {
  padding: 20rpx 0;
}

.join-btn {
  width: 100%;
  height: 88rpx;
  background: linear-gradient(135deg, $primary-color 0%, $secondary-color 100%);
  border-radius: 44rpx;
  color: white;
  font-size: 32rpx;
  font-weight: 500;
  box-shadow: 0 8rpx 20rpx rgba(125, 121, 244, 0.3);
  transition: all 0.3s;
  
  &:active {
    transform: scale(0.98);
    box-shadow: 0 4rpx 10rpx rgba(125, 121, 244, 0.3);
  }
  
  i {
    margin-right: 15rpx;
  }
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60rpx 0;
  
  .loading-spinner {
    width: 60rpx;
    height: 60rpx;
    border: 6rpx solid $primary-color;
    border-radius: 50%;
    border-top-color: transparent;
    animation: spin 1s linear infinite;
    margin-bottom: 20rpx;
  }
  
  text {
    font-size: 28rpx;
    color: $text-tertiary;
  }
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
    