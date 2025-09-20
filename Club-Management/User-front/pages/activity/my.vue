<template>
  <view class="container">
    <!-- 活动状态筛选标签 -->
    <view class="status-tabs">
      <view 
        class="tab-item" 
        :class="{ 'active': currentStatus === 'all' }"
        @click="switchStatus('all')"
      >
        全部
      </view>
      <view 
        class="tab-item" 
        :class="{ 'active': currentStatus === 'upcoming' }"
        @click="switchStatus('upcoming')"
      >
        未开始
      </view>
      <view 
        class="tab-item" 
        :class="{ 'active': currentStatus === 'ongoing' }"
        @click="switchStatus('ongoing')"
      >
        进行中
      </view>
      <view 
        class="tab-item" 
        :class="{ 'active': currentStatus === 'completed' }"
        @click="switchStatus('completed')"
      >
        已结束
      </view>
    </view>

    <!-- 加载状态 -->
    <view class="loading" v-if="isLoading && activities.length === 0">
      <view class="loading-icon">
        <i class="fa fa-spinner fa-spin"></i>
      </view>
      <view class="loading-text">加载中...</view>
    </view>

    <!-- 活动列表 -->
    <view class="activity-list" v-show="!isLoading || activities.length > 0">
      <!-- 根据当前筛选状态显示对应活动 -->
      <view v-if="currentStatus === 'upcoming' && filteredActivities.length > 0" class="section">
        <view class="section-title">未开始</view>
        <view class="activity-items">
          <view 
            class="activity-item" 
            v-for="(activity, index) in filteredActivities" 
            :key="activity.id"
            @click="goToActivityDetail(activity.id)"
          >
            <view class="activity-cover">
              <!-- 替换为默认图标和首字母 -->
              <view class="default-cover" :style="{backgroundColor: getCoverColor(activity.name)}">
                <i class="fa fa-calendar"></i>
                <text class="cover-initial">{{ getActivityInitial(activity.name) }}</text>
              </view>
              <view class="status-badge upcoming">未开始</view>
            </view>
            <view class="activity-info">
              <view class="activity-title">{{ activity.name }}</view>
              <view class="activity-time">
                <i class="fa fa-calendar"></i>
                {{ formatDateRange(activity.startTime, activity.endTime) }}
              </view>
              <view class="activity-place">
                <i class="fa fa-map-marker"></i>
                {{ activity.place || '未指定地点' }}
              </view>
              <view class="activity-club">
                <i class="fa fa-users"></i>
                {{ activity.clubName || '未知社团' }}
              </view>
            </view>
          </view>
        </view>
      </view>

      <view v-if="currentStatus === 'ongoing' && filteredActivities.length > 0" class="section">
        <view class="section-title">进行中</view>
        <view class="activity-items">
          <view 
            class="activity-item" 
            v-for="(activity, index) in filteredActivities" 
            :key="activity.id"
            @click="goToActivityDetail(activity.id)"
          >
            <view class="activity-cover">
              <!-- 替换为默认图标和首字母 -->
              <view class="default-cover" :style="{backgroundColor: getCoverColor(activity.name)}">
                <i class="fa fa-calendar"></i>
                <text class="cover-initial">{{ getActivityInitial(activity.name) }}</text>
              </view>
              <view class="status-badge ongoing">进行中</view>
            </view>
            <view class="activity-info">
              <view class="activity-title">{{ activity.name }}</view>
              <view class="activity-time">
                <i class="fa fa-calendar"></i>
                {{ formatDateRange(activity.startTime, activity.endTime) }}
              </view>
              <view class="activity-place">
                <i class="fa fa-map-marker"></i>
                {{ activity.place || '未指定地点' }}
              </view>
              <view class="activity-club">
                <i class="fa fa-users"></i>
                {{ activity.clubName || '未知社团' }}
              </view>
            </view>
          </view>
        </view>
      </view>

      <view v-if="currentStatus === 'completed' && filteredActivities.length > 0" class="section">
        <view class="section-title">已结束</view>
        <view class="activity-items">
          <view 
            class="activity-item" 
            v-for="(activity, index) in filteredActivities" 
            :key="activity.id"
            @click="goToActivityDetail(activity.id)"
          >
            <view class="activity-cover">
              <!-- 替换为默认图标和首字母 -->
              <view class="default-cover" :style="{backgroundColor: getCoverColor(activity.name)}">
                <i class="fa fa-calendar"></i>
                <text class="cover-initial">{{ getActivityInitial(activity.name) }}</text>
              </view>
              <view class="status-badge completed">已结束</view>
            </view>
            <view class="activity-info">
              <view class="activity-title">{{ activity.name }}</view>
              <view class="activity-time">
                <i class="fa fa-calendar"></i>
                {{ formatDateRange(activity.startTime, activity.endTime) }}
              </view>
              <view class="activity-place">
                <i class="fa fa-map-marker"></i>
                {{ activity.place || '未指定地点' }}
              </view>
              <view class="activity-club">
                <i class="fa fa-users"></i>
                {{ activity.clubName || '未知社团' }}
              </view>
            </view>
          </view>
        </view>
      </view>

      <view v-if="currentStatus === 'all'">
        <!-- 未开始的活动 -->
        <view class="section" v-if="upcomingActivities.length > 0">
          <view class="section-title">未开始</view>
          <view class="activity-items">
            <view 
              class="activity-item" 
              v-for="(activity, index) in upcomingActivities" 
              :key="activity.id"
              @click="goToActivityDetail(activity.id)"
            >
              <view class="activity-cover">
                <!-- 替换为默认图标和首字母 -->
                <view class="default-cover" :style="{backgroundColor: getCoverColor(activity.name)}">
                  <i class="fa fa-calendar"></i>
                  <text class="cover-initial">{{ getActivityInitial(activity.name) }}</text>
                </view>
                <view class="status-badge upcoming">未开始</view>
              </view>
              <view class="activity-info">
                <view class="activity-title">{{ activity.name }}</view>
                <view class="activity-time">
                  <i class="fa fa-calendar"></i>
                  {{ formatDateRange(activity.startTime, activity.endTime) }}
                </view>
                <view class="activity-place">
                  <i class="fa fa-map-marker"></i>
                  {{ activity.place || '未指定地点' }}
                </view>
                <view class="activity-club">
                  <i class="fa fa-users"></i>
                  {{ activity.clubName || '未知社团' }}
                </view>
              </view>
            </view>
          </view>
        </view>

        <!-- 进行中的活动 -->
        <view class="section" v-if="ongoingActivities.length > 0">
          <view class="section-title">进行中</view>
          <view class="activity-items">
            <view 
              class="activity-item" 
              v-for="(activity, index) in ongoingActivities" 
              :key="activity.id"
              @click="goToActivityDetail(activity.id)"
            >
              <view class="activity-cover">
                <!-- 替换为默认图标和首字母 -->
                <view class="default-cover" :style="{backgroundColor: getCoverColor(activity.name)}">
                  <i class="fa fa-calendar"></i>
                  <text class="cover-initial">{{ getActivityInitial(activity.name) }}</text>
                </view>
                <view class="status-badge ongoing">进行中</view>
              </view>
              <view class="activity-info">
                <view class="activity-title">{{ activity.name }}</view>
                <view class="activity-time">
                  <i class="fa fa-calendar"></i>
                  {{ formatDateRange(activity.startTime, activity.endTime) }}
                </view>
                <view class="activity-place">
                  <i class="fa fa-map-marker"></i>
                  {{ activity.place || '未指定地点' }}
                </view>
                <view class="activity-club">
                  <i class="fa fa-users"></i>
                  {{ activity.clubName || '未知社团' }}
                </view>
              </view>
            </view>
          </view>
        </view>

        <!-- 已结束的活动 -->
        <view class="section" v-if="completedActivities.length > 0">
          <view class="section-title">已结束</view>
          <view class="activity-items">
            <view 
              class="activity-item" 
              v-for="(activity, index) in completedActivities" 
              :key="activity.id"
              @click="goToActivityDetail(activity.id)"
            >
              <view class="activity-cover">
                <!-- 替换为默认图标和首字母 -->
                <view class="default-cover" :style="{backgroundColor: getCoverColor(activity.name)}">
                  <i class="fa fa-calendar"></i>
                  <text class="cover-initial">{{ getActivityInitial(activity.name) }}</text>
                </view>
                <view class="status-badge completed">已结束</view>
              </view>
              <view class="activity-info">
                <view class="activity-title">{{ activity.name }}</view>
                <view class="activity-time">
                  <i class="fa fa-calendar"></i>
                  {{ formatDateRange(activity.startTime, activity.endTime) }}
                </view>
                <view class="activity-place">
                  <i class="fa fa-map-marker"></i>
                  {{ activity.place || '未指定地点' }}
                </view>
                <view class="activity-club">
                  <i class="fa fa-users"></i>
                  {{ activity.clubName || '未知社团' }}
                </view>
              </view>
            </view>
          </view>
        </view>
      </view>

      <!-- 空状态 -->
      <view class="empty-state" v-if="filteredActivities.length === 0 && !isLoading">
        <image src="/static/no-activity.svg" class="empty-img" mode="aspectFit" />
        <view class="empty-text">暂无相关活动</view>
        <view class="empty-subtext">快去参加感兴趣的活动吧</view>
        <button class="explore-btn" @click="exploreActivities">
          发现活动
        </button>
      </view>

      <!-- 加载更多提示 -->
      <view class="loading-more" v-if="isLoadingMore">
        <view class="loading-icon">
          <i class="fa fa-spinner fa-spin"></i>
        </view>
        <view class="loading-text">加载更多...</view>
      </view>

      <!-- 没有更多数据 -->
      <view class="no-more-data" v-if="!hasMore && activities.length > 0">
        <view class="line"></view>
        <view class="text">没有更多数据了</view>
        <view class="line"></view>
      </view>
    </view>
  </view>
</template>

<script>
import { mapState } from 'vuex';

export default {
  data() {
    return {
      baseUrl: "http://localhost:8080",
      currentStatus: 'all', // 当前筛选状态
      activities: [], // 所有活动
      isLoading: true,
      isLoadingMore: false,
      page: 1,
      pageSize: 10,
      hasMore: true,
      activityIdSet: new Set() // 用于存储已加载的活动ID，防止重复
    };
  },
  onLoad() {
    this.loadMyActivities();
  },
  computed: {
    ...mapState(['userInfo']),
    
    // 未开始的活动
    upcomingActivities() {
      const now = new Date();
      return this.activities.filter(activity => {
        const startTime = new Date(activity.startTime);
        return startTime > now;
      });
    },
    
    // 进行中的活动
    ongoingActivities() {
      const now = new Date();
      return this.activities.filter(activity => {
        const startTime = new Date(activity.startTime);
        const endTime = new Date(activity.endTime);
        return startTime <= now && endTime >= now;
      });
    },
    
    // 已结束的活动
    completedActivities() {
      const now = new Date();
      return this.activities.filter(activity => {
        const endTime = new Date(activity.endTime);
        return endTime < now;
      });
    },
    
    // 筛选后的活动列表
    filteredActivities() {
      switch (this.currentStatus) {
        case 'upcoming':
          return this.upcomingActivities;
        case 'ongoing':
          return this.ongoingActivities;
        case 'completed':
          return this.completedActivities;
        default:
          return this.activities;
      }
    }
  },
  methods: {
    // 获取活动名称首字母
    getActivityInitial(name) {
      if (!name) return '?';
      // 提取第一个非空字符
      const firstChar = name.trim().charAt(0);
      // 检查是否是中文字符
      if (/[\u4e00-\u9fa5]/.test(firstChar)) {
        return firstChar;
      }
      // 否则返回首字母大写
      return firstChar.toUpperCase();
    },
    
    // 根据活动名称生成不同的背景色
    getCoverColor(name) {
      if (!name) return '#7d79f4';
      
      // 颜色池
      const colors = [
        '#7d79f4', '#409EFF', '#36CFC9', '#52C41A', '#FAAD14', 
        '#FF7A45', '#F5222D', '#EB0AA4', '#722ED1', '#13C2C2'
      ];
      
      // 根据活动名称生成哈希值，确保同一活动始终使用相同颜色
      let hash = 0;
      for (let i = 0; i < name.length; i++) {
        hash = name.charCodeAt(i) + ((hash << 5) - hash);
      }
      
      // 映射到颜色池中的颜色
      return colors[Math.abs(hash) % colors.length];
    },
    
    // 加载我的活动
    loadMyActivities() {
      this.isLoading = true;
      this.activityIdSet.clear(); // 清空ID集合
      
      uni.request({
        url: `${this.baseUrl}/happy/activities/participated`,
        method: 'GET',
        data: {
          userId: this.userInfo.userId,
          page: this.page,
          pageSize: this.pageSize
        },
        success: (res) => {
          if (res.data.code === 200) {
            const newActivities = res.data.data || [];
            
            // 处理活动时间
            this.activities = this.processActivities(newActivities);
            
            // 判断是否还有更多数据
            this.hasMore = newActivities.length >= this.pageSize;
            
            console.log('我的活动加载成功:', this.activities);
          } else {
            uni.showToast({ title: res.data.msg || '获取活动失败', icon: 'none' });
          }
        },
        fail: () => {
          uni.showToast({ title: '网络错误，获取活动失败', icon: 'none' });
        },
        complete: () => {
          this.isLoading = false;
        }
      });
    },
    
    // 处理活动数据，适配后端接口返回的数据结构
    processActivities(activities) {
      const uniqueActivities = [];
      
      activities.forEach(activity => {
        // 只添加ID不存在的活动
        if (!this.activityIdSet.has(activity.activityId)) {
          this.activityIdSet.add(activity.activityId);
          
          // 映射后端字段到前端使用的字段名
          const processedActivity = {
            id: activity.activityId,
            name: activity.name,
            startTime: activity.startTime,
            endTime: activity.endTime,
            place: activity.location,
            clubName: activity.clubName,
            coverImage: activity.coverImage || '',
            isEnded: activity.isEnded
          };
          
          // 格式化日期时间
          if (processedActivity.startTime) {
            try {
              // 确保日期转换正确处理时区
              processedActivity.startTime = new Date(processedActivity.startTime);
            } catch (error) {
              console.error('startTime转换错误:', error);
              processedActivity.startTime = new Date();
            }
          }
          if (processedActivity.endTime) {
            try {
              // 确保日期转换正确处理时区
              processedActivity.endTime = new Date(processedActivity.endTime);
            } catch (error) {
              console.error('endTime转换错误:', error);
              processedActivity.endTime = new Date();
            }
          }
          
          uniqueActivities.push(processedActivity);
        }
      });
      
      return uniqueActivities;
    },
    
    // 格式化日期范围
    formatDateRange(startTime, endTime) {
      if (!startTime) return '时间待定';
      
      const startDate = new Date(startTime);
      const endDate = endTime ? new Date(endTime) : null;
      
      const startStr = startDate.toLocaleDateString('zh-CN', {
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      });
      
      if (!endDate) return startStr;
      
      const endStr = endDate.toLocaleDateString('zh-CN', {
        hour: '2-digit',
        minute: '2-digit'
      });
      
      return `${startStr} - ${endStr}`;
    },
    
    // 切换活动状态筛选
    switchStatus(status) {
      if (this.currentStatus !== status) {
        this.currentStatus = status;
        
        // 添加切换动画
        this.$nextTick(() => {
          const activityItems = uni.createSelectorQuery().selectAll('.activity-item');
          activityItems.boundingClientRect((rects) => {
            rects.forEach((rect, index) => {
              const item = uni.createSelectorQuery().select(`.activity-item:nth-child(${index + 1})`);
              // 修复判断条件，使用实际活动对象而非索引
              const isVisible = this.filteredActivities.some(act => act.id === this.activities[index]?.id);
              item.animation({
                opacity: isVisible ? 1 : 0,
                duration: 300
              }).exec();
            });
          }).exec();
        });
      }
    },
    
    // 返回上一页
    navigateBack() {
      uni.navigateBack();
    },
    
    // 前往活动详情页
    goToActivityDetail(id) {
      console.log('前往活动详情，ID:', id);
      uni.navigateTo({ url: `/pages/activity/detail?id=${id}` });
    },
    
    // 探索更多活动
    exploreActivities() {
      uni.switchTab({ url: '/pages/notice/list' });
    },
    
    // 下拉刷新
    onPullDownRefresh() {
      this.page = 1;
      this.hasMore = true;
      this.loadMyActivities();
      uni.stopPullDownRefresh();
    },
    
    // 上拉加载更多
    onReachBottom() {
      if (this.hasMore && !this.isLoadingMore) {
        this.page++;
        this.loadMoreActivities();
      }
    },
    
    // 加载更多活动
    loadMoreActivities() {
      this.isLoadingMore = true;
      
      uni.request({
        url: `${this.baseUrl}/happy/activities/participated`,
        method: 'GET',
        data: {
          userId: this.userInfo.userId,
          page: this.page,
          pageSize: this.pageSize
        },
        success: (res) => {
          if (res.data.code === 200) {
            const newActivities = res.data.data || [];
            
            // 处理活动时间
            const processedActivities = this.processActivities(newActivities);
            
            // 合并新旧数据
            this.activities = [...this.activities, ...processedActivities];
            
            // 判断是否还有更多数据
            this.hasMore = newActivities.length >= this.pageSize;
            
            console.log('加载更多活动成功:', processedActivities);
          } else {
            uni.showToast({ title: res.data.msg || '获取活动失败', icon: 'none' });
          }
        },
        fail: () => {
          uni.showToast({ title: '网络错误，获取活动失败', icon: 'none' });
        },
        complete: () => {
          this.isLoadingMore = false;
        }
      });
    }
  }
};
</script>

<style lang="scss" scoped>
$primary-color: #7d79f4;
$upcoming-color: #409EFF;
$ongoing-color: #36CFC9;
$completed-color: #999;
$text-dark: #222;
$text-medium: #666;
$text-light: #999;
$bg-white: #FFF;
$bg-light: #F8F8F8;
$radius: 20rpx;
$shadow-level1: 0 6rpx 32rpx rgba(0, 0, 0, 0.08);

.container {
  background: $bg-light;
  min-height: 100vh;
}

.header {
  height: 100rpx;
  background: $bg-white;
  display: flex;
  align-items: center;
  padding: 0 30rpx;
  border-bottom: 1rpx solid #F0F0F0;
  
  .back-btn {
    width: 60rpx;
    height: 60rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    
    i {
      font-size: 32rpx;
      color: $text-dark;
    }
  }
  
  .title {
    flex: 1;
    text-align: center;
    font-size: 36rpx;
    font-weight: 500;
    color: $text-dark;
  }
}

.status-tabs {
  display: flex;
  background: $bg-white;
  height: 90rpx;
  border-bottom: 1rpx solid #F0F0F0;
  
  .tab-item {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 28rpx;
    color: $text-medium;
    position: relative;
    
    &::after {
      content: '';
      position: absolute;
      bottom: 0;
      left: 50%;
      transform: translateX(-50%);
      width: 60rpx;
      height: 6rpx;
      background: $primary-color;
      border-radius: 3rpx;
      opacity: 0;
      transition: opacity 0.3s ease;
    }
    
    &.active {
      color: $primary-color;
      font-weight: 500;
      
      &::after {
        opacity: 1;
      }
    }
  }
}

.loading, .loading-more {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40rpx 0;
  
  .loading-icon {
    margin-bottom: 16rpx;
    
    i {
      font-size: 36rpx;
      color: $primary-color;
    }
  }
  
  .loading-text {
    font-size: 28rpx;
    color: $text-medium;
  }
}

.no-more-data {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40rpx 0;
  
  .line {
    flex: 1;
    height: 1rpx;
    background: #E5E5E5;
  }
  
  .text {
    font-size: 26rpx;
    color: $text-light;
    margin: 0 20rpx;
  }
}

.activity-list {
  padding: 20rpx;
}

.section {
  margin-bottom: 30rpx;
  
  .section-title {
    font-size: 30rpx;
    font-weight: 500;
    color: $text-dark;
    padding: 20rpx;
    background: $bg-white;
    border-radius: $radius $radius 0 0;
  }
  
  .activity-items {
    background: $bg-white;
    border-radius: 0 0 $radius $radius;
  }
}

.activity-item {
  display: flex;
  padding: 20rpx;
  border-bottom: 1rpx solid #F5F5F5;
  transition: transform 0.3s ease;
  
  &:last-child {
    border-bottom: none;
  }
  
  &:hover {
    transform: translateY(-4rpx);
  }
  
  .activity-cover {
    width: 200rpx;
    height: 160rpx;
    border-radius: $radius;
    overflow: hidden;
    position: relative;
    
    .default-cover {
      width: 100%;
      height: 100%;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      
      i {
        font-size: 48rpx;
        color: rgba(255, 255, 255, 0.7);
        margin-bottom: 8rpx;
      }
      
      .cover-initial {
        font-size: 40rpx;
        font-weight: bold;
        color: white;
      }
    }
    
    .status-badge {
      position: absolute;
      top: 10rpx;
      left: 10rpx;
      padding: 4rpx 16rpx;
      border-radius: 20rpx;
      font-size: 22rpx;
      color: $bg-white;
    }
    
    .upcoming {
      background: $upcoming-color;
    }
    
    .ongoing {
      background: $ongoing-color;
    }
    
    .completed {
      background: $completed-color;
    }
  }
  
  .activity-info {
    flex: 1;
    margin-left: 20rpx;
    
    .activity-title {
      font-size: 32rpx;
      font-weight: 500;
      color: $text-dark;
      margin-bottom: 12rpx;
      display: -webkit-box;
      -webkit-line-clamp: 1;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }
    
    .activity-time, .activity-place, .activity-club {
      font-size: 26rpx;
      color: $text-medium;
      margin-bottom: 8rpx;
      display: flex;
      align-items: center;
      
      i {
        width: 32rpx;
        color: $primary-color;
      }
    }
  }
}

.empty-state {
  padding: 100rpx 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  
  .empty-img {
    width: 360rpx;
    height: 360rpx;
    margin-bottom: 40rpx;
  }
  
  .empty-text {
    font-size: 32rpx;
    font-weight: 500;
    color: $text-dark;
    margin-bottom: 16rpx;
  }
  
  .empty-subtext {
    font-size: 28rpx;
    color: $text-medium;
    margin-bottom: 40rpx;
  }
  
  .explore-btn {
    padding: 16rpx 60rpx;
    background: $primary-color;
    color: $bg-white;
    border-radius: 50rpx;
    font-size: 30rpx;
    box-shadow: 0 8rpx 24rpx rgba(125, 121, 244, 0.3);
  }
}
</style>  