<template>
  <view class="container">
    <!-- 顶部导航 -->
    <view class="header">
      <view class="back-btn" @click="goBack">
        <i class="fa fa-arrow-left"></i>
      </view>
      <view class="title">公告详情</view>
    </view>
    
    <!-- 公告内容 -->
    <view class="notice-container">
      <view class="notice-card" v-if="notice">
        <view class="notice-title">
          {{ notice.title }}
          <view class="status-tag" :class="{'public': notice.type === 'public', 'internal': notice.type === 'internal'}">
            {{ notice.type === 'public' ? '公开' : '内部' }}
          </view>
        </view>
        
        <view class="notice-meta">
          <view class="author">
            <i class="fa fa-user-o"></i>
            <text>{{ notice.clubName }}</text>
          </view>
          <view class="date">
            <i class="fa fa-calendar-o"></i>
            <text>{{ formatDate(notice.createdAt) }}</text>
          </view>
        </view>
        
        <view class="notice-content" v-html="notice.content"></view>
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
export default {
  data() {
    return {
      notice: null
    }
  },
  onLoad(options) {
    this.getNoticeDetail(options.id);
  },
  methods: {
    getNoticeDetail(id) {
      uni.showLoading({
        title: '加载中...'
      });
      
      uni.request({
        url: `http://localhost:8080/happy/notices/${id}`,
        method: 'GET',
        success: (res) => {
          if (res.data.code === 200) {
            this.notice = res.data.data;
          } else {
            uni.showToast({
              title: '获取公告详情失败',
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
    
    formatDate(timeStr) {
      if (!timeStr) return '未指定时间';
      const date = new Date(timeStr);
      return `${date.getFullYear()}-${(date.getMonth()+1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')} ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`;
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
$public-color: #34C759;
$internal-color: #646cff;
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

.notice-container {
  padding: 20rpx;
}

.notice-card {
  background-color: white;
  border-radius: 16rpx;
  padding: 30rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.05);
  
  .notice-title {
    font-size: 36rpx;
    font-weight: 500;
    color: $text-primary;
    margin-bottom: 20rpx;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  
  .status-tag {
    padding: 6rpx 16rpx;
    border-radius: 18rpx;
    font-size: 24rpx;
    color: white;
    
    &.public {
      background-color: $public-color;
    }
    
    &.internal {
      background-color: $internal-color;
    }
  }
  
  .notice-meta {
    display: flex;
    align-items: center;
    color: $text-tertiary;
    font-size: 26rpx;
    margin-bottom: 30rpx;
    
    .author, .date {
      display: flex;
      align-items: center;
      margin-right: 40rpx;
      
      i {
        margin-right: 10rpx;
        color: $primary-color;
      }
    }
  }
  
  .notice-content {
    font-size: 28rpx;
    color: $text-primary;
    line-height: 1.6;
    
    // 为HTML内容中的元素添加样式
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
    