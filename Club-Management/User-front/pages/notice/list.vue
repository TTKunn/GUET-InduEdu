<template>
  <view class="container">
    <!-- 顶部搜索栏 -->
    <view class="search-bar">
      <view class="search-box">
        <i class="fa fa-search"></i>
        <input type="text" placeholder="搜索公告或活动" @input="onSearchInput" />
      </view>
    </view>
    
    <!-- 切换选项卡 -->
    <view class="tab-bar">
      <view 
        :class="{'active': currentTab === 'notice'}" 
        @click="switchTab('notice')"
      >
        <i class="fa fa-bullhorn"></i>
        <text>公告</text>
      </view>
      <view 
        :class="{'active': currentTab === 'activity'}" 
        @click="switchTab('activity')"
      >
        <i class="fa fa-calendar"></i>
        <text>活动</text>
      </view>
    </view>
    
    <!-- 内容区域 -->
    <view class="content-area">
      <!-- 公告列表 -->
      <view v-if="currentTab === 'notice'">
        <view class="notice-list">
          <view 
            class="notice-item" 
            v-for="item in filteredNoticeList" 
            :key="item.announcementId" 
            @click="goNoticeDetail(item.announcementId)"
          >
            <view class="item-header">
              <view class="title">{{ item.title }}</view>
              <view class="status-tag" :class="item.type === 'public' ? 'public' : 'internal'">
                {{ item.type === 'public' ? '公开' : '内部' }}
              </view>
            </view>
            <view class="info">
              <text class="time">{{ formatDate(item.createdAt) }}</text>
              <text class="source">{{ item.clubName || '系统公告' }}</text>
            </view>
          </view>
        </view>
      </view>
      
      <!-- 活动列表 -->
      <view v-if="currentTab === 'activity'">
        <view class="activity-list">
          <view 
            class="activity-item" 
            v-for="item in filteredActivityList" 
            :key="item.activityId" 
            @click="goActivityDetail(item.activityId)"
          >
            <view class="item-header">
              <view class="title">{{ item.name }}</view>
              <view 
                class="status-tag" 
                :class="{
                  'status-pending': item.status === 0,
                  'status-active': item.status === 1,
                  'status-ended': item.status === 2
                }"
              >
                {{ getStatusText(item.status) }}
              </view>
            </view>
            <view class="time">
              <i class="fa fa-calendar-o"></i>
              <text>{{ formatDateTime(item.startTime) }} - {{ formatDate(item.endTime) }}</text>
            </view>
            <view class="location">
              <i class="fa fa-map-marker"></i>
              <text>{{ item.location }}</text>
            </view>
            <view class="organizer">
              <i class="fa fa-user-o"></i>
              <text>{{ item.clubName || item.nickName || '未知组织者' }}</text>
            </view>
          </view>
        </view>
      </view>
    </view>
    
    <!-- 加载状态 -->
    <view v-if="loading" class="loading-container">
      <view class="loading-spinner"></view>
      <text>加载中...</text>
    </view>
    
    <!-- 空状态 -->
    <view v-if="!loading && (currentTab === 'notice' ? filteredNoticeList.length === 0 : filteredActivityList.length === 0)" class="empty-container">
      <view class="empty-icon">
        <i class="fa fa-inbox"></i>
      </view>
      <text class="empty-text">暂无内容</text>
      <text class="empty-subtext">请稍后再试或刷新页面</text>
      <button class="refresh-btn" @click="refreshData">
        <i class="fa fa-refresh"></i>
        <text>刷新</text>
      </button>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      currentTab: 'notice',
      noticeList: [],
      activityList: [],
      searchKeyword: '',
      loading: false
    }
  },
  computed: {
    filteredNoticeList() {
      if (!this.searchKeyword) return this.noticeList;
      return this.noticeList.filter(item => 
        item.title.toLowerCase().includes(this.searchKeyword.toLowerCase())
      );
    },
    filteredActivityList() {
      if (!this.searchKeyword) return this.activityList;
      return this.activityList.filter(item => 
        item.name.toLowerCase().includes(this.searchKeyword.toLowerCase()) ||
        (item.clubName && item.clubName.toLowerCase().includes(this.searchKeyword.toLowerCase())) ||
        (item.location && item.location.toLowerCase().includes(this.searchKeyword.toLowerCase()))
      );
    }
  },
  onLoad() {
    this.getNoticeList();
  },
  onShow() {
    if (this.currentTab === 'activity' && this.activityList.length === 0) {
      this.getActivityList();
    }
  },
  methods: {
    switchTab(tab) {
      if (this.currentTab === tab) return;
      this.currentTab = tab;
      
      if (tab === 'activity' && this.activityList.length === 0) {
        this.getActivityList();
      }
    },
    
    getNoticeList() {
      this.loading = true;
      uni.request({
        url: 'http://localhost:8080/happy/notices/public',
        method: 'GET',
        success: (res) => {
          if (res.data.code === 200) {
            this.noticeList = res.data.data;
          } else {
            uni.showToast({
              title: '获取公告失败',
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
          this.loading = false;
        }
      });
    },
    
    getActivityList() {
      this.loading = true;
      uni.request({
        url: 'http://localhost:8080/happy/activities/public',
        method: 'GET',
        success: (res) => {
          if (res.data.code === 200) {
            this.activityList = res.data.data;
          } else {
            uni.showToast({
              title: '获取活动失败',
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
          this.loading = false;
        }
      });
    },
    
    goNoticeDetail(id) {
      uni.navigateTo({
        url: `/pages/notice/detail?id=${id}`
      });
    },
    
    goActivityDetail(id) {
      uni.navigateTo({
        url: `/pages/activity/detail?id=${id}`
      });
    },
    
    formatDate(dateStr) {
      if (!dateStr) return '未指定时间';
      const date = new Date(dateStr);
      return `${date.getFullYear()}-${(date.getMonth()+1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')}`;
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
    
    onSearchInput(e) {
      this.searchKeyword = e.detail.value;
    },
    
    refreshData() {
      if (this.currentTab === 'notice') {
        this.getNoticeList();
      } else {
        this.getActivityList();
      }
    }
  }
}
</script>

<style lang="scss" scoped>
$primary-color: #7d79f4;
$secondary-color: #9d99ff;
$public-color: #34C759;
$internal-color: #646cff;
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

.search-bar {
  padding: 20rpx;
}

.search-box {
  display: flex;
  align-items: center;
  height: 80rpx;
  background-color: white;
  border-radius: 40rpx;
  padding: 0 30rpx;
  box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.05);
  
  i {
    color: $text-tertiary;
    margin-right: 20rpx;
  }
  
  input {
    flex: 1;
    font-size: 28rpx;
    color: $text-primary;
  }
}

.tab-bar {
  display: flex;
  margin: 0 20rpx 20rpx;
  border-radius: 10rpx; // 减小选项卡圆角
  background-color: white;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.05); // 减小阴影强度
  
  view {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 15rpx 0; // 减小内边距
    font-size: 26rpx; // 减小字体大小
    color: $text-secondary;
    
    i {
      font-size: 30rpx; // 减小图标大小
      margin-bottom: 6rpx; // 减小图标和文字间距
    }
  }
  
  view.active {
    background: linear-gradient(135deg, $primary-color 0%, $secondary-color 100%);
    color: white;
    border-radius: 10rpx; // 减小选中状态圆角
    box-shadow: 0 3rpx 8rpx rgba(125, 121, 244, 0.3); // 减小选中状态阴影强度
  }
}

.content-area {
  padding: 0 20rpx;
}

.notice-list, .activity-list {
  padding-bottom: 20rpx;
}

.notice-item, .activity-item {
  background-color: white;
  border-radius: 16rpx;
  padding: 25rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.05);
  transition: transform 0.2s;
  
  &:active {
    transform: scale(0.99);
  }
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15rpx;
}

.title {
  font-size: 32rpx;
  font-weight: 500;
  color: $text-primary;
  max-width: 80%;
}

.status-tag {
  padding: 4rpx 12rpx;
  border-radius: 12rpx;
  font-size: 22rpx;
  color: white;
}

.public {
  background-color: $public-color;
}

.internal {
  background-color: $internal-color;
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

.info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 24rpx;
  color: $text-tertiary;
}

.time, .location, .organizer {
  display: flex;
  align-items: center;
  font-size: 26rpx;
  color: $text-secondary;
  margin-bottom: 10rpx;
  
  i {
    width: 30rpx;
    margin-right: 15rpx;
    color: $primary-color;
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

.empty-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60rpx 0;
  
  .empty-icon {
    width: 120rpx;
    height: 120rpx;
    border-radius: 50%;
    background-color: rgba(125, 121, 244, 0.1);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 30rpx;
    
    i {
      font-size: 60rpx;
      color: $primary-color;
    }
  }
  
  .empty-text {
    font-size: 32rpx;
    color: $text-primary;
    margin-bottom: 10rpx;
  }
  
  .empty-subtext {
    font-size: 26rpx;
    color: $text-tertiary;
    margin-bottom: 40rpx;
  }
  
  .refresh-btn {
    width: 200rpx;
    height: 72rpx;
    border-radius: 36rpx;
    background-color: $primary-color;
    color: white;
    font-size: 28rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    
    i {
      margin-right: 10rpx;
    }
  }
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
    