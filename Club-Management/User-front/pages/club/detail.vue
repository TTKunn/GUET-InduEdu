<template>
  <view class="container">
    <!-- 头部导航 -->
    <view class="header-nav">
      <text class="back-btn" @click="goBack"><i class="fa fa-arrow-left"></i></text>
      <text class="nav-title">{{ clubDetail.name || '社团详情' }}</text>
    </view>
    
    <!-- 头部图片 -->
    <view class="banner-container">
      <image 
        class="club-banner" 
        :src="getFullImageUrl(clubDetail.logoUrl)" 
        mode="aspectFill"
        @load="onBannerLoad"
      ></image>
      <view class="banner-mask"></view>
      <view class="club-basic-info">
        <text class="club-name">{{ clubDetail.name }}</text>
        <view class="info-tags">
          <text class="tag-item">{{ clubDetail.categoryName || '未知分类' }}</text>
          <text class="tag-item">{{ clubDetail.deptName || '未知学院' }}</text>
        </view>
      </view>
    </view>
    
    <!-- 社团数据统计 -->
    <view class="stats-container">
      <view class="stat-item">
        <text class="stat-value">{{ clubDetail.memberCount || 0 }}</text>
        <text class="stat-label">成员</text>
      </view>
      <view class="stat-item">
        <text class="stat-value">{{ clubDetail.activityCount || 0 }}</text>
        <text class="stat-label">活动</text>
      </view>
      <view class="stat-item">
        <text class="stat-value">{{ clubDetail.totalMembersEver || 0 }}</text>
        <text class="stat-label">历史成员</text>
      </view>
    </view>
    
    <!-- 社团详细信息 -->
    <view class="detail-container">
      <!-- 社团简介 -->
      <view class="section">
        <text class="section-title">社团简介</text>
        <text class="section-content">{{ clubDetail.description || '暂无简介' }}</text>
      </view>
      
      <!-- 社团基本信息 -->
      <view class="section">
        <text class="section-title">基本信息</text>
        <view class="info-list">
          <view class="info-item">
            <text class="item-label">社长</text>
            <text class="item-value">{{ clubDetail.nickName || '未知' }}</text>
          </view>
          <view class="info-item">
            <text class="item-label">创建时间</text>
            <text class="item-value">{{ formatDate(clubDetail.createdAt) }}</text>
          </view>
          <view class="info-item">
            <text class="item-label">活跃成员</text>
            <text class="item-value">{{ clubDetail.activeMemberCount || 0 }}人</text>
          </view>
        </view>
      </view>
      
      <!-- 成员分布 -->
      <view class="section" v-if="clubDetail.memberDistribution && clubDetail.memberDistribution.length">
        <text class="section-title">成员分布</text>
        <view class="distribution-chart">
          <view 
            class="distribution-item" 
            v-for="(item, index) in clubDetail.memberDistribution" 
            :key="index"
          >
            <view class="bar-container">
              <view 
                class="bar" 
                :style="{height: item.percentage + '%'}"
              ></view>
            </view>
            <text class="bar-label">{{ item.name }}</text>
            <text class="bar-value">{{ item.count }}人</text>
          </view>
        </view>
      </view>
      
      <!-- 最新活动 -->
      <view class="section" v-if="clubDetail.latestActivities && clubDetail.latestActivities.length">
        <text class="section-title">最新活动</text>
        <view class="activities-list">
          <view 
            class="activity-item" 
            v-for="activity in clubDetail.latestActivities" 
            :key="activity.activityId"
            @click="navigateToActivity(activity.activityId)"
          >
            <image class="activity-cover" :src="getFullImageUrl(activity.coverUrl)" mode="aspectFill" />
            <view class="activity-info">
              <text class="activity-title">{{ activity.title }}</text>
              <text class="activity-date">{{ formatDate(activity.startTime) }}</text>
            </view>
          </view>
        </view>
      </view>
    </view>
    
    <!-- 操作按钮区域 -->
    <view class="action-bar">
      <button v-if="isLeader" class="action-button manage-button" @click="handleManageClub">
        <text class="btn-icon"><i class="fa fa-cog"></i></text>
        <text class="btn-text">管理社团</text>
      </button>
      <button v-else-if="isMember" 
              class="action-button quit-button" 
              @click="handleQuitClub"
              :disabled="requesting">
        <text class="btn-icon"><i class="fa fa-sign-out"></i></text>
        <text class="btn-text">{{ requesting ? '处理中...' : '退出社团' }}</text>
      </button>
      <button v-else 
              class="action-button join-button" 
              @click="handleJoinClub"
              :disabled="requesting">
        <text class="btn-icon"><i class="fa fa-user-plus"></i></text>
        <text class="btn-text">{{ requesting ? '处理中...' : '申请加入' }}</text>
      </button>
    </view>
    
    <!-- 加载状态 -->
    <view v-if="loading" class="loading-mask">
      <view class="loading-container">
        <view class="loading-animation"></view>
        <text class="loading-text">加载中...</text>
      </view>
    </view>
    
    <!-- 错误状态 -->
    <view v-if="errorMessage" class="error-container">
      <text class="error-icon"><i class="fa fa-exclamation-triangle"></i></text>
      <text class="error-text">{{ errorMessage }}</text>
      <button class="retry-button" @click="retryLoad">重试</button>
    </view>
  </view>
</template>

<script>
import { mapState } from 'vuex';

export default {
  data() {
    return {
      clubDetail: {},
      loading: false,
      clubId: null,
      isMember: false,
      requesting: false,
      hasPendingRequest: false,
      bannerHeight: 0,
      showBackdrop: false,
      errorMessage: '',
      // 添加默认的baseUrl
      baseUrl: "http://localhost:8080"
    };
  },
  computed: {
    ...mapState(['userInfo']),
    isLeader() {
      return this.clubDetail.leaderId === this.userInfo.userId;
    }
  },
  onLoad(options) {
    this.clubId = options.clubId;
    this.loadClubDetail();
    this.checkMembership();
  },
  methods: {
    // 加载社团详情
    loadClubDetail() {
      // 检查baseUrl是否存在
      if (!this.baseUrl) {
        this.errorMessage = '服务器地址配置错误';
        this.loading = false;
        return;
      }
      
      this.loading = true;
      this.errorMessage = '';
      
      uni.request({
        url: `${this.baseUrl}/happy/club/detail/${this.clubId}`,
        method: 'GET',
        success: (res) => {
          if (res.data.code === 200) {
            this.clubDetail = res.data.data;
          } else {
            this.errorMessage = res.data.msg || '获取社团详情失败';
            uni.showToast({
              title: this.errorMessage,
              icon: 'none'
            });
          }
        },
        fail: (err) => {
          console.error('获取社团详情失败:', err);
          this.errorMessage = '网络请求失败，请检查网络连接';
          uni.showToast({
            title: this.errorMessage,
            icon: 'none'
          });
        },
        complete: () => {
          this.loading = false;
        }
      });
    },
    
    // 检查会员状态
    checkMembership() {
      // 检查baseUrl和userInfo是否存在
      if (!this.baseUrl || !this.userInfo || !this.userInfo.userId) {
        return;
      }
      
      uni.request({
        url: `${this.baseUrl}/happy/members/check`,
        method: 'GET',
        data: {
          userId: this.userInfo.userId,
          clubId: this.clubId
        },
        success: (res) => {
          if (res.data.code === 200) {
            this.isMember = res.data.data;
          }
        },
        fail: (err) => {
          console.error('检查成员状态失败:', err);
        }
      });
    },
    
    // 格式化日期
    formatDate(dateString) {
      if (!dateString) return '未知';
      const date = new Date(dateString);
      return `${date.getFullYear()}年${date.getMonth()+1}月${date.getDate()}日`;
    },
    
    // 获取完整图片URL
    getFullImageUrl(relativeUrl) {
      // 检查是否是绝对URL
      if (!relativeUrl) return '/static/default-club.png';
      if (relativeUrl.startsWith('http') || relativeUrl.startsWith('https')) {
        return relativeUrl;
      }
      // 确保baseUrl存在
      return this.baseUrl ? `${this.baseUrl}${relativeUrl}` : relativeUrl;
    },
    
    // 处理加入社团
    handleJoinClub() {
      if (this.requesting || this.hasPendingRequest) return;
      
      uni.showModal({
        title: '申请加入社团',
        content: '请输入申请备注',
        editable: true,
        placeholderText: '请填写申请理由...',
        success: (res) => {
          if (res.confirm) {
            const remark = res.content.trim();
            if (!remark) {
              uni.showToast({
                title: '备注不能为空',
                icon: 'none'
              });
              return;
            }
            
            this.requesting = true;
            this.hasPendingRequest = true;
            
            uni.showLoading({ title: '提交中...' });
            uni.request({
              url: `${this.baseUrl}/happy/members/join`,
              method: 'POST',
              data: { 
                userId: this.userInfo.userId,
                clubId: this.clubId,
                remark: remark
              },
              success: (res) => {
                if (res.data.code === 200 && res.data.data) {
                  this.isMember = true;
                  uni.showToast({
                    title: '申请已提交，等待审核',
                    icon: 'success'
                  });
                  this.loadClubDetail();
                } else if(res.data.code === 500 && res.data.msg === '该用户已加入该社团') {
                  uni.showToast({
                    title: '您申请过此社团',
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
                this.requesting = false;
                uni.hideLoading();
              }
            });
          }
        }
      });
    },
    
    // 处理退出社团
    handleQuitClub() {
      if (this.requesting || this.hasPendingRequest) return;
      
      uni.showModal({
        title: '退出社团',
        content: '确认退出该社团吗？',
        success: (res) => {
          if (res.confirm) {
            this.requesting = true;
            this.hasPendingRequest = true;
            
            uni.showLoading({ title: '处理中...' });
            uni.request({
              url: `${this.baseUrl}/happy/members/quit`,
              method: 'POST',
              data: { 
                userId: this.userInfo.userId,
                clubId: this.clubId
              },
              success: (res) => {
                if (res.data.code === 200 && res.data.data) {
                  this.isMember = false;
                  uni.showToast({
                    title: '已成功退出社团',
                    icon: 'success'
                  });
                  this.loadClubDetail();
                } else {
                  uni.showToast({
                    title: '退出失败，请稍后重试',
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
                this.requesting = false;
                uni.hideLoading();
              }
            });
          }
        }
      });
    },
    
    // 处理管理社团
    handleManageClub() {
      uni.navigateTo({
        url: `/pages/club/manage?clubId=${this.clubId}`
      });
    },
    
    // 返回上一页
    goBack() {
      uni.navigateBack();
    },
    
    // 图片加载完成
    onBannerLoad(e) {
      const { width, height } = e.detail;
      const windowWidth = uni.getSystemInfoSync().windowWidth;
      this.bannerHeight = (height / width) * windowWidth;
    },
    
    // 跳转到活动详情
    navigateToActivity(activityId) {
      uni.navigateTo({
        url: `/pages/activity/detail?activityId=${activityId}`
      });
    },
    
    // 重试加载
    retryLoad() {
      this.loadClubDetail();
      this.checkMembership();
    }
  }
};
</script>

<style lang="scss">
$primary-color: #7d79f4;
$secondary-color: #9d99ff;
$success-color: #34C759;
$danger-color: #FF3B30;
$text-primary: #333;
$text-secondary: #666;
$text-tertiary: #999;
$bg-color: #f5f5f5;

.container {
  min-height: 100vh;
  background-color: $bg-color;
  position: relative;
}

/* 头部导航 */
.header-nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 88rpx;
  display: flex;
  align-items: center;
  padding: 0 30rpx;
  z-index: 100;
  background-color: rgba(0, 0, 0, 0.3);
  
  .back-btn {
    font-size: 36rpx;
    color: white;
    width: 40rpx;
  }
  
  .nav-title {
    flex: 1;
    text-align: center;
    font-size: 32rpx;
    color: white;
    font-weight: 500;
  }
}

/* 头部图片 */
.banner-container {
  position: relative;
  overflow: hidden;
  
  .club-banner {
    width: 100%;
    height: 500rpx;
    display: block;
  }
  
  .banner-mask {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 120rpx;
    background: linear-gradient(to top, rgba(0, 0, 0, 0.7), transparent);
  }
  
  .club-basic-info {
    position: absolute;
    bottom: 30rpx;
    left: 30rpx;
    right: 30rpx;
    
    .club-name {
      font-size: 40rpx;
      font-weight: bold;
      color: white;
      text-shadow: 0 2rpx 4rpx rgba(0, 0, 0, 0.5);
      display: block;
      margin-bottom: 15rpx;
    }
    
    .info-tags {
      display: flex;
      flex-wrap: wrap;
      
      .tag-item {
        background-color: rgba(0, 0, 0, 0.4);
        color: white;
        font-size: 24rpx;
        padding: 6rpx 16rpx;
        border-radius: 20rpx;
        margin-right: 15rpx;
        margin-bottom: 10rpx;
      }
    }
  }
}

/* 数据统计 */
.stats-container {
  display: flex;
  background-color: white;
  padding: 30rpx 0;
  border-bottom: 1rpx solid #eee;
  
  .stat-item {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    
    .stat-value {
      font-size: 36rpx;
      font-weight: bold;
      color: $primary-color;
      margin-bottom: 10rpx;
    }
    
    .stat-label {
      font-size: 24rpx;
      color: $text-secondary;
    }
  }
}

/* 详情容器 */
.detail-container {
  padding: 20rpx;
}

.section {
  background-color: white;
  border-radius: 16rpx;
  margin-bottom: 20rpx;
  padding: 30rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.05);
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: $text-primary;
  margin-bottom: 25rpx;
  display: block;
}

.section-content {
  font-size: 28rpx;
  color: $text-secondary;
  line-height: 1.6;
}

/* 信息列表 */
.info-list {
  .info-item {
    display: flex;
    align-items: center;
    margin-bottom: 20rpx;
    
    &:last-child {
      margin-bottom: 0;
    }
    
    .item-label {
      width: 180rpx;
      font-size: 28rpx;
      color: $text-secondary;
    }
    
    .item-value {
      flex: 1;
      font-size: 28rpx;
      color: $text-primary;
    }
  }
}

/* 成员分布图表 */
.distribution-chart {
  display: flex;
  justify-content: space-between;
  height: 240rpx;
  
  .distribution-item {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 0 10rpx;
    
    .bar-container {
      width: 100%;
      height: 180rpx;
      background-color: #f5f5f5;
      border-radius: 8rpx;
      position: relative;
      overflow: hidden;
      
      .bar {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: $primary-color;
        transition: height 0.5s ease;
      }
    }
    
    .bar-label {
      font-size: 24rpx;
      color: $text-secondary;
      margin-top: 15rpx;
      text-align: center;
    }
    
    .bar-value {
      font-size: 24rpx;
      color: $primary-color;
      margin-top: 5rpx;
    }
  }
}

/* 活动列表 */
.activities-list {
  .activity-item {
    display: flex;
    margin-bottom: 25rpx;
    padding-bottom: 25rpx;
    border-bottom: 1rpx solid #f0f0f0;
    
    &:last-child {
      margin-bottom: 0;
      padding-bottom: 0;
      border-bottom: none;
    }
    
    .activity-cover {
      width: 200rpx;
      height: 150rpx;
      border-radius: 12rpx;
      margin-right: 20rpx;
    }
    
    .activity-info {
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      
      .activity-title {
        font-size: 30rpx;
        font-weight: 500;
        color: $text-primary;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
        text-overflow: ellipsis;
      }
      
      .activity-date {
        font-size: 24rpx;
        color: $text-tertiary;
      }
    }
  }
}

/* 操作按钮 */
.action-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 20rpx 30rpx;
  background-color: white;
  box-shadow: 0 -2rpx 8rpx rgba(0, 0, 0, 0.1);
  z-index: 100;
  
  .action-button {
    width: 100%;
    height: 90rpx;
    line-height: 90rpx;
    border-radius: 45rpx;
    font-size: 32rpx;
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    opacity: 0.7;
    transition: opacity 0.3s;
    
    &:not(:disabled) {
      opacity: 1;
      cursor: pointer;
    }
    
    .btn-icon {
      margin-right: 15rpx;
      font-size: 32rpx;
    }
  }
  
  .join-button {
    background: linear-gradient(135deg, $primary-color 0%, $secondary-color 100%);
  }
  
  .quit-button {
    background: linear-gradient(135deg, $danger-color 0%, #FF6B60 100%);
  }
  
  .manage-button {
    background: linear-gradient(135deg, $success-color 0%, #5AC8FA 100%);
  }
}

/* 加载状态 */
.loading-mask {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
  
  .loading-container {
    background-color: white;
    padding: 40rpx 60rpx;
    border-radius: 16rpx;
    display: flex;
    flex-direction: column;
    align-items: center;
    
    .loading-animation {
      width: 60rpx;
      height: 60rpx;
      border: 6rpx solid $primary-color;
      border-radius: 50%;
      border-top-color: transparent;
      animation: spin 1s linear infinite;
      margin-bottom: 20rpx;
    }
    
    .loading-text {
      font-size: 28rpx;
      color: $text-primary;
    }
  }
}

/* 错误状态 */
.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 300rpx;
  padding: 20rpx;
  
  .error-icon {
    font-size: 60rpx;
    color: $danger-color;
    margin-bottom: 20rpx;
  }
  
  .error-text {
    font-size: 28rpx;
    color: $text-secondary;
    margin-bottom: 30rpx;
    text-align: center;
  }
  
  .retry-button {
    background-color: $primary-color;
    color: white;
    font-size: 28rpx;
    padding: 15rpx 40rpx;
    border-radius: 40rpx;
  }
}

/* 动画 */
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>