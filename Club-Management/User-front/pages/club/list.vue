<template>
  <view class="container">    
    <!-- 顶部导航栏 -->
<!--    <view class="header">
      <view class="back-btn" @click="navigateBack">
        <i class="fa fa-arrow-left"></i>
      </view>
      <text class="title">我的社团</text>
    </view> -->

    <!-- 搜索栏 -->
    <view class="search-bar">
      <view class="search-input">
        <i class="fa fa-search"></i>
        <input 
          type="text" 
          placeholder="搜索社团名称或简介..." 
          @input="onSearchInput"
          :placeholder-style="placeholderStyle"
        />
      </view>
    </view>

    <!-- 社团列表 -->
    <view class="club-list">
      <!-- 加载状态 -->
      <view class="loading-state" v-if="isLoading">
        <view class="spinner"></view>
        <text class="loading-text">正在加载你的社团...</text>
      </view>

      <!-- 社团卡片 -->
      <view 
        class="club-card" 
        v-for="club in filteredClubs" 
        :key="club.clubId" 
        @click="goToClubDetail(club.clubId)"
        :style="{ '--badge-color': club.isAdmin ? '#FF6B6B' : '#7D79F4' }"
      >
        <view class="card-thumbnail">
          <image 
            :src="getClubLogo(club.logoUrl)" 
            class="club-logo" 
            mode="aspectFill" 
            lazy-load
          />
          <!-- 管理员徽章 -->
          <view class="admin-badge" v-if="club.isAdmin">
            <text>管</text>
          </view>
        </view>

        <view class="card-content">
          <text class="club-name">{{ club.name }}</text>
          <text class="club-desc">{{ club.description }}</text>

          <view class="card-meta">
            <view class="meta-item">
              <i class="fa fa-calendar"></i>
              <text>加入于 {{ formatDate(club.joinTime) }}</text>
            </view>
          </view>
        </view>
      </view>

      <!-- 空状态 -->
      <view class="empty-state" v-if="filteredClubs.length === 0">
        <image src="/static/no-club.svg" class="empty-img" mode="aspectFit" />
        <text class="empty-title">暂无加入的社团</text>
        <text class="empty-subtitle">点击下方按钮发现更多精彩社团</text>
        <button class="explore-btn" @click="goToClubList">
          <text>探索社团</text>
        </button>
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
      userId: null,
      clubList: [],
      searchKeyword: '',
      isLoading: false,
      placeholderStyle: 'color: #999; font-size: 24rpx;' // 搜索框占位符样式
    };
  },
  computed: {
    ...mapState(['userInfo']),
    filteredClubs() {
      if (!this.searchKeyword) return this.clubList;
      const keyword = this.searchKeyword.toLowerCase();
      return this.clubList.filter(club => 
        club.name.toLowerCase().includes(keyword) || 
        club.description.toLowerCase().includes(keyword)
      );
    }
  },
  onLoad() {
    this.userId = this.userInfo.userId;
    if (!this.userId) return uni.showToast({ title: '用户信息异常', icon: 'none' });
    this.loadClubList();
  },
  methods: {
    // 获取完整图片路径
    getClubLogo(logoPath) {
      return logoPath ? `${this.baseUrl}${logoPath}` : '/static/default-club-logo.png';
    },
    // 加载社团列表
    loadClubList() {
      this.isLoading = true;
      uni.request({
        url: `${this.baseUrl}/happy/clubs/${this.userId}`,
        success: (res) => {
          if (res.data.code === 200) {
            this.clubList = res.data.data || [];
          } else {
            uni.showToast({ title: '加载失败，请重试', icon: 'none' });
          }
        },
        complete: () => this.isLoading = false
      });
    },
    // 格式化日期
    formatDate(timestamp) {
      if (!timestamp) return '未记录';
      const date = new Date(timestamp);
      return date.toLocaleDateString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit' });
    },
    // 跳转详情页
    goToClubDetail(clubId) {
      uni.navigateTo({ url: `/pages/club/myClub?clubId=${clubId}` });
    },
    // 返回上一页
    navigateBack() {
      uni.navigateBack();
    },
    // 搜索输入处理
    onSearchInput(e) {
      this.searchKeyword = e.detail.value;
    }
  }
};
</script>

<style lang="scss" scoped>
$primary-color: #7d79f4;
$secondary-color: #9d99ff;
$danger-color: #FF6B6B;
$text-dark: #222;
$text-medium: #666;
$text-light: #999;
$bg-white: #FFF;
$bg-light: #F8F8F8;
$radius: 16rpx;
$shadow-level1: 0 4rpx 24rpx rgba(0, 0, 0, 0.06);
$shadow-level2: 0 8rpx 32rpx rgba(0, 0, 0, 0.1);

.container {
  display: flex;
  flex-direction: column;
  background: $bg-light;
  min-height: 100vh;
}

/* 顶部导航栏 */
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

/* 搜索栏 */
.search-bar {
  padding: 20rpx 30rpx;
  background: $bg-white;
  border-bottom: 1rpx solid #F0F0F0;
}

.search-input {
  display: flex;
  align-items: center;
  height: 80rpx;
  background: #F9F9F9;
  border-radius: $radius;
  padding: 0 30rpx;
  box-shadow: inset 0 2rpx 8rpx rgba(0, 0, 0, 0.04);
  
  i {
    font-size: 28rpx;
    color: $text-medium;
    margin-right: 20rpx;
  }
  
  input {
    flex: 1;
    font-size: 28rpx;
    color: $text-dark;
    &::placeholder {
      color: $text-light;
    }
  }
}

/* 社团卡片 */
.club-list {
  flex: 1;
  padding: 30rpx;
  gap: 30rpx;
  display: grid;
}

.club-card {
  position: relative;
  background: $bg-white;
  border-radius: $radius;
  box-shadow: $shadow-level1;
  overflow: hidden;
  transition: all 0.2s ease;
  display: grid;
  grid-template-columns: 1fr 3fr;
  column-gap: 30rpx;
  
  &:hover {
    transform: translateY(-4rpx);
    box-shadow: $shadow-level2;
  }

.card-thumbnail {
  width: 160rpx;
  height: 160rpx;
  position: relative;
  
  .club-logo {
    width: 100%;
    height: 100%;
    border-radius: $radius;
  }

  .admin-badge {
    position: absolute;
    top: -12rpx;
    right: -12rpx;
    width: 56rpx;
    height: 56rpx;
    background: var(--badge-color);
    color: white;
    font-size: 24rpx;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
  }
}

.card-content {
  padding: 30rpx 0;
  display: grid;
  gap: 16rpx;
  
  .club-name {
    font-size: 32rpx;
    font-weight: 600;
    color: $text-dark;
  }

  .club-desc {
    font-size: 26rpx;
    color: $text-medium;
    line-height: 1.5;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }

  .card-meta {
    display: flex;
    gap: 30rpx;
    font-size: 24rpx;
    color: $text-light;
    
    .meta-item {
      display: flex;
      align-items: center;
      gap: 8rpx;
      
      i {
        font-size: 30rpx;
        color: var(--badge-color);
      }
    }
  }
}

/* 空状态 */
.empty-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  gap: 30rpx;
  
  .empty-img {
    width: 320rpx;
    height: 320rpx;
  }

  .empty-title {
    font-size: 32rpx;
    font-weight: 500;
    color: $text-dark;
  }

  .empty-subtitle {
    font-size: 26rpx;
    color: $text-medium;
    margin-bottom: 40rpx;
  }

  .explore-btn {
    width: 280rpx;
    height: 90rpx;
    background: linear-gradient(135deg, $primary-color, $secondary-color);
    color: white;
    font-size: 30rpx;
    font-weight: 500;
    border-radius: 45rpx;
    box-shadow: 0 8rpx 24rpx rgba(125, 121, 244, 0.3);
  }
}

/* 加载状态 */
.loading-state {
  padding: 60rpx 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20rpx;
  
  .spinner {
    width: 64rpx;
    height: 64rpx;
    border: 8rpx solid $primary-color;
    border-right-color: transparent;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }

  .loading-text {
    font-size: 28rpx;
    color: $text-medium;
  }
}

@keyframes spin {
  to { transform: rotate(360deg); }
}}
</style>